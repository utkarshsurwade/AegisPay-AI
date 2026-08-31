"""
AegisPay-AI: Continuous Adaptive Learning & Immune Defense Engine (Pillar 3 - DEFEND)
Implements online streaming learning, adversarial contrastive memory replay,
and dynamic cost-sensitive threshold adaptation to evolve defenses after every transaction.
"""
import time
from collections import deque
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import roc_auc_score, f1_score

from red_team.generator import TransactionRecord
from .feature_store import RealTimeFeatureStore, FeatureVector


@dataclass
class AdaptiveImmuneState:
    learning_iteration: int
    memory_buffer_size: int
    current_threshold_approve: float
    current_threshold_alert: float
    current_threshold_decline: float
    online_loss: float
    recent_accuracy: float
    recent_fpr: float
    recent_fnr: float
    active_immune_updates_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AdaptiveImmuneDefender:
    """
    Continuous online learning engine that dynamically hardens decision boundaries
    using contrastive memory replay and cost-sensitive threshold adaptation.
    """

    def __init__(
        self,
        memory_capacity: int = 2000,
        learning_rate: float = 0.05,
        cost_fp_usd: float = 15.0,   # Friction & lost interchange cost
        cost_fn_ratio: float = 1.0,  # Fraud loss = full transaction amount
        seed: int = 42
    ):
        self.memory_capacity = memory_capacity
        self.learning_rate = learning_rate
        self.cost_fp_usd = cost_fp_usd
        self.cost_fn_ratio = cost_fn_ratio
        self.rng = np.random.RandomState(seed)

        # Contrastive Memory Buffer for hard adversarial samples
        self.memory_buffer: deque = deque(maxlen=memory_capacity)

        # Online Streaming Classifier (Incremental SGD with Log Loss)
        self.online_model = SGDClassifier(
            loss="log_loss",
            penalty="l2",
            alpha=0.0001,
            learning_rate="adaptive",
            eta0=learning_rate,
            random_state=seed
        )
        self.is_initialized = False

        # Dynamic Thresholds
        self.th_approve = 0.30
        self.th_alert = 0.70
        self.th_decline = 0.88

        # Telemetry stats
        self.iteration = 0
        self.immune_updates_count = 0
        self.recent_eval_window: deque = deque(maxlen=100)

    def initialize_with_baseline(self, feature_vectors: List[FeatureVector], labels: List[bool]):
        """Initializes online weights on baseline training corpus."""
        X = np.vstack([fv.to_array() for fv in feature_vectors])
        y = np.array(labels, dtype=np.int32)
        classes = np.array([0, 1])

        self.online_model.partial_fit(X, y, classes=classes)
        self.is_initialized = True

        for fv, lab in zip(feature_vectors, labels):
            self.memory_buffer.append((fv.to_array(), int(lab)))

    def predict_online_prob(self, fv: FeatureVector) -> float:
        """Outputs calibrated online probability score."""
        if not self.is_initialized:
            return 0.50
        x = fv.to_array().reshape(1, -1)
        prob = float(self.online_model.predict_proba(x)[0, 1])
        return prob

    def observe_and_adapt(
        self,
        tx: TransactionRecord,
        fv: FeatureVector,
        actual_is_fraud: bool,
        predicted_prob: float
    ) -> AdaptiveImmuneState:
        """
        Executes online continuous learning step after observing a transaction outcome.
        """
        self.iteration += 1
        x = fv.to_array()
        y = 1 if actual_is_fraud else 0

        # Log prediction result (True Positive, False Positive, etc.)
        pred_label = 1 if predicted_prob >= self.th_alert else 0
        is_error = (pred_label != y)
        self.recent_eval_window.append((y, predicted_prob, is_error))

        # If model made an error or sample was a hard adversarial borderline case (0.35 < prob < 0.65)
        # We store it into the contrastive replay buffer
        if is_error or (0.35 <= predicted_prob <= 0.65):
            self.memory_buffer.append((x, y))

        # Perform incremental contrastive batch replay update
        if len(self.memory_buffer) >= 20 and (self.iteration % 5 == 0):
            # Sample balanced batch from memory buffer
            batch_indices = self.rng.choice(len(self.memory_buffer), size=min(32, len(self.memory_buffer)), replace=False)
            batch_x = np.array([self.memory_buffer[i][0] for i in batch_indices])
            batch_y = np.array([self.memory_buffer[i][1] for i in batch_indices])

            if not self.is_initialized:
                self.online_model.partial_fit(batch_x, batch_y, classes=np.array([0, 1]))
                self.is_initialized = True
            else:
                self.online_model.partial_fit(batch_x, batch_y)
            self.immune_updates_count += 1

            # Periodically adapt cost-sensitive thresholds
            self._adapt_thresholds()

        # Compute rolling window metrics
        recent_y = [item[0] for item in self.recent_eval_window]
        recent_prob = [item[1] for item in self.recent_eval_window]
        recent_preds = [1 if p >= self.th_alert else 0 for p in recent_prob]

        acc = float(np.mean([1 if yp == y else 0 for yp, y in zip(recent_preds, recent_y)])) if recent_y else 1.0
        fp = sum(1 for yp, y in zip(recent_preds, recent_y) if yp == 1 and y == 0)
        tn = sum(1 for yp, y in zip(recent_preds, recent_y) if yp == 0 and y == 0)
        fn = sum(1 for yp, y in zip(recent_preds, recent_y) if yp == 0 and y == 1)
        tp = sum(1 for yp, y in zip(recent_preds, recent_y) if yp == 1 and y == 1)

        fpr = float(fp / max(1, fp + tn))
        fnr = float(fn / max(1, fn + tp))

        return AdaptiveImmuneState(
            learning_iteration=self.iteration,
            memory_buffer_size=len(self.memory_buffer),
            current_threshold_approve=round(self.th_approve, 3),
            current_threshold_alert=round(self.th_alert, 3),
            current_threshold_decline=round(self.th_decline, 3),
            online_loss=round(float(1.0 - acc), 4),
            recent_accuracy=round(acc, 4),
            recent_fpr=round(fpr, 4),
            recent_fnr=round(fnr, 4),
            active_immune_updates_count=self.immune_updates_count
        )

    def _adapt_thresholds(self):
        """
        Dynamically adjusts decision cutoffs based on observed false-positive vs false-negative economic losses.
        """
        if len(self.recent_eval_window) < 30:
            return

        recent_y = [item[0] for item in self.recent_eval_window]
        recent_prob = [item[1] for item in self.recent_eval_window]

        # Scan candidate thresholds in [0.40, 0.85]
        best_th = self.th_alert
        min_loss = float("inf")

        for cand_th in np.linspace(0.40, 0.85, 10):
            fp_cost = sum(self.cost_fp_usd for p, y in zip(recent_prob, recent_y) if p >= cand_th and y == 0)
            fn_cost = sum(500.0 * self.cost_fn_ratio for p, y in zip(recent_prob, recent_y) if p < cand_th and y == 1)
            total_loss = fp_cost + fn_cost

            if total_loss < min_loss:
                min_loss = total_loss
                best_th = cand_th

        # Smooth update
        self.th_alert = float(0.85 * self.th_alert + 0.15 * best_th)
        self.th_approve = max(0.20, self.th_alert - 0.40)
        self.th_decline = min(0.95, self.th_alert + 0.18)
