"""
PE投资评分引擎 — 核心评分逻辑
"""

import numpy as np
from .dimensions import DIMENSIONS, DIM_NAMES, DIM_INDICES
from .weights import get_weights, get_grade, DEFAULT_WEIGHTS


class PEScorer:
    """PE投资项目评分器

    使用方法:
        scorer = PEScorer()
        result = scorer.score(
            name="某项目",
            stage="early",
            scores=[5,4,3,4,2, ...],  # 35个子指标评分
        )
        print(result.summary())
    """

    def __init__(self, weights: dict = None):
        """初始化评分器

        Args:
            weights: 自定义阶段权重映射，None则使用默认权重
        """
        self._custom_weights = weights

    def score(self, name: str, stage: str, scores: list) -> "ScoreResult":
        """对单个项目进行评分

        Args:
            name: 项目名称
            stage: 投资阶段 (early/late/seed/pre_ipo)
            scores: 35个子指标评分列表 [1-5]

        Returns:
            ScoreResult 评分结果对象
        """
        if len(scores) != 35:
            raise ValueError(f"需要35个子指标评分，收到{len(scores)}个")

        for i, s in enumerate(scores):
            if not (1 <= s <= 5):
                raise ValueError(f"子指标评分必须在1-5之间，第{i+1}个评分为{s}")

        # 计算维度分（等权均值）
        dim_scores = self._calc_dim_scores(scores)

        # 计算综合评分（加权）
        weights = self._get_weights(stage)
        composite = sum(d * w for d, w in zip(dim_scores, weights))

        # 评级
        grade = get_grade(composite)

        # 找出优势和劣势维度
        dim_ranked = sorted(
            zip(DIM_NAMES, dim_scores), key=lambda x: x[1], reverse=True
        )

        # 找出关键子指标（最高和最低的各3个）
        indexed_scores = list(enumerate(scores))
        top_subs = sorted(indexed_scores, key=lambda x: x[1], reverse=True)[:3]
        bottom_subs = sorted(indexed_scores, key=lambda x: x[1])[:3]

        return ScoreResult(
            name=name,
            stage=stage,
            scores_35=scores,
            dim_scores=dict(zip(DIM_NAMES, dim_scores)),
            composite=composite,
            grade=grade,
            weights_used=weights,
            strengths=[d for d, s in dim_ranked[:2]],
            weaknesses=[d for d, s in dim_ranked[-2:]],
            top_sub_names=[self._sub_index_to_name(i) for i, _ in top_subs],
            bottom_sub_names=[self._sub_index_to_name(i) for i, _ in bottom_subs],
        )

    def score_from_dict(self, name: str, stage: str, dim_scores_dict: dict) -> "ScoreResult":
        """从维度字典评分（不填子指标，直接填维度分）

        Args:
            name: 项目名称
            stage: 投资阶段
            dim_scores_dict: 维度名→评分 的字典，如 {"团队": 3.5, "市场": 4.0, ...}

        Returns:
            ScoreResult
        """
        dim_scores = []
        for dim in DIM_NAMES:
            if dim not in dim_scores_dict:
                raise ValueError(f"缺少维度评分: {dim}")
            s = dim_scores_dict[dim]
            if not (1 <= s <= 5):
                raise ValueError(f"维度'{dim}'评分必须在1-5之间，收到{s}")
            dim_scores.append(s)

        weights = self._get_weights(stage)
        composite = sum(d * w for d, w in zip(dim_scores, weights))
        grade = get_grade(composite)

        dim_ranked = sorted(zip(DIM_NAMES, dim_scores), key=lambda x: x[1], reverse=True)

        return ScoreResult(
            name=name,
            stage=stage,
            scores_35=None,  # 简化模式无子指标
            dim_scores=dict(zip(DIM_NAMES, dim_scores)),
            composite=composite,
            grade=grade,
            weights_used=weights,
            strengths=[d for d, _ in dim_ranked[:2]],
            weaknesses=[d for d, _ in dim_ranked[-2:]],
            top_sub_names=[],
            bottom_sub_names=[],
        )

    def compare(self, results: list) -> dict:
        """对比多个项目的评分结果

        Args:
            results: ScoreResult 列表

        Returns:
            对比摘要字典
        """
        ranked = sorted(results, key=lambda r: r.composite, reverse=True)
        return {
            "ranking": [(r.name, r.composite, r.grade) for r in ranked],
            "best": ranked[0].name,
            "worst": ranked[-1].name,
            "avg_composite": np.mean([r.composite for r in results]),
        }

    def _calc_dim_scores(self, scores_35: list) -> list:
        """从35个子指标计算7个维度分"""
        dim_scores = []
        for dim in DIM_NAMES:
            start, end = DIM_INDICES[dim]
            dim_scores.append(np.mean(scores_35[start:end]))
        return dim_scores

    def _get_weights(self, stage: str) -> list:
        """获取权重"""
        if self._custom_weights and stage in self._custom_weights:
            return self._custom_weights[stage]
        return get_weights(stage)

    @staticmethod
    def _sub_index_to_name(idx: int) -> str:
        """子指标索引转名称"""
        offset = 0
        for dim, subs in DIMENSIONS.items():
            if idx < offset + len(subs):
                return f"{dim}_{subs[idx - offset]}"
            offset += len(subs)
        return f"sub_{idx}"


class ScoreResult:
    """评分结果"""

    def __init__(self, name, stage, scores_35, dim_scores, composite,
                 grade, weights_used, strengths, weaknesses,
                 top_sub_names, bottom_sub_names):
        self.name = name
        self.stage = stage
        self.scores_35 = scores_35
        self.dim_scores = dim_scores
        self.composite = composite
        self.grade = grade
        self.weights_used = weights_used
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.top_sub_names = top_sub_names
        self.bottom_sub_names = bottom_sub_names

    def summary(self) -> str:
        """生成评分摘要文本"""
        lines = [
            f"{'='*50}",
            f"  PE-Score 评分报告: {self.name}",
            f"{'='*50}",
            f"  投资阶段: {self.stage}",
            f"  综合评分: {self.composite:.2f} / 5.00",
            f"  投资评级: {self.grade}级",
            f"",
            f"  维度评分:",
        ]
        for dim, score in self.dim_scores.items():
            bar = "★" * int(round(score)) + "☆" * (5 - int(round(score)))
            lines.append(f"    {dim:>4}  {bar}  {score:.2f}")

        lines.append(f"")
        lines.append(f"  优势维度: {', '.join(self.strengths)}")
        lines.append(f"  劣势维度: {', '.join(self.weaknesses)}")

        if self.top_sub_names:
            lines.append(f"  最强子指标: {', '.join(self.top_sub_names[:3])}")
            lines.append(f"  最弱子指标: {', '.join(self.bottom_sub_names[:3])}")

        # 投资建议
        lines.append(f"")
        lines.append(f"  投资建议: {self._recommendation()}")
        lines.append(f"{'='*50}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """转为字典格式"""
        return {
            "name": self.name,
            "stage": self.stage,
            "composite": round(self.composite, 3),
            "grade": self.grade,
            "dim_scores": {k: round(v, 3) for k, v in self.dim_scores.items()},
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
        }

    def _recommendation(self) -> str:
        """根据评级给出建议"""
        if self.grade == "A":
            return "强烈推荐 — 综合优势显著，建议优先推进尽调"
        elif self.grade == "B":
            return "值得深入 — 整体可行，关注劣势维度风险"
        elif self.grade == "C":
            return "谨慎评估 — 存在明显短板，需重点验证关键假设"
        else:
            return "风险较高 — 多维度不足，建议暂缓或放弃"
