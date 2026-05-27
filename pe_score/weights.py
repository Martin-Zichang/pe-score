"""
分阶段权重方案 — 基于回测优化

早期项目（A轮及以前）: 更重市场+技术，轻财务
后期项目（B轮及以后/Pre-IPO）: 更重退出+政策，财务权重提升
"""

# 分阶段权重: [团队, 市场, 技术, 财务, 退出, 政策, 催化剂]
STAGE_WEIGHTS = {
    "early": [0.15, 0.25, 0.25, 0.05, 0.10, 0.10, 0.10],
    "late":  [0.10, 0.20, 0.15, 0.10, 0.20, 0.15, 0.10],
    "seed":  [0.15, 0.25, 0.25, 0.03, 0.07, 0.10, 0.15],  # 种子轮: 最重市场+技术+催化剂
    "pre_ipo": [0.08, 0.15, 0.10, 0.12, 0.25, 0.18, 0.12],  # Pre-IPO: 最重退出+政策
}

# 默认权重（未知阶段时使用）
DEFAULT_WEIGHTS = [0.12, 0.22, 0.20, 0.08, 0.15, 0.12, 0.10]

# 评级阈值
GRADE_THRESHOLDS = {
    "A": 4.0,  # 优秀
    "B": 3.0,  # 良好
    "C": 2.0,  # 一般
    # < 2.0 = D (较差)
}


def get_weights(stage: str) -> list:
    """获取指定阶段的权重向量"""
    return STAGE_WEIGHTS.get(stage, DEFAULT_WEIGHTS)


def get_grade(score: float) -> str:
    """根据综合评分返回评级"""
    if score >= GRADE_THRESHOLDS["A"]:
        return "A"
    elif score >= GRADE_THRESHOLDS["B"]:
        return "B"
    elif score >= GRADE_THRESHOLDS["C"]:
        return "C"
    else:
        return "D"
