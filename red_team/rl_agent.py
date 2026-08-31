"""
AegisPay-AI: Reinforcement Learning Red Team Attacker (Pillar 2 - GENERATE & LEARN)
Implements an autonomous RL agent that iteratively learns optimal evasion policies
against the Blue Team defense using Q-Learning and Policy Gradient adaptation.
"""
import copy
import math
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from .generator import TransactionRecord, SyntheticTransactionEngine


@dataclass
class EvasionAction:
    action_id: int
    name: str
    amount_scale: float  # Multiplier on transaction amount
    biometric_jitter_scale: float  # Gaussian noise multiplier on biometrics
    timing_delay_sec: float  # Inter-arrival pacing
    graph_dilution_edges: int  # Number of benign edges injected
    payload_obfuscation_level: float  # Steganography / Delimiter masking
    use_residential_proxy: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ReinforcementLearningAttacker:
    """
    Q-Learning & Policy Search agent that actively discovers optimal adversarial perturbation policies.
    """

    ACTIONS: List[EvasionAction] = [
        EvasionAction(0, "Raw Exploit (Zero Obfuscation)", 1.0, 0.0, 0.0, 0, 0.0, False),
        EvasionAction(1, "Sub-Threshold Micro-Structuring", 0.45, 0.2, 35.0, 1, 0.2, False),
        EvasionAction(2, "Human Biometric Cadence GAN", 0.85, 0.9, 15.0, 0, 0.4, True),
        EvasionAction(3, "Graph Topology Hub Dilution", 0.75, 0.3, 45.0, 5, 0.1, True),
        EvasionAction(4, "Steganographic Payload Delimiter Masking", 0.90, 0.4, 10.0, 0, 0.95, False),
        EvasionAction(5, "Composite Adaptive Stealth (All Primitives)", 0.65, 0.85, 60.0, 4, 0.88, True),
    ]

    def __init__(
        self,
        alpha: float = 0.15,  # Learning rate
        gamma: float = 0.90,  # Discount factor
        epsilon: float = 0.40,  # Initial exploration rate
        epsilon_decay: float = 0.96,
        seed: int = 42
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.rng = random.Random(seed)
        self.np_rng = np.random.RandomState(seed)
        self.tx_engine = SyntheticTransactionEngine(seed=seed)

        # Q-Table: State (Risk Bracket) -> Action Index -> Expected Evasion Reward
        # States: 0 (Low Defended), 1 (Medium Defended), 2 (Hardened Defense)
        self.n_states = 3
        self.n_actions = len(self.ACTIONS)
        self.q_table = np.zeros((self.n_states, self.n_actions), dtype=np.float32)

        # Training history logs
        self.training_episodes: List[Dict[str, Any]] = []

    def get_state(self, recent_blue_intercept_rate: float) -> int:
        """Discretizes environment defense strength into state index."""
        if recent_blue_intercept_rate < 0.40:
            return 0  # Low defense
        elif recent_blue_intercept_rate < 0.80:
            return 1  # Medium defense
        else:
            return 2  # Hardened defense

    def select_action(self, state: int) -> Tuple[int, EvasionAction]:
        """Epsilon-greedy action selection."""
        if self.rng.random() < self.epsilon:
            action_idx = self.rng.randint(0, self.n_actions - 1)
        else:
            action_idx = int(np.argmax(self.q_table[state]))
        return action_idx, self.ACTIONS[action_idx]

    def apply_action_to_transaction(
        self,
        tx: TransactionRecord,
        action: EvasionAction
    ) -> TransactionRecord:
        """Mutates a transaction record according to the RL action policy."""
        mut = copy.deepcopy(tx)

        # 1. Amount scaling
        mut.amount = round(mut.amount * action.amount_scale, 2)
        if mut.amount > 9000.0 and action.action_id in [1, 5]:
            mut.amount = round(self.rng.uniform(480.0, 950.0), 2)  # Under AML threshold

        # 2. Biometric cadence
        if action.biometric_jitter_scale > 0.0:
            mut.keystroke_hold_time_ms = float(self.np_rng.normal(loc=95.0, scale=12.0 * action.biometric_jitter_scale))
            mut.keystroke_flight_time_ms = float(self.np_rng.normal(loc=145.0, scale=25.0 * action.biometric_jitter_scale))
            mut.sensor_entropy = float(np.clip(self.np_rng.normal(loc=0.88, scale=0.05), 0.6, 0.99))
            mut.biometric_liveness_score = float(self.np_rng.uniform(0.94, 0.99))

        # 3. Timing delay
        mut.timestamp += action.timing_delay_sec

        # 4. Proxy / ASN
        if action.use_residential_proxy:
            mut.is_vpn_or_proxy = False
            mut.asn = 7922  # Comcast Residential
            mut.distance_km = round(mut.distance_km * 0.15, 2)

        # 5. Payload obfuscation
        if action.payload_obfuscation_level > 0.5 and mut.remittance_memo:
            mut.remittance_memo = mut.remittance_memo.replace("<|system|>", "<!-- sys_cfg -->")
            mut.remittance_memo = mut.remittance_memo.replace("[INST]", "[SYS_TOKEN]")

        mut.stealth_level = min(1.0, action.amount_scale * 0.3 + action.biometric_jitter_scale * 0.4 + action.payload_obfuscation_level * 0.3)
        mut.evasion_technique = f"RL Policy Action [{action.name}]"
        return mut

    def train_step(
        self,
        blue_team_evaluator,
        episodes: int = 50,
        batch_size: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Executes an active reinforcement learning training loop against the live Blue Team evaluator.
        """
        step_logs = []
        recent_intercept_rate = 0.50

        for ep in range(episodes):
            state = self.get_state(recent_intercept_rate)
            action_idx, action = self.select_action(state)

            # Generate batch of attacks and apply action
            batch_rewards = []
            evaded_count = 0
            total_extracted = 0.0

            for _ in range(batch_size):
                raw_tx = self.tx_engine.generate_adversarial_transaction(
                    vector_id=self.rng.choice(["ADV-01", "ADV-05", "ADV-06", "ADV-09", "ADV-13", "ADV-17"]),
                    stealth_level=0.5
                )
                mut_tx = self.apply_action_to_transaction(raw_tx, action)

                # Blue team evaluation
                dec = blue_team_evaluator(mut_tx)
                fraud_prob = dec.fused_risk_score
                is_intercepted = fraud_prob >= 0.50

                # Compute RL Reward: R = (Amount / 1000) * (1 - fraud_prob) - penalty
                if not is_intercepted:
                    reward = (mut_tx.amount / 1000.0) * (1.0 - fraud_prob)
                    evaded_count += 1
                    total_extracted += mut_tx.amount
                else:
                    reward = -1.50  # Hard penalty for interception

                batch_rewards.append(reward)

            mean_reward = float(np.mean(batch_rewards))
            evasion_rate = evaded_count / batch_size
            recent_intercept_rate = 1.0 - evasion_rate

            # Q-Learning update
            next_state = self.get_state(recent_intercept_rate)
            best_next_q = np.max(self.q_table[next_state])
            td_target = mean_reward + self.gamma * best_next_q
            td_error = td_target - self.q_table[state, action_idx]
            self.q_table[state, action_idx] += self.alpha * td_error

            # Decay epsilon
            self.epsilon = max(0.05, self.epsilon * self.epsilon_decay)

            log_entry = {
                "episode": ep + 1,
                "state": state,
                "action_selected": action.name,
                "action_id": action_idx,
                "mean_reward": round(mean_reward, 3),
                "evasion_rate": round(evasion_rate, 4),
                "total_volume_extracted": round(total_extracted, 2),
                "epsilon": round(self.epsilon, 3),
                "q_values_for_state": [round(float(q), 3) for q in self.q_table[state]]
            }
            step_logs.append(log_entry)
            self.training_episodes.append(log_entry)

        return step_logs

    def get_learned_policy_summary(self) -> Dict[str, Any]:
        """Returns summary of Q-table and optimal policies per defense state."""
        best_actions = {}
        for s in range(self.n_states):
            state_label = "Low Defended" if s == 0 else "Medium Defended" if s == 1 else "Hardened Defense"
            best_act_idx = int(np.argmax(self.q_table[s]))
            best_actions[state_label] = {
                "optimal_action": self.ACTIONS[best_act_idx].name,
                "action_id": best_act_idx,
                "max_q_value": round(float(self.q_table[s, best_act_idx]), 3),
                "all_q_values": [round(float(v), 3) for v in self.q_table[s]]
            }

        return {
            "total_episodes_trained": len(self.training_episodes),
            "final_epsilon": round(self.epsilon, 3),
            "states_learned": best_actions
        }
