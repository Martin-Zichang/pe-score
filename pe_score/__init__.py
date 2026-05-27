"""
PE-Score: Data-driven PE investment scoring framework
7 dimensions, 35 sub-indicators, backtested on 31 cases (ρ=0.864)
"""

__version__ = "0.1.0"

from .dimensions import DIMENSIONS, DIM_NAMES, SUB_NAMES
from .scorer import PEScorer
from .weights import STAGE_WEIGHTS

__all__ = ["DIMENSIONS", "DIM_NAMES", "SUB_NAMES", "PEScorer", "STAGE_WEIGHTS"]
