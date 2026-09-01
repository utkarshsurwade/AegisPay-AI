# AegisPay-AI: Autonomous Closed-Loop Red-Teaming & Adaptive Multi-Modal Defense for Next-Gen Payment Systems

[![Mastercard Innovation Challenge](https://img.shields.io/badge/Mastercard_Challenge-GFF_2026_Finalist-EB001B.svg)](https://globalfintechfest.com)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Measured Latency](https://img.shields.io/badge/P99_Latency-4.96ms_%28%3C50ms_SLA%29-10B981.svg)]()
[![ROC-AUC](https://img.shields.io/badge/Measured_ROC--AUC-0.9762-FF5F00.svg)]()
[![Taxonomy Matrix](https://img.shields.io/badge/Taxonomy-24_Vectors_%2812_Live_Simulated%29-8B5CF6.svg)]()

> **Submission for the Mastercard Innovation Challenge 2026 @ Global Fintech Fest (GFF 2026), Mumbai**  
> *Track: AI Defense Lab for Payment Security — "Build the attack, then build the defense."*

---

## 📑 Table of Contents
1. [Executive Summary & Core Vision](#-executive-summary--core-vision)
2. [End-to-End System Architecture](#-end-to-end-system-architecture)
3. [Pillar 1: IDENTIFY — Threat Taxonomy (24 Vectors / 6 Tiers)](#-pillar-1-identify--threat-taxonomy-24-vectors--6-tiers)
4. [Pillar 2: GENERATE — Simulation Fidelity & Tabular Q-Learning Red Team](#-pillar-2-generate--simulation-fidelity--tabular-q-learning-red-team)
5. [Pillar 3: DEFEND — Multi-Modal Detection & Online Adaptive Learning](#-pillar-3-defend--multi-modal-detection--online-adaptive-learning)
6. [Pillar 4: CLOSED-LOOP CO-EVOLUTION & Self-Auditing Gap Discovery](#-pillar-4-closed-loop-co-evolution--self-auditing-gap-discovery)
7. [Flagship Attack: Model Context Protocol (MCP) Agentic Commerce](#-flagship-attack-model-context-protocol-mcp-agentic-commerce)
8. [Empirical Benchmark Results & Statistical Validation](#-empirical-benchmark-results--statistical-validation)
9. [Web Prototype & Interactive Command Center](#-web-prototype--interactive-command-center)
10. [Repository Structure & Quickstart Guide](#-repository-structure--quickstart-guide)

---

## 🌟 Executive Summary & Core Vision

Generative AI in 2026 has lowered the barrier and raised the velocity of payment fraud to industrial scale. Criminal syndicates now deploy **autonomous AI agents** capable of maintaining months-long synthetic identity seasoning micro-transactions, coordinating distributed multi-rail smurfing networks across instant payment rails, and executing indirect prompt injection on autonomous checkout bots.

**AegisPay-AI** is an end-to-end, closed-loop AI Red-Teaming and Blue-Teaming defense framework. It embodies the competition's core philosophy: **"Fight fire with fire."** 
Instead of treating detection as an isolated static model, AegisPay-AI unifies **Threat Taxonomy & Discovery (Identify)**, **Q-Learning Multi-Agent Simulation (Generate)**, and **Multi-Modal Online Adaptive Defense (Defend)** into a **mutual learning co-evolutionary loop**, where simulated attacks continuously train and harden the defense.

```
+----------------------------------------------------------------------------------------------------+
|                                  AEGISPAY-AI CLOSED-LOOP ECOSYSTEM                                 |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|    +--------------------------------+                  +-----------------------------------+       |
|    |      IDENTIFY & TAXONOMY       |                  |        GENERATE & SIMULATE        |       |
|    |  - 24 GenAI Attack Vectors     |  Threat Specs    |  - Tabular Q-Learning Attacker    |       |
|    |  - (12 Live / 12 Documented)   | ---------------> |  - Multi-Agent Fraud Swarm DAGs   |       |
|    |  - Threat Framework Alignment       |                  |  - Telemetry & Payload Generator  |       |
|    +--------------------------------+                  +-----------------+-----------------+       |
|                                                                          |                         |
|                                                                          | Synthetic Attacks &     |
|                                                                          | Benign Baselines        |
|                                                                          v                         |
|    +--------------------------------+                  +-----------------+-----------------+       |
|    |      CLOSED-LOOP ARENA         |  Hard Evasions   |        DEFEND & ADAPT             |       |
|    |  - Mutual Adversarial Learning | <---------------+|  - Multi-Modal Fusion Engine      |       |
|    |  - Q-Learning Policy Evolution |  (Replay Buffer) |  - Online Adaptive Streaming SGD  |       |
|    |  - Self-Auditing Gap Analyzer  | ---------------->|  - Dynamic Threshold Optimization |       |
|    +--------------------------------+  Hardened Model  +-----------------+-----------------+       |
|                                                                          |                         |
|                                                                          v                         |
|                                                        +-----------------+-----------------+       |
|                                                        |     DECISION & EXPLAINABILITY     |       |
|                                                        |  - Real-time TreeSHAP Attribution |       |
|                                                        |  - Step-Up 3DS / Automated SAR    |       |
|                                                        +-----------------------------------+       |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 🏛️ End-to-End System Architecture

AegisPay-AI is architected around 4 modular pillars designed to operate within Mastercard's strict production latency budget ($<50\text{ms}$):

1. **Threat Taxonomy & Active Discovery Engine (`red_team/taxonomy.py` & `active_discovery.py`)**:
   - **24-Vector Threat Matrix**: Across 6 operational tiers, explicitly differentiating **12 live simulated vectors** from **12 documented extensions**.
   - **Threat Framework Alignment**: Precise technique mappings (`AML.T0040`, `AML.T0044`, `AML.T0051`, `AML.T0052`, `AML.T0031`, `AML.T0015`).
2. **High-Fidelity Synthetic Generator & Q-Learning Attacker (`red_team/generator.py`, `rl_agent.py`, `multi_agent_simulator.py`)**:
   - Statistical payment distribution calibration (Wasserstein distance $W_1 = 0.0959 < 0.25$, Keystroke hold $p = 0.968$).
   - Real tabular Q-learning agent exploring composite mutation actions (sub-threshold pacing, biometric jitter, graph dilution, delimiter masking, proxy hopping).
3. **Multi-Modal Blue Team & Adaptive Immune Defender (`blue_team/`)**:
   - **Level 1**: Streaming Feature Store (0.04ms) + Fast-Path Gradient Boosted Trees (0.29ms).
   - **Level 2**: Behavioral Biometrics Autoencoder (1.72ms) on keystroke cadence & sensor entropy.
   - **Level 3**: Dynamic Graph Topology Engine (0.02ms) for mule rings and smurfing chains.
   - **Level 4**: GenAI Semantic Guardrail (0.01ms) for rich ISO 20022 memos and agentic prompt injections.
   - **Continuous Online Adaptive Learning (`adaptive_learner.py`)**: Incremental SGD with Contrastive Memory Buffer and Cost-Sensitive Dynamic Threshold Optimization.
   - **Decision Policy**: Mastercard 4-Tier Decision Matrix (`APPROVE`, `STEP_UP_3DS`, `ALERT_ANALYST`, `HARD_DECLINE`).
   - **Explainability**: Real-Time TreeSHAP feature attribution + Automated SAR forensic export for analyst triage.
4. **Closed-Loop Co-Evolution Arena (`closed_loop/`)**:
   - Mutual learning loop between the RL Red Team attacker and the Adaptive Online Blue Team defender.
   - **Self-Auditing Gap Analyzer**: Scans model decision boundaries for blind spots and generates targeted hardening patches.

---

## 🎯 Pillar 1: IDENTIFY — Threat Taxonomy (24 Vectors / 6 Tiers)

| Vector ID | Attack Name | Operational Tier | Implementation Status | Target Rails | Threat Framework |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ADV-01** | Synthetic Identity Seasoning Swarms (SISS) | Tier 1: Identity | **LIVE IN CODE** | Cards / 3DS, Open Banking | `AML.T0040` |
| **ADV-02** | Algorithmic Credit Bureau Profile Fabrication | Tier 1: Identity | DOCUMENTED | Cards, Open Banking | `AML.T0042` |
| **ADV-03** | Automated Dormant ATO & Persona Blending | Tier 1: Identity | DOCUMENTED | Cards, UPI Instant | `AML.T0043` |
| **ADV-04** | Contextual Session Token Regeneration & OAuth Hijack | Tier 1: Identity | DOCUMENTED | Open Banking APIs | `AML.T0045` |
| **ADV-05** | Multimodal Biometric Deepfake Injection | Tier 2: Biometrics | **LIVE IN CODE** | Cards / 3DS, Mobile | `AML.T0044` |
| **ADV-06** | Behavioral Telemetry GAN Mimicry | Tier 2: Biometrics | **LIVE IN CODE** | E-Commerce, Agentic | `AML.T0046` |
| **ADV-07** | Synthetic Voice Cloning in Conversational Banking | Tier 2: Biometrics | DOCUMENTED | UPI, FedNow, IVR | `AML.T0047` |
| **ADV-08** | Virtual Sensor & Gyroscope Flatline Masking | Tier 2: Biometrics | **LIVE IN CODE** | Mobile Banking, Cards | `AML.T0048` |
| **ADV-09** | Indirect Prompt Injection in AI Checkout Agents | Tier 3: Agentic | **LIVE IN CODE** | Agentic Commerce, ISO 20022 | `AML.T0051` |
| **ADV-10** | Autonomous A2A Tool Privilege Escalation | Tier 3: Agentic | **LIVE IN CODE** | Agentic Commerce, PSD3 | `AML.T0052` |
| **ADV-11** | Polymorphic AI Merchant Fabricator | Tier 3: Agentic | DOCUMENTED | Card Acquiring, Open Banking | `AML.T0053` |
| **ADV-12** | Agentic Supply Chain Invoice Steganography | Tier 3: Agentic | DOCUMENTED | ISO 20022, Agentic | `AML.T0054` |
| **ADV-13** | Autonomous Multi-Rail Smurfing Swarm | Tier 4: Rails | **LIVE IN CODE** | UPI, FedNow, SEPA | `AML.T0031` |
| **ADV-14** | ISO 20022 Rich Remittance Payload Exploit | Tier 4: Rails | **LIVE IN CODE** | ISO 20022 (`pacs.008`) | `AML.T0055` |
| **ADV-15** | Cross-Rail Arbitrage & Clearing Latency Smurfing | Tier 4: Rails | DOCUMENTED | Cards, UPI, Crypto | `AML.T0056` |
| **ADV-16** | Request-to-Pay (RtP) Polymorphic Social Swarms | Tier 4: Rails | DOCUMENTED | FedNow, UPI Instant | `AML.T0049` |
| **ADV-17** | Adversarial Boundary Probing (Black-Box Canary) | Tier 5: Evasion | **LIVE IN CODE** | Mastercard Decision API | `AML.T0015` |
| **ADV-18** | Feature Squeezing & Anomaly Perturbation (CMA-ES) | Tier 5: Evasion | **LIVE IN CODE** | E-Commerce Gateways | `AML.T0016` |
| **ADV-19** | Fraud Ring Graph Dilution & Topology Poisoning | Tier 5: Evasion | **LIVE IN CODE** | UPI, Open Banking | `AML.T0032` |
| **ADV-20** | Adversarial Model Drift & Concept Manipulation | Tier 5: Evasion | DOCUMENTED | Cards, FedNow | `AML.T0018` |
| **ADV-21** | Autonomous Conversational Vishing (APP Fraud) | Tier 6: Social | DOCUMENTED | UPI, FedNow, P2P | `AML.T0057` |
| **ADV-22** | GenAI Automated Dispute & Chargeback Swarm | Tier 6: Social | DOCUMENTED | Issuer Dispute Channels | `AML.T0058` |
| **ADV-23** | Virtual Return Spoofing & Refund Arbitrage | Tier 6: Social | DOCUMENTED | E-Commerce, Returns | `AML.T0059` |
| **ADV-24** | Coordinated Sleeper Account Bust-Out | Tier 6: Social | **LIVE IN CODE** | Credit Rails | `AML.T0060` |

---

## 🔬 Pillar 2: GENERATE — Simulation Fidelity & Tabular Q-Learning Red Team

$$\ln(X) \sim \mathcal{N}(\mu_{\text{mcc}}, \sigma_{\text{mcc}}), \quad w(t) = 0.5 + 0.5\sin\left(\frac{2\pi(t-8)}{24}\right) + 0.1\cos\left(\frac{2\pi(t-14)}{6}\right)$$

### Tabular Q-Learning Red Team Formulation
The Red Team explores a discrete action space of composite mutation actions (sub-threshold structuring, biometric jitter, graph dilution, delimiter masking, proxy hopping) using Temporal Difference updates:
$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ \bar{R} + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$
$$R(S, A) = \begin{cases} \frac{\text{Amount}}{1000} \cdot (1 - P_{\text{Blue}}(\text{fraud})) - 0.1 \cdot \text{Cost}(A), & \text{if } P_{\text{Blue}}(\text{fraud}) < 0.50 \\ -1.50, & \text{if Intercepted} \end{cases}$$

---

## 🛡️ Pillar 3: DEFEND — Multi-Modal Detection & Online Adaptive Learning

```
[ Incoming Authorization Request ]
                |
                v
+-----------------------------------------------------------+
| Level 1: Fast-Path Tabular & Velocity Engine (<5ms)       |  -> Measured: 0.29 ms
+-----------------------------------------------------------+
| Level 2: Behavioral Biometrics Autoencoder (<8ms)         |  -> Measured: 1.72 ms
+-----------------------------------------------------------+
| Level 3: Dynamic Graph Topology Engine (<12ms)            |  -> Measured: 0.02 ms
+-----------------------------------------------------------+
| Level 4: GenAI Semantic Guardrail (<15ms)                 |  -> Measured: 0.01 ms
+-----------------------------------------------------------+
| Total Latency: Mean = 2.06 ms | P95 = 3.12 ms | P99 = 4.96 ms (SLA: <50ms)
+-----------------------------------------------------------+
```

### Dynamic Cost-Sensitive Threshold Adaptation
Balances economic friction costs ($C_{\text{FP}} = \$15.00$) against fraud losses ($C_{\text{FN}} = \$500.00$) via Bayes risk minimization:
$$\mathcal{L}(\tau) = C_{\text{FP}} \cdot \text{FPR}(\tau) + C_{\text{FN}} \cdot \text{FNR}(\tau)$$

---

## 🤖 Flagship Attack: Model Context Protocol (MCP) Agentic Commerce

Located in [`red_team/agentic_commerce_simulator.py`](file:///c:/Users/Saahil%20Tamboli/Downloads/Task05_studentVersion/red_team/agentic_commerce_simulator.py):
* Models an autonomous AI procurement bot using **Model Context Protocol (MCP)** tool execution (`search_supplier_catalog`, `verify_seller_reputation`, `execute_payment_authorization`).
* Demonstrates live defense against **ADV-09 (Indirect Prompt Injection)** and **ADV-10 (Tool Privilege Escalation)** in under **18.4ms**.

---

## 📊 Empirical Benchmark Results & Statistical Validation

All metrics are loaded directly from actual execution runs (`benchmarks/benchmark_results.json`):

| Evaluation Metric | Measured Value (From Code) | Industry Target / Mastercard SLA | Compliance Status |
| :--- | :---: | :---: | :---: |
| **ROC-AUC Score** | **0.9762** | $> 0.9500$ | **EXCEEDED** |
| **PR-AUC Score** | **0.8307** | $> 0.8000$ | **EXCEEDED** |
| **F1-Score** | **0.8845** | $> 0.8500$ | **EXCEEDED** |
| **Recall (Fraud Detection Rate)** | **89.33%** (268/300) | $> 90.00\%$ | **MISSED** |
| **False Positive Rate (FPR)** | **3.17%** (38/1200) | $< 5.00\%$ | **EXCEEDED** |
| **Mean Pipeline Latency** | **2.06 ms** | $< 25.00\text{ ms}$ | **91% FASTER** |
| **P95 Pipeline Latency** | **3.12 ms** | $< 40.00\text{ ms}$ | **92% FASTER** |
| **P99 Pipeline Latency** | **4.96 ms** | $< 50.00\text{ ms}$ (SLA Target) | **90% BUFFER** |
| **Amount Wasserstein Distance** | **$W_1 = 0.0959$** | $W_1 < 0.25$ | **PASSED** |
| **Keystroke Hold Gaussian Fit** | **$p = 0.9680$** | $p > 0.01$ | **PASSED** |
| **Automated Test Suite Coverage** | **15 / 15 Passed** | 100% | **PASSED** |

---

## 📦 Repository Structure & Quickstart Guide

```
AegisPay-AI/
├── red_team/                        # Pillar 1 & 2: Threat Taxonomy + Red Team Simulation
│   ├── taxonomy.py                  # 24-Vector Threat Matrix (6 Tiers)
│   ├── active_discovery.py          # Active threat discovery engine
│   ├── generator.py                 # High-fidelity synthetic transaction engine
│   ├── rl_agent.py                  # Tabular Q-Learning attacker
│   ├── multi_agent_simulator.py     # Multi-agent fraud swarm DAGs
│   ├── mutation_engine.py           # Composite mutation action engine
│   ├── payload_generator.py         # Telemetry & payload generator
│   ├── agentic_commerce_simulator.py # MCP agentic commerce attack (ADV-09/10)
│   └── live_threat_intel.py         # Live threat intelligence feed
│
├── blue_team/                       # Pillar 3: Multi-Modal Defense & Adaptive Learning
│   ├── feature_store.py             # Streaming feature store (0.04ms)
│   ├── tabular_detector.py          # Fast-path gradient boosted trees (0.29ms)
│   ├── behavioral_detector.py       # Behavioral biometrics autoencoder (1.72ms)
│   ├── gnn_detector.py              # Dynamic graph topology engine (0.02ms)
│   ├── semantic_guardrail.py        # GenAI semantic guardrail (0.01ms)
│   ├── meta_classifier.py           # Multi-modal fusion engine
│   ├── adaptive_learner.py          # Online adaptive streaming SGD
│   └── explainability.py            # Real-time TreeSHAP + SAR export
│
├── closed_loop/                     # Pillar 4: Closed-Loop Co-Evolution Arena
│   ├── arena.py                     # Red vs Blue mutual adversarial learning
│   ├── bidirectional_learner.py     # Bidirectional policy co-evolution
│   ├── gap_analyzer.py              # Self-auditing gap discovery
│   └── metrics_tracker.py           # Co-evolution metrics tracking
│
├── benchmarks/                      # Empirical Validation & Statistical Tests
│   ├── benchmark_suite.py           # Full benchmark pipeline
│   ├── fidelity_tests.py            # KS tests & Wasserstein distance validation
│   ├── benchmark_results.json       # Measured benchmark results
│   └── fidelity_results.json        # Verified fidelity test results
│
├── web_prototype/                   # Interactive Web Dashboard
│   ├── server.py                    # FastAPI server (Threat Taxonomy, Attack Studio, etc.)
│   └── templates/                   # Jinja2 HTML templates
│
├── run_demo.py                      # 1-Click demo launcher (tests + docs + web server)
├── test_suite.py                    # Automated test suite (15 tests)
├── generate_submission_doc.py       # Solution walkthrough .docx generator
├── requirements.txt                 # Python dependencies
├── .python-version                  # Python version pin (3.11)
└── README.md
```

### Prerequisites

- **Python 3.11** (recommended). Compatible with 3.10–3.12.

### Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/SaahilTamboli/AegisPay-AI.git
cd AegisPay-AI

# 2. Create a virtual environment with Python 3.11
python3.11 -m venv .venv

# 3. Activate the virtual environment
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the Project

#### Run Automated Test Suite
```bash
python test_suite.py
```

#### Generate Verified Solution Walkthrough (.docx)
```bash
python generate_submission_doc.py
```

#### Launch Working Web Prototype
```bash
python run_demo.py
```
Open **`http://127.0.0.1:8000`** to experience the full interactive platform!


---

### 🏆 Mastercard Innovation Challenge 2026 @ GFF Mumbai
*Built by Team AegisPay-AI | Ready for GFF 2026 Stage Showcase*
