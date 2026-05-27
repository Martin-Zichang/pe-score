"""
PE-Score 快速示例
"""

from pe_score import PEScorer, DIMENSIONS

# ===== 示例1: 完整35子指标评分 =====
scorer = PEScorer()

# 寒武纪A轮评分（来自回测数据）
cambricon_scores = [
    # 团队(5个子指标)
    5, 2, 2, 3, 4,
    # 市场
    5, 3, 4, 3, 2,
    # 技术
    5, 3, 3, 2, 4,
    # 财务
    1, 2, 1, 1, 2,
    # 退出
    4, 4, 4, 3, 4,
    # 政策
    5, 4, 5, 5, 4,
    # 催化剂
    4, 5, 4, 4, 4,
]

result = scorer.score("寒武纪", "early", cambricon_scores)
print(result.summary())
print()

# ===== 示例2: 简化7维度评分 =====
result2 = scorer.score_from_dict(
    name="某AI芯片项目",
    stage="early",
    dim_scores_dict={
        "团队": 3.5,
        "市场": 4.2,
        "技术": 4.0,
        "财务": 2.0,
        "退出": 3.5,
        "政策": 4.5,
        "催化剂": 4.0,
    }
)
print(result2.summary())
print()

# ===== 示例3: 对比多个项目 =====
project_a = scorer.score_from_dict("项目A-半导体", "early", {
    "团队": 4.0, "市场": 4.5, "技术": 4.5, "财务": 2.0, "退出": 3.5, "政策": 4.5, "催化剂": 4.0
})
project_b = scorer.score_from_dict("项目B-新能源", "late", {
    "团队": 3.5, "市场": 4.0, "技术": 3.5, "财务": 3.0, "退出": 4.0, "政策": 4.5, "催化剂": 3.0
})
project_c = scorer.score_from_dict("项目C-消费", "late", {
    "团队": 3.0, "市场": 3.0, "技术": 2.0, "财务": 3.5, "退出": 2.5, "政策": 2.0, "催化剂": 2.0
})

comparison = scorer.compare([project_a, project_b, project_c])
print("项目对比:")
for name, score, grade in comparison["ranking"]:
    print(f"  {name}: {score:.2f} ({grade}级)")
print(f"  推荐优先: {comparison['best']}")
