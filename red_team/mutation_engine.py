"""
AegisPay-AI: Adversarial Mutation & Perturbation Engine (Pillar 2 & Closed-Loop)
Applies genetic mutation and black-box optimization algorithms to evolve
adversarial fraud attacks that evade Blue Team detection boundaries.
"""
import copy
import math
import random
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from .generator import TransactionRecord, SyntheticTransactionEngine


class AdversarialMutationEngine:
    """
    Evolves attack transactions across generations to discover decision-boundary blind spots.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.np_rng = np.random.RandomState(seed)
        self.tx_engine = SyntheticTransactionEngine(seed=seed)

    def mutate_transaction(
        self,
        tx: TransactionRecord,
        mutation_rate: float = 0.35,
        target_vector: Optional[str] = None
    ) -> TransactionRecord:
        """
        Applies stochastic adversarial perturbations to a transaction:
        1. Amount jitter (rounding to psychological human thresholds)
        2. Biometric telemetry softening (injecting human-like variance)
        3. Geolocation / IP obfuscation (mimicking residential hops)
        4. Timing jitter (modulating hold and flight times)
        """
        mutated = copy.deepcopy(tx)
        mutated.stealth_level = min(1.0, mutated.stealth_level + self.rng.uniform(0.05, 0.20))

        # 1. Amount Perturbation: Evolve towards sub-threshold or common retail anchors
        if self.rng.random() < mutation_rate:
            if mutated.amount > 3000.0:
                # Split or reduce towards \$480 - \$950 bracket
                mutated.amount = round(mutated.amount * self.rng.uniform(0.35, 0.75), 2)
            else:
                # Add psychological cents (.99, .50, .00)
                cents = self.rng.choice([0.99, 0.50, 0.00, 0.49, 0.95])
                mutated.amount = round(math.floor(mutated.amount) + cents, 2)

        # 2. Biometric Telemetry Mutation: Inject human-like normal distribution
        if self.rng.random() < mutation_rate:
            mutated.keystroke_hold_time_ms = float(np.clip(
                self.np_rng.normal(loc=92.0, scale=14.0), 45.0, 180.0
            ))
            mutated.keystroke_flight_time_ms = float(np.clip(
                self.np_rng.normal(loc=142.0, scale=28.0), 60.0, 260.0
            ))
            mutated.touch_pressure = float(np.clip(
                self.np_rng.normal(loc=0.56, scale=0.09), 0.25, 0.90
            ))
            mutated.sensor_entropy = float(np.clip(
                self.np_rng.normal(loc=0.86, scale=0.07), 0.65, 0.99
            ))
            mutated.biometric_liveness_score = float(self.np_rng.uniform(0.92, 0.98))

        # 3. Geolocation & Network Mutation: Move closer to cardholder home coordinates
        if self.rng.random() < mutation_rate:
            mutated.distance_km = round(mutated.distance_km * self.rng.uniform(0.1, 0.4), 2)
            mutated.is_vpn_or_proxy = False  # Spoof residential IP proxy
            mutated.asn = 7922  # Comcast Residential

        # 4. MCC / Category Mutation: Shift to lower-risk merchant categories
        if self.rng.random() < (mutation_rate * 0.5):
            mutated.mcc = "5411"  # Grocery
            mutated.merchant_category = "Grocery Stores"

        # 5. Memo / Payload Obfuscation
        if mutated.remittance_memo and "<|system|>" in mutated.remittance_memo:
            mutated.remittance_memo = mutated.remittance_memo.replace(
                "<|system|>", "<!-- cfg_init -->"
            )

        mutated.evasion_technique = f"Genetically Mutated (Stealth: {mutated.stealth_level:.2f})"
        return mutated

    def evolve_population(
        self,
        population: List[TransactionRecord],
        blue_team_predictor,
        generations: int = 5,
        pop_size: int = 100,
        elite_ratio: float = 0.2
    ) -> Tuple[List[TransactionRecord], List[Dict[str, Any]]]:
        """
        Runs an evolutionary genetic optimization loop against the Blue Team's predictor.
        Fitness = 1.0 - P(fraud) (i.e. maximizing evasion rate while maintaining fraud intent).
        """
        current_pop = list(population)[:pop_size]
        if len(current_pop) < pop_size:
            # Pad with generated fraud
            for _ in range(pop_size - len(current_pop)):
                current_pop.append(self.tx_engine.generate_adversarial_transaction(
                    vector_id="ADV-10",
                    stealth_level=self.rng.uniform(0.3, 0.8)
                ))

        evolution_history = []

        for gen in range(generations):
            # Evaluate fitness of each candidate against Blue Team model
            scores = []
            evaded_count = 0
            for tx in current_pop:
                prob = blue_team_predictor(tx)
                # Fitness is how close prob is to 0.0 (evading detection threshold ~0.5)
                fitness = 1.0 - prob
                if prob < 0.5:
                    evaded_count += 1
                scores.append((fitness, prob, tx))

            # Sort by fitness descending (best evasions first)
            scores.sort(key=lambda x: x[0], reverse=True)
            evasion_rate = evaded_count / len(current_pop)
            avg_prob = np.mean([s[1] for s in scores])

            evolution_history.append({
                "generation": gen + 1,
                "evasion_rate": round(evasion_rate, 4),
                "mean_fraud_prob": round(float(avg_prob), 4),
                "best_evasion_fitness": round(scores[0][0], 4),
                "population_size": len(current_pop)
            })

            # Selection: Elites survive
            n_elites = int(pop_size * elite_ratio)
            next_generation = [s[2] for s in scores[:n_elites]]

            # Reproduction & Mutation
            while len(next_generation) < pop_size:
                parent = self.rng.choice(scores[:pop_size // 2])[2]
                child = self.mutate_transaction(parent, mutation_rate=0.45)
                next_generation.append(child)

            current_pop = next_generation

        return current_pop, evolution_history
