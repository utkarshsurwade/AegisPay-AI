"""
AegisPay-AI: Bi-Directional Learning & Closed-Loop Coordinator (Pillar 4 - CLOSED LOOP)
Orchestrates continuous mutual reinforcement learning where:
1. Red Team learns from Blue Team defenses and evolves new bypasses.
2. Blue Team learns from Red Team attacks, patches decision boundaries, and updates immune memory.
3. Live Online Threat Intel feeds novel zero-day vectors into the Red Team.
4. Self-Auditing Gap Analyzer identifies blind spots in both attacks and defenses.
"""
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from red_team.taxonomy import ThreatTaxonomy
from red_team.live_threat_intel import LiveThreatIntelResearcher, ThreatIntelFeedItem
from red_team.rl_agent import ReinforcementLearningAttacker
from red_team.generator import SyntheticTransactionEngine, TransactionRecord
from blue_team.meta_classifier import MultiModalFusionEngine
from .gap_analyzer import SelfAuditingGapAnalyzer, SystemFlawReport


@dataclass
class BiDirectionalCycleResult:
    cycle_id: str
    timestamp: float
    threat_intel_ingested: int
    rl_episodes_trained: int
    blue_immune_updates_executed: int
    pre_cycle_evasion_rate: float
    post_cycle_evasion_rate: float
    flaws_identified_and_patched: int
    system_resilience_gain_pct: float
    gap_audit_report: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BiDirectionalLearningCoordinator:
    """
    Unified master coordinator realizing the complete closed-loop AI defense paradigm.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.intel_researcher = LiveThreatIntelResearcher(seed=seed)
        self.rl_attacker = ReinforcementLearningAttacker(seed=seed)
        self.tx_engine = SyntheticTransactionEngine(seed=seed)
        self.gap_analyzer = SelfAuditingGapAnalyzer(seed=seed)
        self.blue_engine = MultiModalFusionEngine()
        # Initialize baseline model
        init_data = self.tx_engine.generate_dataset(n_samples=600, fraud_ratio=0.15)
        self.blue_engine.train_baseline(init_data)
        self.cycle_history: List[BiDirectionalCycleResult] = []

    def execute_complete_bidirectional_cycle(
        self,
        episodes_per_cycle: int = 25
    ) -> BiDirectionalCycleResult:
        """
        Executes one full closed-loop co-evolutionary cycle across all 4 components.
        """
        cycle_id = f"CYCLE_BIO_{int(time.time())}"
        t_start = time.time()

        # -------------------------------------------------------------
        # STEP 1: Live Real-Time Threat Intelligence Ingestion
        # -------------------------------------------------------------
        intel_items = self.intel_researcher.fetch_live_threat_intel()

        # -------------------------------------------------------------
        # STEP 2: Pre-Cycle Baseline Resilience Assessment
        # -------------------------------------------------------------
        pre_audit = self.gap_analyzer.audit_system_flaws_and_gaps(self.blue_engine, sample_probes_per_vector=15)
        pre_evasion_rate = 1.0 - pre_audit.overall_system_resilience_score

        # -------------------------------------------------------------
        # STEP 3: Red Team RL Training & Policy Adaptation
        # -------------------------------------------------------------
        def blue_evaluator(tx: TransactionRecord):
            return self.blue_engine.evaluate_transaction(tx)

        rl_logs = self.rl_attacker.train_step(
            blue_team_evaluator=blue_evaluator,
            episodes=episodes_per_cycle,
            batch_size=12
        )

        # -------------------------------------------------------------
        # STEP 4: Blue Team Online Adaptive Immune Defense Retraining
        # -------------------------------------------------------------
        # Generate targeted attacks based on discovered blind spots
        flaws_patched = 0
        for blind_spot in pre_audit.decision_boundary_blind_spots[:4]:
            vec_id = blind_spot["vector_id"]
            # Generate hard adversarial attacks on this blind spot
            for _ in range(20):
                hard_tx = self.tx_engine.generate_adversarial_transaction(
                    vector_id=vec_id,
                    stealth_level=0.88
                )
                fv = self.blue_engine.feature_store.extract_features(hard_tx)
                dec = self.blue_engine.evaluate_transaction(hard_tx)

                # Blue Team learns from this attack and adapts weights
                self.blue_engine.adaptive_learner.observe_and_adapt(
                    tx=hard_tx,
                    fv=fv,
                    actual_is_fraud=True,
                    predicted_prob=dec.fused_risk_score
                )
                flaws_patched += 1

        # -------------------------------------------------------------
        # STEP 5: Post-Cycle Gap & Resilience Audit
        # -------------------------------------------------------------
        post_audit = self.gap_analyzer.audit_system_flaws_and_gaps(self.blue_engine, sample_probes_per_vector=15)
        post_evasion_rate = 1.0 - post_audit.overall_system_resilience_score

        resilience_gain = (
            ((post_audit.overall_system_resilience_score - pre_audit.overall_system_resilience_score) / max(1e-4, pre_audit.overall_system_resilience_score)) * 100.0
        )

        result = BiDirectionalCycleResult(
            cycle_id=cycle_id,
            timestamp=t_start,
            threat_intel_ingested=len(intel_items),
            rl_episodes_trained=episodes_per_cycle,
            blue_immune_updates_executed=flaws_patched,
            pre_cycle_evasion_rate=round(float(pre_evasion_rate), 4),
            post_cycle_evasion_rate=round(float(post_evasion_rate), 4),
            flaws_identified_and_patched=flaws_patched,
            system_resilience_gain_pct=round(float(resilience_gain), 2),
            gap_audit_report=post_audit.to_dict()
        )

        self.cycle_history.append(result)
        return result
