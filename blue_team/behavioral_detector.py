"""
AegisPay-AI: Behavioral Biometrics & Telemetry Detector (Pillar 3 - DEFEND Level 2)
Detects synthetic keystroke dynamics, touchscreen jitter anomalies, and biometric deepfakes (<8ms).
"""
from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.ensemble import IsolationForest

from red_team.generator import TransactionRecord


class BehavioralBiometricsDetector:
    """
    Evaluates human-interaction authenticity vs. bot/GAN mimicry.
    """

    def __init__(self):
        # Baseline human empirical constants
        self.mean_hold = 95.0
        self.std_hold = 12.0
        self.mean_flight = 145.0
        self.std_flight = 25.0
        self.mean_entropy = 0.88
        self.std_entropy = 0.06

        # Isolation model for high-dimensional telemetry
        self.iso_model = IsolationForest(
            n_estimators=50,
            contamination=0.1,
            random_state=42
        )
        self.is_fitted = False

    def fit_baseline(self, benign_records: List[TransactionRecord]):
        """
        Fits the unsupervised isolation forest on genuine human interaction profiles.
        """
        X = []
        for r in benign_records:
            X.append([
                r.keystroke_hold_time_ms,
                r.keystroke_flight_time_ms,
                r.touch_pressure,
                r.touch_motion_speed,
                r.sensor_entropy,
                r.biometric_liveness_score
            ])
        if len(X) > 10:
            self.iso_model.fit(np.array(X))
            self.is_fitted = True

    def predict_anomaly_score(self, tx: TransactionRecord) -> Dict[str, Any]:
        """
        Computes behavioral anomaly score [0.0 - 1.0].
        """
        # 1. Statistical Z-scores
        z_hold = abs(tx.keystroke_hold_time_ms - self.mean_hold) / self.std_hold
        z_flight = abs(tx.keystroke_flight_time_ms - self.mean_flight) / self.std_flight
        z_entropy = max(0.0, (self.mean_entropy - tx.sensor_entropy) / self.std_entropy)

        # 2. Heuristic indicators of synthetic/bot activity
        is_bot_speed = 1.0 if (tx.keystroke_hold_time_ms < 35.0 or tx.keystroke_flight_time_ms < 30.0) else 0.0
        is_deepfake = 1.0 if (tx.biometric_liveness_score < 0.60) else 0.0
        is_flatline_sensor = 1.0 if (tx.sensor_entropy < 0.30) else 0.0

        # 3. Isolation Forest scoring if fitted
        if self.is_fitted:
            x_vec = np.array([[
                tx.keystroke_hold_time_ms,
                tx.keystroke_flight_time_ms,
                tx.touch_pressure,
                tx.touch_motion_speed,
                tx.sensor_entropy,
                tx.biometric_liveness_score
            ]])
            # Isolation score maps -1 (anomaly) to +1 (normal)
            raw_score = self.iso_model.decision_function(x_vec)[0]
            iso_risk = float(np.clip(1.0 - (raw_score + 0.5), 0.0, 1.0))
        else:
            iso_risk = 0.0

        # Weighted combination
        rule_risk = (
            0.30 * min(1.0, z_hold / 4.0) +
            0.20 * min(1.0, z_flight / 4.0) +
            0.20 * min(1.0, z_entropy / 4.0) +
            0.30 * (1.0 - tx.biometric_liveness_score)
        )

        if is_bot_speed > 0:
            rule_risk = max(rule_risk, 0.88)
        if is_deepfake > 0:
            rule_risk = max(rule_risk, 0.95)

        combined_risk = float(np.clip(0.6 * rule_risk + 0.4 * iso_risk, 0.0, 1.0))

        return {
            "behavioral_risk_score": round(combined_risk, 4),
            "is_synthetic_telemetry": combined_risk > 0.65,
            "biometric_liveness": round(tx.biometric_liveness_score, 4),
            "sensor_entropy": round(tx.sensor_entropy, 4),
            "keystroke_cadence": f"{tx.keystroke_hold_time_ms:.1f}ms hold / {tx.keystroke_flight_time_ms:.1f}ms flight",
            "anomaly_reasons": [
                k for k, v in [
                    ("Inhuman keystroke velocity", is_bot_speed > 0),
                    ("Synthetic face/voice deepfake signature", is_deepfake > 0),
                    ("Flatline device motion sensor (Emulator)", is_flatline_sensor > 0),
                    ("Abnormal touch spline pressure", tx.touch_pressure > 0.95 or tx.touch_pressure < 0.15)
                ] if v
            ]
        }
