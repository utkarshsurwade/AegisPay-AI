"""
AegisPay-AI: Red Team Module
Pillar 1 (Identify) & Pillar 2 (Generate)
"""
from .taxonomy import ThreatTaxonomy, AttackVector, AttackTier, PaymentRail, SeverityLevel
from .active_discovery import ActiveThreatDiscoveryEngine, DiscoveredThreatVector
from .live_threat_intel import LiveThreatIntelResearcher, ThreatIntelFeedItem
from .generator import SyntheticTransactionEngine, TransactionRecord
from .multi_agent_simulator import MultiAgentSwarmSimulator, SwarmCampaignResult
from .agentic_commerce_simulator import AgenticCommerceSimulator, AgenticProcurementTrace, AgentToolCall
from .payload_generator import PayloadGenerator
from .mutation_engine import AdversarialMutationEngine
from .rl_agent import ReinforcementLearningAttacker, EvasionAction

__all__ = [
    "ThreatTaxonomy",
    "AttackVector",
    "AttackTier",
    "PaymentRail",
    "SeverityLevel",
    "ActiveThreatDiscoveryEngine",
    "DiscoveredThreatVector",
    "LiveThreatIntelResearcher",
    "ThreatIntelFeedItem",
    "SyntheticTransactionEngine",
    "TransactionRecord",
    "MultiAgentSwarmSimulator",
    "SwarmCampaignResult",
    "AgenticCommerceSimulator",
    "AgenticProcurementTrace",
    "AgentToolCall",
    "PayloadGenerator",
    "AdversarialMutationEngine",
    "ReinforcementLearningAttacker",
    "EvasionAction",
]
