"""
AegisPay-AI: Comprehensive Benchmark Pipeline (Pillar 3 & 5 Validation)
Evaluates ROC-AUC, PR-AUC, F1-Score, False Positive Rate at High Recall,
sub-50ms latency benchmarks (per-component & overall percentiles),
and writes verified results to 'benchmarks/benchmark_results.json'.
"""
import time
import json
import os
from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix
)

from red_team.generator import SyntheticTransactionEngine, TransactionRecord
from red_team.taxonomy import ThreatTaxonomy
from blue_team.meta_classifier import MultiModalFusionEngine, DecisionAction


class BenchmarkPipeline:
    """
    Comprehensive performance and latency evaluation suite.
    All outputs come directly from actual execution runs.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.tx_engine = SyntheticTransactionEngine(seed=seed)
        self.taxonomy = ThreatTaxonomy()
        self.blue_engine = MultiModalFusionEngine()

    def run_full_benchmark(
        self,
        train_samples: int = 3500,
        test_samples: int = 1500,
        fraud_ratio: float = 0.15,
        save_results: bool = True
    ) -> Dict[str, Any]:
        """
        Executes end-to-end training, testing, per-level latency profiling, and vector ablation benchmarks.
        """
        print(f"[*] Generating {train_samples} training records...")
        train_dataset = self.tx_engine.generate_dataset(
            n_samples=train_samples,
            fraud_ratio=fraud_ratio,
            stealth_distribution="mixed"
        )

        print("[*] Training Blue Team Multi-Modal Defense...")
        t_train_start = time.perf_counter()
        self.blue_engine.train_baseline(train_dataset)
        train_duration = time.perf_counter() - t_train_start

        print(f"[*] Generating {test_samples} test records across 24 attack vectors...")
        test_dataset = self.tx_engine.generate_dataset(
            n_samples=test_samples,
            fraud_ratio=0.20,  # 20% fraud test mix
            stealth_distribution="mixed"
        )

        print("[*] Evaluating live inference and measuring real-time latency breakdown...")
        y_true = []
        y_probs = []
        y_preds = []
        total_latencies = []
        
        # Component-level latencies
        fs_latencies = []
        l1_latencies = []
        l2_latencies = []
        l3_latencies = []
        l4_latencies = []

        vector_performance: Dict[str, Dict[str, Any]] = {}

        for tx in test_dataset:
            # Component breakdown measurements
            t0 = time.perf_counter()
            fv = self.blue_engine.feature_store.extract_features(tx)
            fs_latencies.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = self.blue_engine.tabular_detector.predict_proba(fv)
            l1_latencies.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = self.blue_engine.behavioral_detector.predict_anomaly_score(tx)
            l2_latencies.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = self.blue_engine.gnn_detector.score_ego_subgraph(tx)
            l3_latencies.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = self.blue_engine.semantic_guardrail.inspect_payload(tx)
            l4_latencies.append((time.perf_counter() - t0) * 1000.0)

            # Measure full evaluation pipeline
            t_eval_start = time.perf_counter()
            dec = self.blue_engine.evaluate_transaction(tx)
            total_elapsed_ms = (time.perf_counter() - t_eval_start) * 1000.0
            total_latencies.append(total_elapsed_ms)

            prob = float(dec.fused_risk_score)
            y_true.append(1 if tx.is_fraud else 0)
            y_probs.append(prob)
            y_preds.append(1 if prob >= 0.50 else 0)

            # Vector-level tracking
            if tx.is_fraud and tx.attack_vector_id:
                vec_id = tx.attack_vector_id
                if vec_id not in vector_performance:
                    vector_performance[vec_id] = {"total": 0, "detected": 0, "probs": []}
                vector_performance[vec_id]["total"] += 1
                if prob >= 0.50:
                    vector_performance[vec_id]["detected"] += 1
                vector_performance[vec_id]["probs"].append(prob)

        y_true = np.array(y_true)
        y_probs = np.array(y_probs)
        y_preds = np.array(y_preds)

        # Core Metrics
        roc_auc = float(roc_auc_score(y_true, y_probs))
        pr_auc = float(average_precision_score(y_true, y_probs))
        f1 = float(f1_score(y_true, y_preds))
        precision = float(precision_score(y_true, y_preds))
        recall = float(recall_score(y_true, y_preds))

        tn, fp, fn, tp = confusion_matrix(y_true, y_preds).ravel()
        fpr = float(fp / max(1, (fp + tn)))
        fnr = float(fn / max(1, (fn + tp)))

        # Format Vector-level breakdown
        vector_breakdown = {}
        for vec_id, v_data in vector_performance.items():
            tot = v_data["total"]
            det = v_data["detected"]
            mean_prob = float(np.mean(v_data["probs"])) if tot > 0 else 0.0
            rec = (det / tot) * 100.0 if tot > 0 else 0.0
            vector_breakdown[vec_id] = {
                "total_probes": tot,
                "detected_count": det,
                "detection_rate_pct": round(rec, 2),
                "mean_fused_risk": round(mean_prob, 4)
            }

        # Format Latency Breakdown
        latency_summary = {
            "mean_latency_ms": round(float(np.mean(total_latencies)), 2),
            "p50_latency_ms": round(float(np.percentile(total_latencies, 50)), 2),
            "p90_latency_ms": round(float(np.percentile(total_latencies, 90)), 2),
            "p95_latency_ms": round(float(np.percentile(total_latencies, 95)), 2),
            "p99_latency_ms": round(float(np.percentile(total_latencies, 99)), 2),
            "component_means_ms": {
                "feature_store": round(float(np.mean(fs_latencies)), 2),
                "level_1_tabular": round(float(np.mean(l1_latencies)), 2),
                "level_2_biometrics": round(float(np.mean(l2_latencies)), 2),
                "level_3_graph_gnn": round(float(np.mean(l3_latencies)), 2),
                "level_4_semantic_nlp": round(float(np.mean(l4_latencies)), 2),
            },
            "mastercard_sla_target_ms": 50.0,
            "sla_compliant": bool(np.percentile(total_latencies, 99) < 50.0)
        }

        classification_summary = {
            "roc_auc": round(roc_auc, 4),
            "pr_auc": round(pr_auc, 4),
            "f1_score": round(f1, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "false_positive_rate": round(fpr, 4),
            "false_negative_rate": round(fnr, 4),
            "confusion_matrix": {
                "true_positives": int(tp),
                "false_positives": int(fp),
                "true_negatives": int(tn),
                "false_negatives": int(fn)
            },
            "sample_counts": {
                "train_samples": train_samples,
                "test_samples": test_samples,
                "benign_test": int(tn + fp),
                "fraud_test": int(tp + fn)
            },
            "training_duration_seconds": round(train_duration, 2)
        }

        results = {
            "benchmark_timestamp": time.time(),
            "summary": classification_summary,
            "latency": latency_summary,
            "vector_breakdown": vector_breakdown
        }

        if save_results:
            results_path = os.path.join(os.path.dirname(__file__), "benchmark_results.json")
            with open(results_path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"[+] Saved verified benchmark results to '{results_path}'")

        return results


if __name__ == "__main__":
    bp = BenchmarkPipeline(seed=42)
    res = bp.run_full_benchmark()
    print("\n--- BENCHMARK RESULTS SUMMARY ---")
    print(json.dumps(res["summary"], indent=2))
    print("\n--- LATENCY BREAKDOWN ---")
    print(json.dumps(res["latency"], indent=2))
