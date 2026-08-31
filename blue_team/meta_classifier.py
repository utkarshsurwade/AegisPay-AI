"""
AegisPay-AI: Multi-Modal Fusion Engine & Decision Policy (Pillar 3 - DEFEND)
Combines Tabular, Behavioral, Graph, and Semantic signals into a unified risk score (<25ms).
Implements the 4-tier Mastercard Decision Matrix: APPROVE, STEP_UP_3DS, ALERT_ANALYST, HARD_DECLINE.
"""
import time
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from red_team.generator import TransactionRecord
from .feature_store import RealTimeFeatureStore, FeatureVector
from .tabular_detector import TabularRiskDetector
from .behavioral_detector import BehavioralBiometricsDetector
from .gnn_detector import GraphTopologyDetector
from .semantic_guardrail import SemanticGuardrailDetector
from .adaptive_learner import AdaptiveImmuneDefender, AdaptiveImmuneState


class DecisionAction(str, Enum):
    APPROVE = "APPROVE (Low Risk - Seamless Auth)"
    STEP_UP_3DS = "STEP_UP_3DS (Medium Risk - Dynamic Biometric Challenge)"
    ALERT_ANALYST = "ALERT_ANALYST (High Risk - Queued for SAR Investigation)"
    HARD_DECLINE = "HARD_DECLINE (Critical Risk - Immediate Authorization Intercept)"


@dataclass
class DetectionDecision:
    tx_id: str
    timestamp: float
    account_id: str
    merchant_id: str
    amount: float
    payment_rail: str

    # Component Risk Scores
    tabular_risk_score: float
    behavioral_risk_score: float
    graph_topology_risk_score: float
    semantic_risk_score: float

    # Unified Ensemble Score
    fused_risk_score: float
    action: DecisionAction
    latency_ms: float

    # Explanations & Signals
    primary_risk_factor: str
    contributing_signals: List[str]
    rule_overrides: List[str]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["action"] = self.action.value
        return d


class MultiModalFusionEngine:
    """
    Unified multi-modal decision intelligence engine.
    """

    def __init__(
        self,
        weights: Tuple[float, float, float, float] = (0.40, 0.25, 0.20, 0.15),
        threshold_step_up: float = 0.30,
        threshold_alert: float = 0.70,
        threshold_decline: float = 0.88,
    ):
        self.w_tab, self.w_bio, self.w_graph, self.w_nlp = weights
        self.th_step_up = threshold_step_up
        self.th_alert = threshold_alert
        self.th_decline = threshold_decline

        # Initialize sub-modules
        self.feature_store = RealTimeFeatureStore()
        self.tabular_detector = TabularRiskDetector()
        self.behavioral_detector = BehavioralBiometricsDetector()
        self.gnn_detector = GraphTopologyDetector()
        self.semantic_guardrail = SemanticGuardrailDetector()
        self.adaptive_learner = AdaptiveImmuneDefender()

    def train_baseline(self, dataset: List[TransactionRecord]):
        """
        Fits all sub-detectors on training dataset.
        """
        benign = [t for t in dataset if not t.is_fraud]
        feature_vectors = []
        labels = []

        for tx in dataset:
            fv = self.feature_store.extract_features(tx)
            feature_vectors.append(fv)
            labels.append(tx.is_fraud)

        # Train tabular model
        self.tabular_detector.train(feature_vectors, labels)
        # Fit behavioral baseline
        self.behavioral_detector.fit_baseline(benign)
        # Initialize online adaptive learner
        self.adaptive_learner.initialize_with_baseline(feature_vectors, labels)

    def evaluate_transaction(self, tx: TransactionRecord) -> DetectionDecision:
        """
        Evaluates an incoming payment transaction across all 4 levels in real-time.
        """
        start_t = time.perf_counter()

        # Level 1: Feature Extraction & Tabular Risk
        fv = self.feature_store.extract_features(tx)
        s_tab = self.tabular_detector.predict_proba(fv)

        # Level 2: Behavioral Biometrics
        bio_res = self.behavioral_detector.predict_anomaly_score(tx)
        s_bio = bio_res["behavioral_risk_score"]

        # Level 3: Graph Topology
        graph_res = self.gnn_detector.score_ego_subgraph(tx)
        s_graph = graph_res["graph_topology_risk"]

        # Level 4: Semantic Guardrail
        nlp_res = self.semantic_guardrail.inspect_payload(tx)
        s_nlp = nlp_res["semantic_risk_score"]

        # Rule Overrides (Zero-Tolerance Critical Vectors)
        overrides = []
        if nlp_res["payload_compromised"]:
            overrides.append("CRITICAL: Malicious Prompt Injection / XML Exploit Detected")
        if bio_res.get("is_synthetic_telemetry") and tx.amount > 3000.0:
            overrides.append("HIGH: Synthetic Biometric Spoof on High-Value Transaction")
        if graph_res.get("smurfing_signature_detected"):
            overrides.append("HIGH: Coordinated Multi-Hop Smurfing Flow Detected")

        # Compute Fused Multi-Modal Risk Score
        raw_fused = (
            self.w_tab * s_tab +
            self.w_bio * s_bio +
            self.w_graph * s_graph +
            self.w_nlp * s_nlp
        )

        if overrides:
            raw_fused = max(raw_fused, 0.92)

        fused_score = float(np.clip(raw_fused, 0.0, 1.0))

        # Dynamic Action Policy Mapping
        if fused_score < self.th_step_up:
            action = DecisionAction.APPROVE
        elif fused_score < self.th_alert:
            action = DecisionAction.STEP_UP_3DS
        elif fused_score < self.th_decline:
            action = DecisionAction.ALERT_ANALYST
        else:
            action = DecisionAction.HARD_DECLINE

        # Measure elapsed latency in milliseconds
        latency_ms = (time.perf_counter() - start_t) * 1000.0

        # Synthesize top signals
        signals = []
        signals.extend(bio_res.get("anomaly_reasons", []))
        signals.extend(graph_res.get("subgraph_motifs", []))
        if nlp_res.get("detected_injection_tokens"):
            signals.append(f"Prompt Injection: {nlp_res['detected_injection_tokens'][0]}")

        # Primary risk factor attribution
        scores = [("Tabular / Velocity", s_tab), ("Behavioral Biometrics", s_bio), ("Graph Topology", s_graph), ("Semantic Guardrail", s_nlp)]
        scores.sort(key=lambda x: x[1], reverse=True)
        primary_factor = f"{scores[0][0]} (Score: {scores[0][1]:.2f})"

        return DetectionDecision(
            tx_id=tx.tx_id,
            timestamp=tx.timestamp,
            account_id=tx.account_id,
            merchant_id=tx.merchant_id,
            amount=tx.amount,
            payment_rail=tx.payment_rail,
            tabular_risk_score=round(s_tab, 4),
            behavioral_risk_score=round(s_bio, 4),
            graph_topology_risk_score=round(s_graph, 4),
            semantic_risk_score=round(s_nlp, 4),
            fused_risk_score=round(fused_score, 4),
            action=action,
            latency_ms=round(latency_ms, 2),
            primary_risk_factor=primary_factor,
            contributing_signals=signals[:5],
            rule_overrides=overrides,
        )
