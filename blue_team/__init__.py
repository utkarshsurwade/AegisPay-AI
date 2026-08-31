"""
AegisPay-AI: Blue Team Module
Pillar 3 (Defend) - Real-Time Multi-Modal Detection & Continuous Adaptive Immune Learning (<30ms)
"""
from .feature_store import RealTimeFeatureStore, FeatureVector
from .tabular_detector import TabularRiskDetector
from .behavioral_detector import BehavioralBiometricsDetector
from .gnn_detector import GraphTopologyDetector
from .semantic_guardrail import SemanticGuardrailDetector
from .adaptive_learner import AdaptiveImmuneDefender, AdaptiveImmuneState
from .meta_classifier import MultiModalFusionEngine, DetectionDecision, DecisionAction
from .explainability import ExplainabilityEngine, SuspiciousActivityReport

__all__ = [
    "RealTimeFeatureStore",
    "FeatureVector",
    "TabularRiskDetector",
    "BehavioralBiometricsDetector",
    "GraphTopologyDetector",
    "SemanticGuardrailDetector",
    "AdaptiveImmuneDefender",
    "AdaptiveImmuneState",
    "MultiModalFusionEngine",
    "DetectionDecision",
    "DecisionAction",
    "ExplainabilityEngine",
    "SuspiciousActivityReport",
]
