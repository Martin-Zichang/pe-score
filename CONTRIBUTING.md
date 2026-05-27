# Contributing to PE-Score

Thank you for your interest in contributing!

## Ways to Contribute

### 1. Add Backtest Cases

The most valuable contribution. Add your own PE/VC case data to improve the model's predictive power.

**Format**: Add a new case to `pe_score/backtest_cases.py`:

```python
cases.append(("项目名称", "early", 15.0, [
    5,2,2,3,4,  # 团队
    5,3,4,3,2,  # 市场
    5,3,3,2,4,  # 技术
    1,2,1,1,2,  # 财务
    4,4,4,3,4,  # 退出
    5,4,5,5,4,  # 政策
    4,5,4,4,4,  # 催化剂
]))
```

Requirements:
- Return multiple must be verifiable (IPO, acquisition, or confirmed write-off)
- Scores must be based on information available **at the time of investment**, not retrospectively
- Include the investment year and sector

### 2. Industry-Specific Weights

If you have domain expertise in a specific industry, propose weight adjustments with justification.

### 3. Bug Reports & Feature Requests

Open an issue with:
- Clear description
- Steps to reproduce (for bugs)
- Expected vs. actual behavior

### 4. Code Contributions

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest`)
5. Submit a pull request

## Development Setup

```bash
git clone https://github.com/<your-username>/pe-score.git
cd pe-score
pip install -e ".[dev]"
pytest
```

## Code Style

- Python 3.8+ compatible
- Follow PEP 8
- Add docstrings to public functions
- Keep dependencies minimal

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
