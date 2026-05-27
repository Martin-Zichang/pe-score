"""Tests for pe_score package."""

import pytest
from pe_score import PEScorer, DIMENSIONS, DIM_NAMES, SUB_NAMES, STAGE_WEIGHTS
from pe_score.weights import get_grade


class TestDimensions:
    def test_seven_dimensions(self):
        assert len(DIMENSIONS) == 7

    def test_five_subs_per_dim(self):
        for dim, subs in DIMENSIONS.items():
            assert len(subs) == 5, f"{dim} has {len(subs)} subs, expected 5"

    def test_total_35_sub_indicators(self):
        assert len(SUB_NAMES) == 35


class TestScorer:
    def setup_method(self):
        self.scorer = PEScorer()
        # 宁德时代A轮（来自回测数据，已知回报500x，评分最高）
        self.catl_scores = [
            5,5,5,4,2,  # 团队
            5,5,5,5,4,  # 市场
            5,5,5,5,5,  # 技术
            5,5,5,5,4,  # 财务
            5,5,5,5,5,  # 退出
            5,5,5,5,5,  # 政策
            5,5,5,5,5,  # 催化剂
        ]

    def test_score_returns_result(self):
        result = self.scorer.score("宁德时代", "early", self.catl_scores)
        assert result.name == "宁德时代"
        assert result.stage == "early"
        assert result.grade == "A"

    def test_composite_in_range(self):
        result = self.scorer.score("宁德时代", "early", self.catl_scores)
        assert 1.0 <= result.composite <= 5.0

    def test_invalid_score_count(self):
        with pytest.raises(ValueError, match="35"):
            self.scorer.score("test", "early", [3] * 34)

    def test_invalid_score_range(self):
        with pytest.raises(ValueError, match="1-5"):
            self.scorer.score("test", "early", [3] * 34 + [6])

    def test_simplified_scoring(self):
        result = self.scorer.score_from_dict("test", "early", {
            "团队": 3.0, "市场": 4.0, "技术": 4.0,
            "财务": 2.0, "退出": 3.5, "政策": 3.0, "催化剂": 3.5
        })
        assert result.composite > 0
        assert result.grade in ("A", "B", "C", "D")

    def test_compare(self):
        r1 = self.scorer.score_from_dict("A", "early", {
            "团队": 4, "市场": 4, "技术": 4, "财务": 3, "退出": 4, "政策": 4, "催化剂": 4
        })
        r2 = self.scorer.score_from_dict("B", "early", {
            "团队": 2, "市场": 2, "技术": 2, "财务": 2, "退出": 2, "政策": 2, "催化剂": 2
        })
        comp = self.scorer.compare([r1, r2])
        assert comp["best"] == "A"

    def test_to_dict(self):
        result = self.scorer.score("test", "early", [3]*35)
        d = result.to_dict()
        assert "name" in d
        assert "composite" in d
        assert "grade" in d


class TestGrading:
    def test_a_grade(self):
        assert get_grade(4.5) == "A"

    def test_b_grade(self):
        assert get_grade(3.5) == "B"

    def test_c_grade(self):
        assert get_grade(2.5) == "C"

    def test_d_grade(self):
        assert get_grade(1.5) == "D"

    def test_boundary(self):
        assert get_grade(4.0) == "A"
        assert get_grade(3.0) == "B"
        assert get_grade(2.0) == "C"
