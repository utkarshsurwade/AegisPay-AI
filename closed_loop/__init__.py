"""
AegisPay-AI: Closed-Loop Co-Evolution Module
Pillar 4 - Red vs. Blue Adversarial Self-Play, System Gap Auditing, and Mutual Learning
"""
from .metrics_tracker import CoEvolutionMetricsTracker, GenerationSnapshot
from .arena import ClosedLoopArena
from .gap_analyzer import SelfAuditingGapAnalyzer, SystemFlawReport
from .bidirectional_learner import BiDirectionalLearningCoordinator, BiDirectionalCycleResult

__all__ = [
    "CoEvolutionMetricsTracker",
    "GenerationSnapshot",
    "ClosedLoopArena",
    "SelfAuditingGapAnalyzer",
    "SystemFlawReport",
    "BiDirectionalLearningCoordinator",
    "BiDirectionalCycleResult",
]
