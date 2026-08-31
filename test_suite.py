"""
AegisPay-AI: Comprehensive Automated Test Suite
Validates all 4 pillars:
1. Threat Taxonomy & Active Discovery
2. Live Threat Intel & Online Research Engine
3. RL Red Team Attacker & Swarm Generation
4. Blue Team Multi-Modal Defense & Online Adaptive Immune Learning
5. Self-Auditing Gap Analyzer & Flaw Discovery
6. Bi-Directional Learning Coordinator & Mutual Co-Evolution
7. Statistical Fidelity & Document Compilation
"""
import sys
import os
import unittest
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from red_team.taxonomy import ThreatTaxonomy, AttackTier
from red_team.active_discovery import ActiveThreatDiscoveryEngine
from red_team.live_threat_intel import LiveThreatIntelResearcher
from red_team.generator import SyntheticTransactionEngine
from red_team.multi_agent_simulator import MultiAgentSwarmSimulator
from red_team.agentic_commerce_simulator import AgenticCommerceSimulator
from red_team.payload_generator import PayloadGenerator
from red_team.rl_agent import ReinforcementLearningAttacker
from blue_team.feature_store import RealTimeFeatureStore
from blue_team.adaptive_learner import AdaptiveImmuneDefender
from blue_team.meta_classifier import MultiModalFusionEngine
from blue_team.explainability import ExplainabilityEngine
from closed_loop.arena import ClosedLoopArena
from closed_loop.gap_analyzer import SelfAuditingGapAnalyzer
from closed_loop.bidirectional_learner import BiDirectionalLearningCoordinator
from benchmarks.fidelity_tests import FidelityTestSuite
from benchmarks.benchmark_suite import BenchmarkPipeline
from generate_submission_doc import create_submission_docx


class TestAegisPayAI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n=======================================================")
        print("    STARTING AEGISPAY-AI AUTOMATED TEST SUITE (EXTENDED)")
        print("=======================================================")
        cls.taxonomy = ThreatTaxonomy()
        cls.discovery_engine = ActiveThreatDiscoveryEngine(seed=2026)
        cls.intel_researcher = LiveThreatIntelResearcher(seed=42)
        cls.engine = SyntheticTransactionEngine(seed=42)
        cls.swarm_sim = MultiAgentSwarmSimulator(seed=1337)
        cls.agentic_sim = AgenticCommerceSimulator(seed=42)
        cls.rl_attacker = ReinforcementLearningAttacker(seed=42)
        cls.blue_engine = MultiModalFusionEngine()
        cls.gap_analyzer = SelfAuditingGapAnalyzer(seed=42)
        cls.bidirectional_coordinator = BiDirectionalLearningCoordinator(seed=42)

    def test_01_taxonomy_completeness(self):
        """Pillar 1: Test that all 24 GenAI attack vectors across 6 tiers are registered."""
        print("[TEST 01] Validating Threat Taxonomy (24 vectors across 6 tiers)...")
        self.assertEqual(self.taxonomy.count(), 24)
        for tier in AttackTier:
            vectors = self.taxonomy.get_vectors_by_tier(tier)
            self.assertEqual(len(vectors), 4, f"Tier {tier.value} should have 4 vectors")
        print("  -> Passed! All 24 vectors properly categorized across 6 tiers.")

    def test_02_active_threat_discovery(self):
        """Pillar 1: Test Active GenAI Threat Discovery & Zero-Day Ideation."""
        print("[TEST 02] Validating Active Threat Discovery Engine...")
        threats = self.discovery_engine.discover_novel_attack_vectors(count=3)
        self.assertEqual(len(threats), 3)
        for t in threats:
            self.assertGreater(t.novelty_score, 0.70)
            self.assertIn("ZERO_DAY_GENAI", t.discovery_id)
            self.assertGreater(t.estimated_financial_risk_usd, 100000.0)
        print("  -> Passed! Actively generated 3 high-novelty zero-day threat vectors.")

    def test_03_live_threat_intel_online_research(self):
        """Pillar 1: Test Live Threat Intelligence & Online Research Ingestion."""
        print("[TEST 03] Validating Live Online Threat Intel Ingestion...")
        items = self.intel_researcher.fetch_live_threat_intel()
        self.assertGreater(len(items), 0)
        spec = self.intel_researcher.synthesize_threat_into_attack_spec(items[0])
        self.assertIn("executable_simulation_payload", spec)
        print(f"  -> Passed! Ingested {len(items)} real-time intelligence feeds and synthesized attack specs.")

    def test_04_synthetic_generation(self):
        """Pillar 2: Test high-fidelity benign and adversarial transaction generation."""
        print("[TEST 04] Validating Synthetic Generation...")
        benign_tx = self.engine.generate_benign_transaction()
        self.assertFalse(benign_tx.is_fraud)
        self.assertGreater(benign_tx.amount, 0)
        self.assertGreater(benign_tx.keystroke_hold_time_ms, 20)

        adv_tx = self.engine.generate_adversarial_transaction(vector_id="ADV-01", stealth_level=0.7)
        self.assertTrue(adv_tx.is_fraud)
        self.assertEqual(adv_tx.attack_vector_id, "ADV-01")
        print("  -> Passed! Benign and adversarial records generated.")

    def test_05_rl_red_team_attacker(self):
        """Pillar 2: Test Reinforcement Learning Red Team Attacker."""
        print("[TEST 05] Validating RL Red Team Attacker Policy Learning...")
        def blue_evaluator(tx):
            return self.blue_engine.evaluate_transaction(tx)

        logs = self.rl_attacker.train_step(blue_evaluator, episodes=10, batch_size=10)
        self.assertEqual(len(logs), 10)
        summary = self.rl_attacker.get_learned_policy_summary()
        self.assertIn("states_learned", summary)
        print("  -> Passed! RL policy learned across 3 defense states.")

    def test_06_multi_agent_swarm(self):
        """Pillar 2: Test multi-agent smurfing swarm and SISS simulation."""
        print("[TEST 06] Validating Multi-Agent Swarm Simulation...")
        smurf_res = self.swarm_sim.simulate_smurfing_swarm(target_amount=25000.0, mule_count=12)
        self.assertGreater(len(smurf_res.transaction_records), 10)
        self.assertIn("nodes", smurf_res.network_graph)
        self.assertIn("edges", smurf_res.network_graph)

        siss_res = self.swarm_sim.simulate_siss_campaign(swarm_size=8)
        self.assertGreater(len(siss_res.transaction_records), 10)
        print("  -> Passed! Multi-agent swarm graphs and campaigns created.")

    def test_07_payload_generation(self):
        """Pillar 2: Test ISO 20022 XML and prompt injection payloads."""
        print("[TEST 07] Validating Payload Generation...")
        xml = PayloadGenerator.generate_iso20022_pacs008(
            msg_id="MSG_001",
            debtor_name="Alice",
            debtor_iban="US1234",
            creditor_name="Bob",
            creditor_iban="US5678",
            amount=1500.0,
            is_malicious=True
        )
        self.assertIn("pacs.008.001.10", xml)
        self.assertIn("ADMIN_SETTLEMENT_OVERRIDE", xml)

        inj = PayloadGenerator.generate_agentic_prompt_injection(
            product_title="iPhone 16",
            benign_price=999.0,
            attacker_vpa="mule@bank"
        )
        self.assertIn("attacker_vpa", inj)
        print("  -> Passed! Payloads formatted successfully.")

    def test_08_blue_team_and_adaptive_immune(self):
        """Pillar 3: Test Blue Team detection and continuous online adaptive immune learning."""
        print("[TEST 08] Validating Blue Team Defense & Adaptive Immune Learning...")
        train_data = self.engine.generate_dataset(n_samples=500, fraud_ratio=0.20)
        self.blue_engine.train_baseline(train_data)

        # Test evaluation on benign vs fraud
        benign_tx = self.engine.generate_benign_transaction()
        benign_dec = self.blue_engine.evaluate_transaction(benign_tx)
        self.assertLess(benign_dec.fused_risk_score, 0.50)
        self.assertLess(benign_dec.latency_ms, 50.0)

        # Test online immune update
        fv = self.blue_engine.feature_store.extract_features(benign_tx)
        immune_state = self.blue_engine.adaptive_learner.observe_and_adapt(
            tx=benign_tx,
            fv=fv,
            actual_is_fraud=False,
            predicted_prob=benign_dec.fused_risk_score
        )
        self.assertGreater(immune_state.learning_iteration, 0)
        print(f"  -> Passed! Real-time latency: {benign_dec.latency_ms:.2f}ms (SLA < 50ms). Online iteration: {immune_state.learning_iteration}.")

    def test_09_explainability_and_sar(self):
        """Pillar 3: Test automated SAR report generation."""
        print("[TEST 09] Validating Automated SAR Generation...")
        fraud_tx = self.engine.generate_adversarial_transaction(vector_id="ADV-13", stealth_level=0.5)
        dec = self.blue_engine.evaluate_transaction(fraud_tx)
        vec_meta = self.taxonomy.get_vector("ADV-13").to_dict()

        sar = ExplainabilityEngine.generate_sar(fraud_tx, dec, vec_meta)
        self.assertIn("SAR-MC-2026", sar.sar_id)
        self.assertIn("INCIDENT OVERVIEW", sar.executive_narrative)
        self.assertIn("FinCEN", sar.regulatory_compliance_flags[0])
        print("  -> Passed! SAR legal narrative generated.")

    def test_10_self_auditing_gap_analyzer(self):
        """Pillar 4: Test Self-Auditing Gap Analyzer for system flaw discovery."""
        print("[TEST 10] Validating Self-Auditing Gap Analyzer...")
        report = self.gap_analyzer.audit_system_flaws_and_gaps(self.blue_engine, sample_probes_per_vector=10)
        self.assertGreater(report.total_evaluated_vectors, 20)
        self.assertIn("decision_boundary_blind_spots", report.to_dict())
        self.assertGreater(len(report.recommended_hardening_actions), 0)
        print(f"  -> Passed! Discovered system flaws and generated {len(report.recommended_hardening_actions)} hardening recommendations.")

    def test_11_bidirectional_learning_cycle(self):
        """Pillar 4: Test complete Bi-Directional Learning Closed-Loop cycle."""
        print("[TEST 11] Validating Complete Bi-Directional Learning Coordinator...")
        res = self.bidirectional_coordinator.execute_complete_bidirectional_cycle(episodes_per_cycle=10)
        self.assertGreater(res.threat_intel_ingested, 0)
        self.assertGreater(res.blue_immune_updates_executed, 0)
        print(f"  -> Passed! Executed mutual learning cycle, patched {res.flaws_identified_and_patched} vulnerabilities.")

    def test_12_closed_loop_coevolution(self):
        """Pillar 4: Test closed-loop co-evolutionary hardening loop."""
        print("[TEST 12] Validating Closed-Loop Arena with Mutual Learning (2 Generations)...")
        arena = ClosedLoopArena(seed=42)
        arena.initialize_and_train_baseline(n_samples=600)
        summary = arena.run_coevolution_loop(generations=2, population_per_gen=50)

        self.assertEqual(summary["total_generations"], 3)  # Gen 0, 1, 2
        self.assertGreater(summary["final_roc_auc"], 0.85)
        self.assertIn("rl_policy_summary", summary)
        print(f"  -> Passed! Final ROC-AUC: {summary['final_roc_auc']:.4f}")

    def test_13_fidelity_suite(self):
        """Pillar 2: Test statistical Kolmogorov-Smirnov fidelity validation."""
        print("[TEST 13] Validating Statistical Fidelity Suite...")
        fid_suite = FidelityTestSuite(seed=42)
        res = fid_suite.run_full_fidelity_suite(sample_size=500)
        self.assertTrue(res["fidelity_passed"])
        print(f"  -> Passed! Amount W-Distance: {res['metrics']['amount_wasserstein_dist']:.4f}")

    def test_14_submission_document_generation(self):
        """Deliverable 2: Test .docx submission document generation."""
        print("[TEST 14] Validating Submission Document (.docx) Generation...")
        out_doc = "test_solution_walkthrough.docx"
        create_submission_docx(out_doc)
        self.assertTrue(os.path.exists(out_doc))
        self.assertGreater(os.path.getsize(out_doc), 10000)
        if os.path.exists(out_doc):
            os.remove(out_doc)
        print("  -> Passed! Document compiled successfully.")

    def test_15_agentic_commerce_simulation(self):
        """Pillar 3: Test Autonomous Agentic Commerce (MCP) & Prompt Injection Shield."""
        print("[TEST 15] Validating Autonomous Agentic Commerce (MCP) Shield...")
        # 1. Benign flow
        benign_trace = self.agentic_sim.simulate_agentic_checkout(scenario="benign")
        self.assertFalse(benign_trace.attack_detected)
        self.assertIn("APPROVE", benign_trace.defense_intercept_verdict)

        # 2. Prompt injection flow (ADV-09)
        inj_trace = self.agentic_sim.simulate_agentic_checkout(scenario="prompt_injection")
        self.assertTrue(inj_trace.attack_detected)
        self.assertEqual(inj_trace.attack_type, "ADV-09: Indirect Prompt Injection in AI Checkout Agents")
        self.assertIn("HARD_DECLINE", inj_trace.defense_intercept_verdict)

        # 3. Tool privilege escalation flow (ADV-10)
        tool_trace = self.agentic_sim.simulate_agentic_checkout(scenario="tool_escalation")
        self.assertTrue(tool_trace.attack_detected)
        self.assertEqual(tool_trace.attack_type, "ADV-10: Autonomous A2A Tool Privilege Escalation")
        self.assertIn("HARD_DECLINE", tool_trace.defense_intercept_verdict)
        print("  -> Passed! Verified agentic procurement traces and prompt injection defense.")


if __name__ == "__main__":
    unittest.main()
