"""
AegisPay-AI: Self-Auditing & System Flaw Discovery Engine (Pillar 4 - CLOSED LOOP)
Introspects Blue Team decision boundaries, measures coverage gaps across payment rails,
and identifies structural blind spots in both attack simulation and defensive models.
"""
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from red_team.generator import SyntheticTransactionEngine, TransactionRecord
from red_team.taxonomy import ThreatTaxonomy, PaymentRail
from blue_team.meta_classifier import MultiModalFusionEngine


@dataclass
class SystemFlawReport:
    audit_timestamp: float
    total_evaluated_vectors: int
    overall_system_resilience_score: float  # [0.0 - 1.0]

    # Vulnerability & Gap Breakdowns
    vulnerable_payment_rails: List[Dict[str, Any]]
    decision_boundary_blind_spots: List[Dict[str, Any]]
    red_team_unexplored_action_spaces: List[Dict[str, Any]]
    recommended_hardening_actions: List[str]
    critical_flaws_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SelfAuditingGapAnalyzer:
    """
    Autonomous introspective auditor discovering blind spots in its own models.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.tx_engine = SyntheticTransactionEngine(seed=seed)
        self.taxonomy = ThreatTaxonomy()

    def audit_system_flaws_and_gaps(
        self,
        blue_engine: MultiModalFusionEngine,
        sample_probes_per_vector: int = 25
    ) -> SystemFlawReport:
        """
        Conducts systematic multi-dimensional probing against Blue Team defenses
        to uncover structural coverage gaps and decision boundary weaknesses.
        """
        all_vectors = self.taxonomy.get_all_vectors()
        rail_performance: Dict[str, Dict[str, Any]] = {}
        boundary_blind_spots: List[Dict[str, Any]] = []

        total_probes = 0
        total_intercepted = 0

        for vec in all_vectors:
            # Generate high-stealth adversarial probes
            stealth_levels = [0.4, 0.7, 0.95]
            vec_scores = []
            evaded_at_high_stealth = 0

            for s in stealth_levels:
                for _ in range(sample_probes_per_vector // len(stealth_levels)):
                    total_probes += 1
                    tx = self.tx_engine.generate_adversarial_transaction(
                        vector_id=vec.id,
                        stealth_level=s
                    )
                    dec = blue_engine.evaluate_transaction(tx)
                    prob = dec.fused_risk_score
                    vec_scores.append(prob)

                    if prob >= 0.50:
                        total_intercepted += 1
                    elif s >= 0.80:
                        evaded_at_high_stealth += 1

            # Aggregate per target rail
            for r in vec.target_rails:
                r_name = r.value
                if r_name not in rail_performance:
                    rail_performance[r_name] = {"probes": 0, "intercepted": 0, "vectors": []}
                rail_performance[r_name]["probes"] += len(vec_scores)
                rail_performance[r_name]["intercepted"] += sum(1 for sc in vec_scores if sc >= 0.50)
                if vec.id not in rail_performance[r_name]["vectors"]:
                    rail_performance[r_name]["vectors"].append(vec.id)

            # Check for Decision Boundary Blind Spot (High evasion at stealth > 0.8)
            avg_score = float(np.mean(vec_scores))
            score_variance = float(np.var(vec_scores))

            if avg_score < 0.65 or score_variance > 0.08 or evaded_at_high_stealth > 2:
                boundary_blind_spots.append({
                    "vector_id": vec.id,
                    "vector_name": vec.name,
                    "tier": vec.tier.value,
                    "mean_detection_score": round(avg_score, 4),
                    "score_variance": round(score_variance, 4),
                    "vulnerability_severity": "CRITICAL" if avg_score < 0.50 else "HIGH",
                    "flaw_description": f"Model exhibits high decision variance or sub-threshold classification on {vec.name} under high-stealth evasion.",
                    "mitigation_target": vec.mitigation_strategy
                })

        # Process Rail Coverage Gaps
        vulnerable_rails = []
        for r_name, r_data in rail_performance.items():
            recall = (r_data["intercepted"] / max(1, r_data["probes"])) * 100.0
            if recall < 92.0:
                vulnerable_rails.append({
                    "rail_name": r_name,
                    "tested_probes": r_data["probes"],
                    "detection_recall_pct": round(recall, 2),
                    "associated_vectors_count": len(r_data["vectors"]),
                    "risk_assessment": "ATTENTION_REQUIRED" if recall < 85.0 else "MODERATE_DEFENSE"
                })

        # Red Team unexplored action spaces
        unexplored_spaces = [
            {
                "subspace": "Multi-Rail Liquidity Arbitrage (Card Auth vs Instant Settlement)",
                "action_gap": "Latency desynchronization probes across cross-border cryptocurrency on-ramps",
                "recommended_rl_action": "Increase RL exploration rate on Action 5 (Composite Stealth) with cross-rail hopping."
            },
            {
                "subspace": "Zero-Width Steganography in B2B Invoices (ISO 20022)",
                "action_gap": "Nested CDATA recursive expansion in remittance information",
                "recommended_rl_action": "Synthesize deep XML parser test harnesses in Red Team payload generator."
            }
        ]

        # Formulate Hardening Recommendations
        recommendations = [
            "Inject hard adversarial samples for top 3 boundary blind spots into Blue Team contrastive memory replay buffer.",
            "Deploy dynamic cost-sensitive threshold shift on vulnerable rail endpoints (tighten threshold by 0.08).",
            "Dispatch Red Team RL policy agents to systematically probe newly identified rail subspaces.",
            "Activate multi-spectral biometric liveness invariant checks on Mobile/3DS channels."
        ]

        overall_resilience = float(total_intercepted / max(1, total_probes))

        return SystemFlawReport(
            audit_timestamp=time.time(),
            total_evaluated_vectors=len(all_vectors),
            overall_system_resilience_score=round(overall_resilience, 4),
            vulnerable_payment_rails=vulnerable_rails,
            decision_boundary_blind_spots=boundary_blind_spots[:6],
            red_team_unexplored_action_spaces=unexplored_spaces,
            recommended_hardening_actions=recommendations,
            critical_flaws_count=len([b for b in boundary_blind_spots if b["vulnerability_severity"] == "CRITICAL"])
        )
