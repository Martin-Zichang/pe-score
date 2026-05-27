# PE-Score 🎯

**Data-driven PE investment scoring framework** — 7 dimensions, 35 sub-indicators, backtested on 31 Chinese PE/VC cases (Spearman ρ = 0.864)

> The **only** open-source PE investment scoring tool with empirical backtesting.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Why PE-Score?

Most PE investment decisions rely on gut feeling and incomplete frameworks. PE-Score changes that:

- **Quantified, not qualitative** — Every dimension and sub-indicator is scored 1-5 with clear definitions
- **Backtested** — Validated on 31 real Chinese PE/VC cases (2016-2021) with ρ=0.864 correlation to actual returns
- **Stage-adaptive** — Different weight schemes for seed/early/late/Pre-IPO stages
- **Open source** — Transparent methodology you can audit, customize, and contribute to

### Backtest Results

| Metric | Value |
|--------|-------|
| Composite score vs. log-return correlation | **ρ = 0.864** (p ≈ 0) |
| A-grade (≥4.0) average return | **215x** |
| Score ≥ 3.5 → return > 5x | **90%** of cases |
| Top predictive dimension | 退出 (Exit, ρ = 0.836) |
| Top predictive sub-indicator | 逆向信号 (Contrarian Signal, ρ = 0.890) |

---

## Quick Start

```bash
pip install pe-score
```

### Score a project (35 sub-indicators)

```python
from pe_score import PEScorer

scorer = PEScorer()

# Full 35 sub-indicator scoring (1-5 each)
result = scorer.score(
    name="某AI芯片项目",
    stage="early",
    scores=[
        5,2,2,3,4,  # 团队: 行业势能5, 操盘能力2, 团队完整2, 治理3, 关键人风险4
        5,3,4,3,2,  # 市场
        5,3,3,2,4,  # 技术
        1,2,1,1,2,  # 财务
        4,4,4,3,4,  # 退出
        5,4,5,5,4,  # 政策
        4,5,4,4,4,  # 催化剂
    ]
)

print(result.summary())
```

Output:
```
==================================================
  PE-Score 评分报告: 某AI芯片项目
==================================================
  投资阶段: early
  综合评分: 3.41 / 5.00
  投资评级: B级

  维度评分:
     团队  ★★★☆☆  3.20
     市场  ★★★☆☆  3.40
     技术  ★★★☆☆  3.40
     财务  ★☆☆☆☆  1.40
     退出  ★★★★☆  3.80
     政策  ★★★★★  4.60
    催化剂  ★★★★☆  4.20

  优势维度: 政策, 退出
  劣势维度: 财务, 团队

  投资建议: 值得深入 — 整体可行，关注劣势维度风险
==================================================
```

### Simplified scoring (7 dimensions only)

```python
result = scorer.score_from_dict(
    name="某新能源项目",
    stage="late",
    dim_scores_dict={
        "团队": 3.5, "市场": 4.0, "技术": 3.5,
        "财务": 3.0, "退出": 4.0, "政策": 4.5, "催化剂": 3.0
    }
)
print(result.composite)  # 3.63
print(result.grade)      # B
```

### Compare multiple projects

```python
projects = [scorer.score_from_dict(n, s, d) for n, s, d in [
    ("项目A-半导体", "early", {"团队":4, "市场":4.5, "技术":4.5, "财务":2, "退出":3.5, "政策":4.5, "催化剂":4}),
    ("项目B-新能源", "late",  {"团队":3.5, "市场":4, "技术":3.5, "财务":3, "退出":4, "政策":4.5, "催化剂":3}),
]]
print(scorer.compare(projects))
```

### CLI

```bash
# List all dimensions and sub-indicators
pe-score list

# Show weight schemes
pe-score weights

# Score with 7 dimensions (simplified)
pe-score score --name "某项目" --stage early --dims "3.5,4.0,4.0,2.0,3.5,4.5,4.0"

# Score with 35 sub-indicators
pe-score score --name "某项目" --stage early --scores "5,2,2,3,4,5,3,4,3,2,..."

# Output as JSON
pe-score score --name "某项目" --stage early --dims "3.5,4,4,2,3.5,4.5,4" --json
```

---

## The 7×5 Framework

| # | Dimension | Sub-indicators | Early Weight | Late Weight |
|---|-----------|---------------|:------------:|:-----------:|
| 1 | **团队** (Team) | 行业势能, 操盘能力, 拼图完整度, 治理与激励, 关键人风险 | 15% | 10% |
| 2 | **市场** (Market) | 天花板, 需求爆发时点, 竞争壁垒, 客户粘性, 下游分散度 | 25% | 20% |
| 3 | **技术** (Tech) | 原创度, IP厚度, 路线风险, 产业化成熟度, 追赶壁垒 | 25% | 15% |
| 4 | **财务** (Finance) | 营收质量, 盈利路径, 资本效率, 现金流, 规范性 | 5% | 10% |
| 5 | **退出** (Exit) | 路径明确度, 时间窗口, 监管适配, 估值锚定, 流动性 | 10% | 20% |
| 6 | **政策** (Policy) | 产业方向, 补贴红利, 合规风险, 国资适配, 地方支持 | 10% | 15% |
| 7 | **催化剂** (Catalyst) | 短期催化, 估值弹性, 周期位置, 逆向信号, 下轮预期 | 10% | 10% |

### Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Excellent — top 10% in this aspect |
| 4 | Good — above average |
| 3 | Average — industry standard |
| 2 | Below average — notable weakness |
| 1 | Poor — critical risk |

### Grade Thresholds

| Grade | Score Range | Interpretation |
|-------|-------------|----------------|
| **A** | ≥ 4.0 | Strong buy — proceed with due diligence |
| **B** | 3.0 – 3.99 | Worth exploring — watch weak dimensions |
| **C** | 2.0 – 2.99 | Caution — significant concerns, validate key assumptions |
| **D** | < 2.0 | High risk — multiple weaknesses, consider passing |

---

## Methodology

PE-Score is built on empirical analysis of **31 Chinese PE/VC investment cases** (2016-2021) covering AI/semiconductors, new energy, biotech, advanced manufacturing, and consumer internet.

### Key Findings from Backtesting

1. **Exit is the strongest predictor** (ρ = 0.836) — Not technology, not team. Whether you can exit matters more than what you invest in.
2. **Catalyst dimension is underrated** (ρ = 0.816) — Contrarian signals (逆向信号, ρ = 0.890) and competitive moat type (竞争壁垒类型, ρ = 0.869) are among the top 5 predictors.
3. **Financial metrics are the weakest predictor** (ρ = 0.514) — Especially for early-stage deals. Revenue quality matters less than whether the market exists.
4. **High valuation is the biggest risk** — Cases entering at >20B RMB valuation had 70%+ chance of negative returns regardless of other scores.
5. **Stage matters** — Early-stage returns are driven by market + technology bets; late-stage returns depend on exit timing + policy alignment.

### Known Limitations

- **Sample bias**: Cases are all from China's market (2016-2021). Different markets/periods may need weight recalibration.
- **False positive**: 中创新航 scored B (3.17) but returned 0.85x — high policy scores masked weak competitive moat.
- **Survivorship**: The backtest intentionally includes failed cases (9/31 returned < 1x), but there may be unreported failures.

---

## Roadmap

- [ ] Web UI (Streamlit) — interactive scoring with visualizations
- [ ] AI-assisted scoring — auto-score from BP/financial data
- [ ] More backtest cases (target: 50+)
- [ ] Industry-specific weight tuning
- [ ] PDF report generation
- [ ] English documentation

---

## Contributing

Contributions welcome! Especially:

- **New backtest cases** — Add your own PE/VC case data to improve the model
- **Industry-specific weights** — Calibrate for biotech, SaaS, hardware, etc.
- **International cases** — Help validate beyond China's market
- **Bug fixes & docs** — Any improvement is appreciated

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License — Use it, fork it, sell it. Just keep the attribution.

---

## Citation

If you use PE-Score in your work:

```
PE-Score: A Data-Driven PE Investment Scoring Framework
Ma Zichang, 2026
https://github.com/<your-username>/pe-score
```

---

**Disclaimer**: PE-Score is a decision-support tool, not investment advice. Past backtest performance does not guarantee future results. Always conduct your own due diligence.
