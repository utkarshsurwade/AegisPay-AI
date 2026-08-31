"""
AegisPay-AI: Co-Evolution Metrics Tracker (Pillar 4 - CLOSED LOOP)
Logs and computes mathematical metrics across Red-vs-Blue co-evolutionary generations.
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import numpy as np


@dataclass
class GenerationSnapshot:
    generation: int
    red_evasion_rate: float  # Fraction of attacks that bypassed defense (P(fraud) < 0.50)
    blue_robustness_score: float  # 1.0 - red_evasion_rate
    blue_roc_auc: float
    blue_pr_auc: float
    blue_f1: float
    false_positive_rate: float
    hard_adversarial_samples_discovered: int
    avg_inference_latency_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CoEvolutionMetricsTracker:
    """
    Maintains historical trajectory of the Red-vs-Blue arms race.
    """

    def __init__(self):
        self.snapshots: List[GenerationSnapshot] = []

    def record_generation(
        self,
        generation: int,
        red_evasion_rate: float,
        blue_roc_auc: float,
        blue_pr_auc: float,
        blue_f1: float,
        false_positive_rate: float,
        hard_samples_count: int,
        avg_latency_ms: float,
    ) -> GenerationSnapshot:
        robustness = float(np.clip(1.0 - red_evasion_rate, 0.0, 1.0))
        snap = GenerationSnapshot(
            generation=generation,
            red_evasion_rate=round(float(red_evasion_rate), 4),
            blue_robustness_score=round(robustness, 4),
            blue_roc_auc=round(float(blue_roc_auc), 4),
            blue_pr_auc=round(float(blue_pr_auc), 4),
            blue_f1=round(float(blue_f1), 4),
            false_positive_rate=round(float(false_positive_rate), 5),
            hard_adversarial_samples_discovered=hard_samples_count,
            avg_inference_latency_ms=round(float(avg_latency_ms), 2),
        )
        self.snapshots.append(snap)
        return snap

    def get_trajectory_summary(self) -> Dict[str, Any]:
        if not self.snapshots:
            return {"status": "NO_GENERATIONS_RECORDED"}

        init_snap = self.snapshots[0]
        final_snap = self.snapshots[-1]

        evasion_reduction_pct = (
            ((init_snap.red_evasion_rate - final_snap.red_evasion_rate) / max(1e-4, init_snap.red_evasion_rate)) * 100.0
        )
        robustness_gain_pct = (
            ((final_snap.blue_robustness_score - init_snap.blue_robustness_score) / max(1e-4, init_snap.blue_robustness_score)) * 100.0
        )

        return {
            "total_generations": len(self.snapshots),
            "initial_evasion_rate": init_snap.red_evasion_rate,
            "final_evasion_rate": final_snap.red_evasion_rate,
            "evasion_reduction_pct": round(evasion_reduction_pct, 2),
            "initial_robustness": init_snap.blue_robustness_score,
            "final_robustness": final_snap.blue_robustness_score,
            "robustness_gain_pct": round(robustness_gain_pct, 2),
            "final_roc_auc": final_snap.blue_roc_auc,
            "final_pr_auc": final_snap.blue_pr_auc,
            "final_fpr": final_snap.false_positive_rate,
            "snapshots": [s.to_dict() for s in self.snapshots],
        }
