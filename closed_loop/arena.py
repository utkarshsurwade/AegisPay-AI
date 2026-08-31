"""
AegisPay-AI: Closed-Loop Co-Evolutionary Arena (Pillar 4 - CLOSED LOOP)
Orchestrates autonomous adversarial self-play between:
1. Learning Red Team RL Agent (Q-learning policy mutating features, pacing, topologies)
2. Learning Blue Team Adaptive Immune Defender (Online SGD, contrastive memory replay, dynamic thresholds)
"""
import time
from typing import List, Dict, Any, Tuple, Optional, Callable
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score

from red_team.generator import SyntheticTransactionEngine, TransactionRecord
from red_team.mutation_engine import AdversarialMutationEngine
from red_team.rl_agent import ReinforcementLearningAttacker
from blue_team.meta_classifier import MultiModalFusionEngine
from .metrics_tracker import CoEvolutionMetricsTracker, GenerationSnapshot


class ClosedLoopArena:
    """
    Executes iterative co-evolution where both Red Team and Blue Team learn simultaneously.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.tx_engine = SyntheticTransactionEngine(seed=seed)
        self.mutation_engine = AdversarialMutationEngine(seed=seed)
        self.rl_attacker = ReinforcementLearningAttacker(seed=seed)
        self.blue_engine = MultiModalFusionEngine()
        self.tracker = CoEvolutionMetricsTracker()

    def initialize_and_train_baseline(
        self,
        n_samples: int = 3000,
        fraud_ratio: float = 0.15
    ) -> Dict[str, Any]:
        """
        Initializes dataset (Generation 0) and trains initial Blue Team defense.
        """
        dataset = self.tx_engine.generate_dataset(
            n_samples=n_samples,
            fraud_ratio=fraud_ratio,
            stealth_distribution="mixed"
        )
        self.blue_engine.train_baseline(dataset)
        self.training_corpus: List[TransactionRecord] = list(dataset)

        # Baseline evaluation
        gen0_snap = self._evaluate_and_record(generation=0, test_pop_size=200)
        return {
            "status": "INITIALIZED",
            "generation_0": gen0_snap.to_dict(),
            "corpus_size": len(self.training_corpus)
        }

    def run_coevolution_loop(
        self,
        generations: int = 5,
        population_per_gen: int = 150,
        mutation_rate: float = 0.45,
        callback: Optional[Callable[[GenerationSnapshot], None]] = None
    ) -> Dict[str, Any]:
        """
        Runs multi-generation adversarial co-evolution with mutual learning.
        """
        if not hasattr(self, "training_corpus"):
            self.initialize_and_train_baseline()

        for gen in range(1, generations + 1):
            # -------------------------------------------------------------
            # 1. RED TEAM TURN: RL Policy Training & Mutation
            # -------------------------------------------------------------
            # Train RL Agent against current Blue Team for 20 episodes
            def blue_evaluator(tx: TransactionRecord):
                return self.blue_engine.evaluate_transaction(tx)

            rl_step_logs = self.rl_attacker.train_step(blue_evaluator, episodes=20, batch_size=15)

            # Sample past fraud transactions and apply learned RL policy + genetic mutation
            past_fraud = [t for t in self.training_corpus if t.is_fraud]
            candidate_pop = (
                self.mutation_engine.rng.sample(past_fraud, k=min(len(past_fraud), population_per_gen))
                if len(past_fraud) >= population_per_gen
                else past_fraud
            )

            # Evolve population
            evolved_attacks, history = self.mutation_engine.evolve_population(
                population=candidate_pop,
                blue_team_predictor=lambda tx: self.blue_engine.evaluate_transaction(tx).fused_risk_score,
                generations=3,
                pop_size=population_per_gen
            )

            # -------------------------------------------------------------
            # 2. IDENTIFY HARD ADVERSARIAL EVASIONS
            # -------------------------------------------------------------
            hard_adversarials: List[TransactionRecord] = []
            for atk in evolved_attacks:
                dec = self.blue_engine.evaluate_transaction(atk)
                if dec.fused_risk_score < 0.50:
                    hard_adversarials.append(atk)

            # -------------------------------------------------------------
            # 3. BLUE TEAM TURN: Online Adaptive Retraining & Immune Memory
            # -------------------------------------------------------------
            # Stream hard evasions through the Blue Team Adaptive Immune Defender
            for hard_tx in hard_adversarials:
                fv = self.blue_engine.feature_store.extract_features(hard_tx)
                dec = self.blue_engine.evaluate_transaction(hard_tx)
                self.blue_engine.adaptive_learner.observe_and_adapt(
                    tx=hard_tx,
                    fv=fv,
                    actual_is_fraud=True,
                    predicted_prob=dec.fused_risk_score
                )

            # Re-fold hard samples and fresh benign baselines into main corpus
            fresh_benign = [
                self.tx_engine.generate_benign_transaction()
                for _ in range(max(50, len(hard_adversarials) * 2))
            ]
            self.training_corpus.extend(hard_adversarials)
            self.training_corpus.extend(fresh_benign)

            # Full multi-modal ensemble retrain
            self.blue_engine.train_baseline(self.training_corpus)

            # -------------------------------------------------------------
            # 4. RECORD GENERATION METRICS
            # -------------------------------------------------------------
            snap = self._evaluate_and_record(generation=gen, test_pop_size=population_per_gen)
            if callback:
                callback(snap)

        trajectory = self.tracker.get_trajectory_summary()
        trajectory["rl_policy_summary"] = self.rl_attacker.get_learned_policy_summary()
        return trajectory

    def _evaluate_and_record(self, generation: int, test_pop_size: int = 150) -> GenerationSnapshot:
        """
        Evaluates current Blue Team on a fresh balanced test set.
        """
        test_benign = [self.tx_engine.generate_benign_transaction() for _ in range(test_pop_size)]
        test_fraud = [
            self.tx_engine.generate_adversarial_transaction(
                vector_id=self.tx_engine.rng.choice([
                    "ADV-01", "ADV-02", "ADV-05", "ADV-06", "ADV-09", "ADV-10",
                    "ADV-13", "ADV-14", "ADV-17", "ADV-18", "ADV-21", "ADV-24"
                ]),
                stealth_level=self.tx_engine.rng.uniform(0.35, 0.95)
            )
            for _ in range(test_pop_size)
        ]

        test_records = test_benign + test_fraud
        y_true = [0] * len(test_benign) + [1] * len(test_fraud)
        y_probs = []
        latencies = []
        evaded_attacks = 0

        for tx in test_records:
            t0 = time.perf_counter()
            dec = self.blue_engine.evaluate_transaction(tx)
            latencies.append((time.perf_counter() - t0) * 1000.0)
            prob = dec.fused_risk_score
            y_probs.append(prob)
            if tx.is_fraud and prob < 0.50:
                evaded_attacks += 1

        y_true = np.array(y_true)
        y_probs = np.array(y_probs)
        y_preds = (y_probs >= 0.50).astype(int)

        roc_auc = float(roc_auc_score(y_true, y_probs))
        pr_auc = float(average_precision_score(y_true, y_probs))
        f1 = float(f1_score(y_true, y_preds))

        fp = np.sum((y_preds == 1) & (y_true == 0))
        tn = np.sum((y_preds == 0) & (y_true == 0))
        fpr = float(fp / max(1, (fp + tn)))

        evasion_rate = float(evaded_attacks / len(test_fraud))

        return self.tracker.record_generation(
            generation=generation,
            red_evasion_rate=evasion_rate,
            blue_roc_auc=roc_auc,
            blue_pr_auc=pr_auc,
            blue_f1=f1,
            false_positive_rate=fpr,
            hard_samples_count=evaded_attacks,
            avg_latency_ms=float(np.mean(latencies))
        )
