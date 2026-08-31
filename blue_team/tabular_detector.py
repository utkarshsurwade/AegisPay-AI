"""
AegisPay-AI: Tabular Risk Detector (Pillar 3 - DEFEND Level 1)
Optimized tree-based ensemble classifier with feature attribution (<5ms inference).
"""
import time
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score

from .feature_store import FeatureVector


class TabularRiskDetector:
    """
    Fast-path tabular classifier scoring transactional velocity, amounts, and metadata.
    """

    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.08,
            max_depth=5,
            subsample=0.85,
            random_state=42,
        )
        self.is_trained = False
        self.feature_names = FeatureVector.get_feature_names()

    def train(self, feature_vectors: List[FeatureVector], labels: List[bool]) -> Dict[str, float]:
        """
        Trains the gradient boosting model on extracted feature vectors.
        """
        X = np.vstack([fv.to_array() for fv in feature_vectors])
        y = np.array(labels, dtype=np.int32)

        start_t = time.time()
        self.model.fit(X, y)
        train_time = time.time() - start_t

        self.is_trained = True
        probs = self.model.predict_proba(X)[:, 1]
        preds = (probs >= 0.5).astype(int)

        roc_auc = float(roc_auc_score(y, probs))
        pr_auc = float(average_precision_score(y, probs))
        f1 = float(f1_score(y, preds))

        return {
            "train_time_sec": round(train_time, 3),
            "train_roc_auc": round(roc_auc, 4),
            "train_pr_auc": round(pr_auc, 4),
            "train_f1": round(f1, 4),
            "sample_count": len(labels),
        }

    def predict_proba(self, feature_vector: FeatureVector) -> float:
        """
        Predicts fraud probability in sub-millisecond time.
        """
        if not self.is_trained:
            # Fallback heuristic if not yet fitted
            return 0.5

        x = feature_vector.to_array().reshape(1, -1)
        prob = float(self.model.predict_proba(x)[0, 1])
        return prob

    def get_feature_importances(self) -> Dict[str, float]:
        """
        Returns normalized feature importances.
        """
        if not self.is_trained:
            return {f: 1.0 / len(self.feature_names) for f in self.feature_names}

        importances = self.model.feature_importances_
        return {
            name: round(float(imp), 4)
            for name, imp in zip(self.feature_names, importances)
        }

    def explain_prediction(self, feature_vector: FeatureVector) -> List[Dict[str, Any]]:
        """
        Provides tree-based feature contribution breakdown (SHAP approximation).
        """
        x = feature_vector.to_array()
        importances = self.model.feature_importances_ if self.is_trained else np.ones(len(x))

        contributions = []
        for name, val, imp in zip(self.feature_names, x, importances):
            # Contribution proxy: (feature_value_scaled * feature_importance)
            contrib = float(val * imp)
            contributions.append({
                "feature": name,
                "value": round(float(val), 2),
                "importance": round(float(imp), 4),
                "contribution": round(contrib, 4)
            })

        contributions.sort(key=lambda c: abs(c["contribution"]), reverse=True)
        return contributions[:8]
