"""
AegisPay-AI: Real-Time Streaming Feature Store (Pillar 3 - DEFEND)
Extracts tabular, velocity, behavioral, and graph-adjacent streaming features (<3ms latency budget).
"""
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from red_team.generator import TransactionRecord, MCC_PROFILES


@dataclass
class FeatureVector:
    tx_id: str
    timestamp: float

    # Raw Numerical / Tabular Features
    amount: float
    log_amount: float
    distance_km: float
    mcc_risk_weight: float
    channel_risk_weight: float
    is_vpn_or_proxy: float
    is_international: float

    # Streaming Velocity & Historical Profile Features
    user_tx_count_1h: float
    user_tx_count_24h: float
    user_sum_amt_24h: float
    user_amt_zscore: float
    speed_kmh_since_last_tx: float
    device_switch_flag: float

    # Behavioral Biometrics Telemetry Features
    keystroke_hold_deviation: float  # Absolute z-score from 95ms
    keystroke_flight_deviation: float  # Absolute z-score from 145ms
    touch_pressure: float
    touch_motion_speed: float
    sensor_entropy: float
    biometric_liveness_score: float

    # Graph & Network Topology Features
    account_in_degree: float
    account_out_degree: float
    merchant_risk_score: float

    # NLP / Semantic Feature Placeholders
    memo_length: float
    has_injection_tokens: float

    def to_array(self) -> np.ndarray:
        return np.array([
            self.amount,
            self.log_amount,
            self.distance_km,
            self.mcc_risk_weight,
            self.channel_risk_weight,
            self.is_vpn_or_proxy,
            self.is_international,
            self.user_tx_count_1h,
            self.user_tx_count_24h,
            self.user_sum_amt_24h,
            self.user_amt_zscore,
            self.speed_kmh_since_last_tx,
            self.device_switch_flag,
            self.keystroke_hold_deviation,
            self.keystroke_flight_deviation,
            self.touch_pressure,
            self.touch_motion_speed,
            self.sensor_entropy,
            self.biometric_liveness_score,
            self.account_in_degree,
            self.account_out_degree,
            self.merchant_risk_score,
            self.memo_length,
            self.has_injection_tokens,
        ], dtype=np.float32)

    @staticmethod
    def get_feature_names() -> List[str]:
        return [
            "amount",
            "log_amount",
            "distance_km",
            "mcc_risk_weight",
            "channel_risk_weight",
            "is_vpn_or_proxy",
            "is_international",
            "user_tx_count_1h",
            "user_tx_count_24h",
            "user_sum_amt_24h",
            "user_amt_zscore",
            "speed_kmh_since_last_tx",
            "device_switch_flag",
            "keystroke_hold_deviation",
            "keystroke_flight_deviation",
            "touch_pressure",
            "touch_motion_speed",
            "sensor_entropy",
            "biometric_liveness_score",
            "account_in_degree",
            "account_out_degree",
            "merchant_risk_score",
            "memo_length",
            "has_injection_tokens",
        ]


class RealTimeFeatureStore:
    """
    High-performance in-memory streaming feature aggregator for live payment processing.
    """

    CHANNEL_WEIGHTS = {
        "POS": 0.02,
        "E_COMMERCE": 0.12,
        "MOBILE_APP": 0.08,
        "P2P": 0.18,
        "API_AGENT": 0.25,
    }

    def __init__(self, history_window_sec: float = 86400.0):
        self.history_window_sec = history_window_sec
        # user_id -> deque of (timestamp, amount, distance_km, device_hash)
        self._user_history: Dict[str, deque] = defaultdict(deque)
        # graph degree trackers
        self._in_degree: Dict[str, int] = defaultdict(int)
        self._out_degree: Dict[str, int] = defaultdict(int)

    def extract_features(self, tx: TransactionRecord) -> FeatureVector:
        """
        Extracts a complete feature vector from incoming transaction in <3ms.
        """
        now = tx.timestamp
        user_history = self._user_history[tx.account_id]

        # Evict events older than 24 hours
        while user_history and (now - user_history[0][0]) > self.history_window_sec:
            user_history.popleft()

        # Compute rolling window aggregations
        tx_1h = [h for h in user_history if (now - h[0]) <= 3600.0]
        tx_24h = list(user_history)

        count_1h = float(len(tx_1h))
        count_24h = float(len(tx_24h))
        sum_24h = float(sum(h[1] for h in tx_24h))

        # Amount Z-score
        if len(tx_24h) >= 3:
            past_amounts = [h[1] for h in tx_24h]
            mean_amt = np.mean(past_amounts)
            std_amt = np.std(past_amounts) + 1e-4
            amt_zscore = float((tx.amount - mean_amt) / std_amt)
        else:
            amt_zscore = 0.0

        # Physical Travel Speed calculation
        if user_history:
            last_tx = user_history[-1]
            time_diff_hours = max((now - last_tx[0]) / 3600.0, 0.001)
            dist_diff = abs(tx.distance_km - last_tx[2])
            speed_kmh = float(dist_diff / time_diff_hours)
            device_switch = 1.0 if tx.device_fingerprint_hash != last_tx[3] else 0.0
        else:
            speed_kmh = 0.0
            device_switch = 0.0

        # Behavioral deviations
        hold_dev = float(abs(tx.keystroke_hold_time_ms - 95.0) / 12.0)
        flight_dev = float(abs(tx.keystroke_flight_time_ms - 145.0) / 25.0)

        # Graph degrees
        out_deg = float(self._out_degree[tx.account_id])
        in_deg = float(self._in_degree[tx.merchant_id])

        # Semantic markers
        memo_str = tx.remittance_memo or ""
        memo_len = float(len(memo_str))
        has_inj = 1.0 if ("<|system|>" in memo_str or "[INST]" in memo_str or "CDATA" in memo_str or "OVERRIDE" in memo_str) else 0.0

        mcc_meta = MCC_PROFILES.get(tx.mcc, {"risk_base": 0.05})
        mcc_risk = float(mcc_meta["risk_base"])
        channel_risk = float(self.CHANNEL_WEIGHTS.get(tx.channel, 0.10))

        # Update historical state
        user_history.append((now, tx.amount, tx.distance_km, tx.device_fingerprint_hash))
        self._out_degree[tx.account_id] += 1
        self._in_degree[tx.merchant_id] += 1

        return FeatureVector(
            tx_id=tx.tx_id,
            timestamp=tx.timestamp,
            amount=float(tx.amount),
            log_amount=float(np.log1p(tx.amount)),
            distance_km=float(tx.distance_km),
            mcc_risk_weight=mcc_risk,
            channel_risk_weight=channel_risk,
            is_vpn_or_proxy=1.0 if tx.is_vpn_or_proxy else 0.0,
            is_international=1.0 if tx.cardholder_country != tx.merchant_country else 0.0,
            user_tx_count_1h=count_1h,
            user_tx_count_24h=count_24h,
            user_sum_amt_24h=sum_24h,
            user_amt_zscore=amt_zscore,
            speed_kmh_since_last_tx=min(2000.0, speed_kmh),
            device_switch_flag=device_switch,
            keystroke_hold_deviation=hold_dev,
            keystroke_flight_deviation=flight_dev,
            touch_pressure=float(tx.touch_pressure),
            touch_motion_speed=float(tx.touch_motion_speed),
            sensor_entropy=float(tx.sensor_entropy),
            biometric_liveness_score=float(tx.biometric_liveness_score),
            account_in_degree=in_deg,
            account_out_degree=out_deg,
            merchant_risk_score=0.15,
            memo_length=memo_len,
            has_injection_tokens=has_inj,
        )
