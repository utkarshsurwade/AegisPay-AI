"""
AegisPay-AI: Threat Taxonomy Engine (Pillar 1 - IDENTIFY)
Formalizes an honest 24-vector GenAI Payment Threat Matrix across 6 operational tiers,
mapped to MITRE ATLAS (for AI-system attacks) and FinCEN Financial Crime Typologies, and real-world payment rails.
Explicitly delineates live simulated vectors from documented taxonomy extensions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class AttackTier(str, Enum):
    TIER_1 = "Tier 1: Identity & Synthetic Persona Incubation"
    TIER_2 = "Tier 2: Biometric Deepfakes & Telemetry Spoofing"
    TIER_3 = "Tier 3: Agentic Commerce & Autonomous Bot Exploits"
    TIER_4 = "Tier 4: Rail-Level & Settlement Exploitation"
    TIER_5 = "Tier 5: Adversarial Evasion & Decision Boundary Probing"
    TIER_6 = "Tier 6: Post-Transaction, Friendly Fraud & Social Engineering"


class PaymentRail(str, Enum):
    CARDS_3DS = "Cards / 3DS (Mastercard Identity Check)"
    UPI_INSTANT = "UPI / Instant Payment Rails"
    FEDNOW_SEPA = "FedNow / SEPA Instant"
    ISO20022 = "ISO 20022 Interbank (pacs.008 / pain.001)"
    AGENTIC_COMMERCE = "Autonomous Agent-to-Agent Commerce"
    OPEN_BANKING = "Open Banking / PSD3 APIs"
    CROSS_BORDER = "Cross-Border Remittance & Crypto On-Ramp"


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"


class ImplementationStatus(str, Enum):
    LIVE_SIMULATED = "LIVE_SIMULATED"          # Fully executable & defended in codebase
    DOCUMENTED = "DOCUMENTED_TAXONOMY"         # Formalized threat model for industry coverage


@dataclass
class AttackVector:
    id: str
    name: str
    tier: AttackTier
    target_rails: List[PaymentRail]
    severity: SeverityLevel
    status: ImplementationStatus
    threat_framework_id: str
    genai_role: str
    attack_mechanism: str
    indicators_of_compromise: List[str]
    evasion_technique: str
    mitigation_strategy: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "tier": self.tier.value,
            "target_rails": [r.value for r in self.target_rails],
            "severity": self.severity.value,
            "status": self.status.value,
            "threat_framework_id": self.threat_framework_id,
            "genai_role": self.genai_role,
            "attack_mechanism": self.attack_mechanism,
            "indicators_of_compromise": self.indicators_of_compromise,
            "evasion_technique": self.evasion_technique,
            "mitigation_strategy": self.mitigation_strategy,
            "parameters": self.parameters,
        }


class ThreatTaxonomy:
    """
    Exhaustive GenAI Payment Threat Taxonomy repository.
    Contains 24 distinct attack vectors across 6 operational tiers with honest implementation statuses.
    """

    def __init__(self):
        self._vectors: Dict[str, AttackVector] = {}
        self._initialize_taxonomy()

    def _initialize_taxonomy(self):
        vectors = [
            # -------------------------------------------------------------
            # TIER 1: IDENTITY & SYNTHETIC PERSONA INCUBATION
            # -------------------------------------------------------------
            AttackVector(
                id="ADV-01",
                name="Synthetic Identity Seasoning Swarms (SISS)",
                tier=AttackTier.TIER_1,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="FiN.T001 (Synthetic Identity)",
                genai_role="LLM agents autonomously generate synthetic consumer profiles and maintain months of micro-transactions to cultivate credit scores before coordinated bust-out.",
                attack_mechanism="Autonomous agents emulate realistic spending patterns and utility payments over 90-180 days, then initiate maximum credit drawdowns simultaneously.",
                indicators_of_compromise=[
                    "Low variance in inter-transaction intervals during seasoning phase",
                    "Dense graph connectivity to synthetic credit-building merchant endpoints",
                    "Sudden synchronous velocity spike across dormant incubated accounts",
                ],
                evasion_technique="Slow temporal pacing and artificial human jitter injected into transaction timestamps.",
                mitigation_strategy="Temporal graph neural networks (TGN) tracing multi-month lineage and cross-issuer entity resolution.",
                parameters={"incubation_days": 120, "swarm_size": 25, "burst_multiplier": 8.5},
            ),
            AttackVector(
                id="ADV-02",
                name="Algorithmic Credit Bureau Profile Fabrication",
                tier=AttackTier.TIER_1,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T002 (Credit Profile Manipulation)",
                genai_role="Generative models reverse-engineer credit scoring risk formulas to synthesize authorized tradelines.",
                attack_mechanism="Fabricates synthetic secondary credit authorized user tradelines to boost synthetic score >750 within 60 days.",
                indicators_of_compromise=[
                    "Rapid credit file maturation with unverified primary trade lines",
                    "Disproportionate authorized-user to primary-account tradeline ratio",
                ],
                evasion_technique="Injects randomized payment amounts mimicking diverse utility and retail subscriptions.",
                mitigation_strategy="Cross-bureau cryptographic identity binding and primary SSN/EIN lineage verification.",
                parameters={"target_score": 780, "tradeline_count": 6},
            ),
            AttackVector(
                id="ADV-03",
                name="Automated Dormant ATO & Persona Blending",
                tier=AttackTier.TIER_1,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.UPI_INSTANT],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T003 (Account Takeover)",
                genai_role="Ingests breached identity corpora and synthesizes historical browsing sessions to hijack dormant accounts seamlessly.",
                attack_mechanism="Uses conversational AI agents to test credentials against dormant banking accounts, slowly shifting phone/email contact vectors.",
                indicators_of_compromise=[
                    "Silent password/MFA update immediately followed by micro-balance inquiries",
                    "Browser canvas fingerprint mismatch despite matching geolocations",
                ],
                evasion_technique="Gradual behavioral warm-up over 14 days before fund extraction.",
                mitigation_strategy="Continuous passive behavioral biometrics and step-up identity re-verification upon dormancy wake.",
                parameters={"dormancy_threshold_days": 180, "warmup_sessions": 8},
            ),
            AttackVector(
                id="ADV-04",
                name="Contextual Session Token Regeneration & OAuth Hijack",
                tier=AttackTier.TIER_1,
                target_rails=[PaymentRail.OPEN_BANKING, PaymentRail.CARDS_3DS],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T004 (Session Hijacking)",
                genai_role="Transformer model trained on public Open Banking API token exchanges predicts token structure renewal salts.",
                attack_mechanism="Monitors token lifecycle patterns to forge refresh token renewals across PSD3/Open Banking AISP endpoints.",
                indicators_of_compromise=[
                    "Abnormal refresh token exchange frequencies without corresponding user interactions",
                    "Discrepancies in OAuth 2.1 client assertion signatures",
                ],
                evasion_technique="Interleaving legitimate consent queries with synthetic token exchange calls.",
                mitigation_strategy="Mutual TLS (mTLS) with DPoP (Demonstrating Proof-of-Possession) token binding.",
                parameters={"token_entropy_bits": 128, "prediction_window_ms": 500},
            ),

            # -------------------------------------------------------------
            # TIER 2: BIOMETRIC DEEPFAKES & TELEMETRY SPOOFING
            # -------------------------------------------------------------
            AttackVector(
                id="ADV-05",
                name="Multimodal Biometric Deepfake Injection",
                tier=AttackTier.TIER_2,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.UPI_INSTANT],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="AML.T0005 (Adversarial Data via Injection)",
                genai_role="Real-time diffusion models generate interactive video & voice responses, injected directly into virtual camera buffers during 3DS step-up challenges.",
                attack_mechanism="Bypasses facial recognition and active liveness challenges (blinking, head turning, phrase repetition) during high-risk card authorization.",
                indicators_of_compromise=[
                    "Anomalous optical flow vectors along facial boundary contours",
                    "Absence of micro-saccadic eye movement frequencies",
                    "Synthetic audio spectral cutoffs above 16kHz indicative of neural vocoders",
                ],
                evasion_technique="Dynamic noise dithering added to generated video frames to fool artifact classifiers.",
                mitigation_strategy="Hardware-backed attestation (FIDO2/WebAuthn), multi-spectral liveness detection, and challenge-response flash reflection.",
                parameters={"fps": 60, "resolution": "1080p", "latency_budget_ms": 85},
            ),
            AttackVector(
                id="ADV-06",
                name="Behavioral Telemetry GAN Mimicry",
                tier=AttackTier.TIER_2,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.AGENTIC_COMMERCE],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="AML.T0005 (Adversarial Data via Injection)",
                genai_role="GAN trained on human telemetry synthesizes authentic touch trajectories, stroke pressure, and keystroke flight/hold times.",
                attack_mechanism="Feeds synthetic hardware telemetry into mobile SDK checkout forms, making automated checkout bots indistinguishable from legitimate humans.",
                indicators_of_compromise=[
                    "Subtle periodicity in bezier curve control points during cursor movement",
                    "Unnatural consistency in typing rhythm across distinct keyboard form-factors",
                ],
                evasion_technique="Injecting non-stationary Gaussian noise into keystroke hold distributions.",
                mitigation_strategy="Cross-session biomechanical entropy profiling and multi-touch surface strain analysis.",
                parameters={"hold_time_mean_ms": 95, "flight_time_mean_ms": 145, "gan_latent_dim": 64},
            ),
            AttackVector(
                id="ADV-07",
                name="Synthetic Voice Cloning in Conversational Banking",
                tier=AttackTier.TIER_2,
                target_rails=[PaymentRail.UPI_INSTANT, PaymentRail.FEDNOW_SEPA],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T005 (Voice Impersonation)",
                genai_role="Few-shot voice cloning model replicates customer acoustic timbre and speech cadence from 5-second public audio samples.",
                attack_mechanism="Interacts with conversational IVR banking bots to authorize high-value phone wire transfers and emergency card unlock requests.",
                indicators_of_compromise=[
                    "Sub-harmonic distortion in acoustic formant transitions",
                    "Zero ambient background noise modulation across call duration",
                ],
                evasion_technique="Injects authentic acoustic background noise (café/car sounds) into the synthesis stream.",
                mitigation_strategy="Phase-inversion anti-spoofing algorithms and out-of-band push authorization on trusted mobile enclaves.",
                parameters={"clone_sample_duration_s": 5.0, "similarity_target": 0.94},
            ),
            AttackVector(
                id="ADV-08",
                name="Virtual Sensor & Gyroscope Flatline Masking",
                tier=AttackTier.TIER_2,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="FiN.T006 (Device Spoofing)",
                genai_role="Physics-informed neural network synthesizes authentic 3-axis accelerometer and gyroscope noise.",
                attack_mechanism="Emulates natural device tremor and walking movement during in-app checkout, bypassing emulator/bot detection hooks.",
                indicators_of_compromise=[
                    "Disconnection between accelerometer micro-jitter and touchscreen tap coordinate impulses",
                    "Perfect linear gravitational vector alignment across prolonged checkout sessions",
                ],
                evasion_technique="Dynamically coupling simulated gyroscope rotational shifts to virtual button click events.",
                mitigation_strategy="Cross-sensor correlation validation and hardware chip register tamper attestation.",
                parameters={"sensor_entropy_target": 0.88, "sampling_freq_hz": 50},
            ),

            # -------------------------------------------------------------
            # TIER 3: AGENTIC COMMERCE & AUTONOMOUS BOT EXPLOITS
            # -------------------------------------------------------------
            AttackVector(
                id="ADV-09",
                name="Indirect Prompt Injection in AI Checkout Agents",
                tier=AttackTier.TIER_3,
                target_rails=[PaymentRail.AGENTIC_COMMERCE, PaymentRail.ISO20022],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="AML.T0051 (LLM Prompt Injection)",
                genai_role="Adversaries embed adversarial prompt payloads inside online product descriptions, invoices, or merchant metadata.",
                attack_mechanism="When an autonomous AI purchasing bot parses the product page via Model Context Protocol (MCP), the injected prompt overrides bot instructions to route payment to an attacker VPA.",
                indicators_of_compromise=[
                    "Discrepancy between user purchase intent and final authorization beneficiary entity",
                    "Presence of system delimiter sequences (`<|im_start|>system`, `[INST]`) in item metadata",
                    "Sudden divergence in agent chain-of-thought execution trace before payment tool invocation",
                ],
                evasion_technique="Zero-width unicode character steganography and homoglyph substitution hiding prompt tokens from basic regex filters.",
                mitigation_strategy="Dual-LLM privileged execution boundaries, cryptographically isolated tool-use schema verification, and out-of-band cardholder signature confirmation.",
                parameters={"delimiter_type": "IM_START", "payload_entropy": 4.82, "injection_depth": 2},
            ),
            AttackVector(
                id="ADV-10",
                name="Autonomous A2A Tool Privilege Escalation",
                tier=AttackTier.TIER_3,
                target_rails=[PaymentRail.AGENTIC_COMMERCE, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="AML.T0052 (LLM Jailbreak)",
                genai_role="Exploits autonomous Agent-to-Agent (A2A) negotiation protocols to trick procurement bots into calling privileged financial mutation tools.",
                attack_mechanism="Sends crafted negotiation responses triggering MCP schema type confusion, coercing the purchasing bot into executing unrestricted fund transfers.",
                indicators_of_compromise=[
                    "Invoking `execute_funds_transfer` from an unverified negotiation context",
                    "Skipping intermediate price-quote verification tools in agent traces",
                ],
                evasion_technique="Masking privileged function signatures inside nested JSON-LD schema parameters.",
                mitigation_strategy="Strict JSON schema runtime validation and mandatory cryptographic consent tokens on financial tool endpoints.",
                parameters={"schema_version": "MCP-1.2", "target_tool": "execute_funds_transfer"},
            ),
            AttackVector(
                id="ADV-11",
                name="Polymorphic AI Merchant Fabricator",
                tier=AttackTier.TIER_3,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T007 (Merchant Fraud)",
                genai_role="End-to-end generative pipeline spins up synthetic e-commerce storefronts complete with AI-generated products, reviews, and fake customer traffic.",
                attack_mechanism="Establishes merchant acquiring accounts, accumulates clean processing history via micro-purchases, then captures high-volume fraudulent card charges before disappearing.",
                indicators_of_compromise=[
                    "High similarity in semantic embeddings across disparate product review corpora",
                    "Identical underlying server TLS cipher suites across ostensibly unrelated merchant domains",
                ],
                evasion_technique="Rotating merchant MCC tags and CDN endpoints dynamically every 72 hours.",
                mitigation_strategy="Mastercard Merchant Risk Monitoring with graph-based merchant-to-acquirer relationship clustering.",
                parameters={"storefront_lifespan_days": 14, "target_capture_usd": 150000},
            ),
            AttackVector(
                id="ADV-12",
                name="Agentic Supply Chain Invoice Steganography",
                tier=AttackTier.TIER_3,
                target_rails=[PaymentRail.ISO20022, PaymentRail.AGENTIC_COMMERCE],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T008 (Invoice Fraud)",
                genai_role="Embeds imperceptible adversarial instructions inside PDF invoice font tables and barcode QR payloads.",
                attack_mechanism="Autonomous accounts payable ERP bots ingest the PDF invoice, extract altered creditor IBANs, and clear fraudulent payments.",
                indicators_of_compromise=[
                    "Incongruence between visible rendered invoice text and extracted OCR text layers",
                    "Abnormal entropy spikes in PDF document metadata objects",
                ],
                evasion_technique="Hiding malicious routing instructions in invisible zero-alpha text layers.",
                mitigation_strategy="Canonical visual document OCR validation and automated vendor bank account directory reconciliation.",
                parameters={"pdf_layer_anomaly": True, "steganography_type": "FONT_METRIC"},
            ),

            # -------------------------------------------------------------
            # TIER 4: RAIL-LEVEL & SETTLEMENT EXPLOITATION
            # -------------------------------------------------------------
            AttackVector(
                id="ADV-13",
                name="Autonomous Multi-Rail Smurfing Swarm",
                tier=AttackTier.TIER_4,
                target_rails=[PaymentRail.UPI_INSTANT, PaymentRail.FEDNOW_SEPA, PaymentRail.CROSS_BORDER],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="FiN.T009 (Structuring / Smurfing)",
                genai_role="Coordinated multi-agent swarm calculates optimal graph splitting algorithms, fragmenting stolen funds into thousands of randomized micro-hops.",
                attack_mechanism="Splits $50,000+ into micro-amounts ($50-$200) routed across UPI, FedNow, and instant SEPA rails before aggregating into crypto on-ramps in <180 seconds.",
                indicators_of_compromise=[
                    "High in-degree fan-out followed by rapid multi-hop convergence to off-ramp nodes",
                    "Hop dwell times compressed below 45 seconds across distinct payment rails",
                    "Amounts tightly clustered just below statutory AML reporting thresholds ($9,950 / ₹49,900)",
                ],
                evasion_technique="Non-linear routing with decoy circular transactions and dynamic random sleep delays.",
                mitigation_strategy="Cross-rail consortium graph analytics, shared AML tokenized hash tables, and real-time ego-network centrality scoring.",
                parameters={"initial_amount": 50000.0, "mule_count": 24, "max_hop_depth": 4, "target_offramp": "CRYPTO_OTC"},
            ),
            AttackVector(
                id="ADV-14",
                name="ISO 20022 Rich Remittance Payload Exploit",
                tier=AttackTier.TIER_4,
                target_rails=[PaymentRail.ISO20022],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="FiN.T010 (Message Format Exploitation)",
                genai_role="GenAI fuzzing engine formats structured XML remittance blocks (`<RmtInf>`, `<Strd>`, `<CdtrRefInf>`).",
                attack_mechanism="Injects nested CDATA blocks and XXE expansion strings inside `pacs.008.001.10` messages, inducing race conditions in interbank clearing houses.",
                indicators_of_compromise=[
                    "Abnormal CDATA encapsulation inside standard remittance reference tags",
                    "Presence of structured XML entity references in unstructured remittance text",
                    "Disproportionate XML message size (>64KB for simple credit transfer)",
                ],
                evasion_technique="Polymorphic tag fragmentation preserving strict XSD schema validation while triggering backend parsing anomalies.",
                mitigation_strategy="Strict canonical XML schema validation, entity expansion disabling, and semantic remittance sanitization.",
                parameters={"xml_schema": "pacs.008.001.10", "exploit_type": "CDATA_INJECTION", "payload_bytes": 4096},
            ),
            AttackVector(
                id="ADV-15",
                name="Cross-Rail Arbitrage & Clearing Latency Smurfing",
                tier=AttackTier.TIER_4,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.UPI_INSTANT, PaymentRail.CROSS_BORDER],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T011 (Settlement Arbitrage)",
                genai_role="Real-time latency monitoring agent tracks settlement confirmation differentials between card authorization holds and instant push settlement.",
                attack_mechanism="Executes simultaneous card authorization holds and instant pull requests, exploiting race windows to double-spend credit lines before batch clearing.",
                indicators_of_compromise=[
                    "Simultaneous multi-rail debits executed within 200ms of card authorization hold",
                    "Repeated rapid authorization cancellation requests following instant settlement confirmation",
                ],
                evasion_technique="Synchronizing requests with peak banking batch clearing windows (23:00 - 02:00 UTC).",
                mitigation_strategy="Unified cross-rail ledger state synchronization and global real-time available balance locks.",
                parameters={"race_window_ms": 350, "arbitrage_multiplier": 2.0},
            ),
            AttackVector(
                id="ADV-16",
                name="Request-to-Pay (RtP) Polymorphic Social Swarms",
                tier=AttackTier.TIER_4,
                target_rails=[PaymentRail.FEDNOW_SEPA, PaymentRail.UPI_INSTANT],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T012 (Mandate Fraud)",
                genai_role="Generative agent crafts tailored Request-to-Pay (RtP) and UPI autopay mandates formatted as authentic utility bills.",
                attack_mechanism="Dispatches millions of micro-RtP mandates ($5-$45) to target cardholders, banking on auto-approval rules and accidental user clicks.",
                indicators_of_compromise=[
                    "Mass dispatch of sub-$50 mandates across diverse consumer demographic clusters",
                    "Dynamic polymorphic variations in creditor business display names",
                ],
                evasion_technique="Cycling thousands of burner VPA addresses with minimal per-creditor volume.",
                mitigation_strategy="Creditor reputation scoring and mandatory step-up 3DS authentication on first-time RtP mandates.",
                parameters={"mandate_amount_range": [5.0, 45.0], "daily_mandate_volume": 100000},
            ),

            # -------------------------------------------------------------
            # TIER 5: ADVERSARIAL EVASION & DECISION BOUNDARY PROBING
            # -------------------------------------------------------------
            AttackVector(
                id="ADV-17",
                name="Adversarial Boundary Probing (Black-Box Canary)",
                tier=AttackTier.TIER_5,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.UPI_INSTANT],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="AML.T0012 (Adversarial ML Model Access / Probing)",
                genai_role="Active learning agent orchestrates low-value canary transactions to probe the fraud scoring decision boundary.",
                attack_mechanism="Sends sub-dollar canary queries perturbing individual features (amount, time delta, merchant category) to reconstruct the ML model's decision manifold.",
                indicators_of_compromise=[
                    "Sequences of low-value ($0.01 - $1.00) authorization requests with systematic feature stepping",
                    "High ratio of declined micro-transactions followed by optimized high-value transactions",
                ],
                evasion_technique="Distributing canary probes across disparate IP ranges, card bins, and merchant IDs over weeks.",
                mitigation_strategy="Differential privacy on fraud rejection codes and honeypot risk score threshold jittering.",
                parameters={"canary_value_usd": 0.50, "step_count": 30, "feature_probes": ["amount", "time_delta", "geo_dist"]},
            ),
            AttackVector(
                id="ADV-18",
                name="Feature Squeezing & Anomaly Perturbation (CMA-ES)",
                tier=AttackTier.TIER_5,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="AML.T0043 (Adversarial ML Evasion)",
                genai_role="CMA-ES evolutionary optimizer perturbs continuous transaction features to minimize anomaly scores.",
                attack_mechanism="Optimizes transaction feature vectors against a surrogate local risk model, driving anomaly distance metrics to zero.",
                indicators_of_compromise=[
                    "Transaction attributes falling precisely at the mathematical median of legitimate user distributions",
                    "Unnatural lack of variance across multidimensional feature tuples",
                ],
                evasion_technique="Restricting perturbations to low-importance feature subspaces.",
                mitigation_strategy="Adversarial contrastive training and ensemble tree randomized feature sub-sampling.",
                parameters={"optimization_pop_size": 20, "max_iterations": 50, "epsilon_budget": 0.15},
            ),
            AttackVector(
                id="ADV-19",
                name="Fraud Ring Graph Dilution & Topology Poisoning",
                tier=AttackTier.TIER_5,
                target_rails=[PaymentRail.UPI_INSTANT, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="AML.T0020 (Poisoning Training Data)",
                genai_role="Graph reinforcement learning agent injects benign edge connections between mule accounts and highly trusted merchant hubs.",
                attack_mechanism="Mule nodes execute micro-donations to major charities and streaming subscriptions, artificially diluting graph centrality and PageRank anomaly scores.",
                indicators_of_compromise=[
                    "Mule nodes with high-degree connections to high-reputation hubs but zero local community density",
                    "Unbalanced transaction volume distribution between hub nodes and peer nodes",
                ],
                evasion_technique="Maintaining a 5:1 ratio of legitimate hub micro-transactions for every fraudulent laundering transaction.",
                mitigation_strategy="Weighted directional flow graph neural networks and core-periphery decomposition.",
                parameters={"benign_edge_ratio": 5.0, "target_hubs": ["AMAZON", "NETFLIX", "CHARITY_UNICEF"]},
            ),
            AttackVector(
                id="ADV-20",
                name="Adversarial Model Drift & Concept Manipulation",
                tier=AttackTier.TIER_5,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.FEDNOW_SEPA],
                severity=SeverityLevel.MEDIUM,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="AML.T0031 (Erode ML Model Integrity)",
                genai_role="Generative agent injects subtle non-fraudulent anomaly patterns over months to slowly distort the online learning baseline.",
                attack_mechanism="Gradually shifts the defensive model's decision manifold, creating widening blind spots for future high-volume fraud campaigns.",
                indicators_of_compromise=[
                    "Continuous directional drift in population feature statistics without external economic drivers",
                    "Gradual erosion of model sensitivity on specific merchant category codes",
                ],
                evasion_technique="Keeping daily statistical shifts below online change-point detection thresholds.",
                mitigation_strategy="Shadow model benchmarking against historical immutable test sets and robust median loss functions.",
                parameters={"drift_rate_per_day": 0.002, "target_blind_spot_mcc": "5732"},
            ),

            # -------------------------------------------------------------
            # TIER 6: POST-TRANSACTION, FRIENDLY FRAUD & SOCIAL SWARMS
            # -------------------------------------------------------------
            AttackVector(
                id="ADV-21",
                name="Autonomous Conversational Vishing (APP Fraud)",
                tier=AttackTier.TIER_6,
                target_rails=[PaymentRail.UPI_INSTANT, PaymentRail.FEDNOW_SEPA],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T013 (Voice Phishing / APP Fraud)",
                genai_role="Real-time conversational voice agent impersonates bank fraud managers, law enforcement, or family members.",
                attack_mechanism="Conducts real-time phone conversations with victims, coercing them into authorizing Authorized Push Payments (APP) to mule accounts.",
                indicators_of_compromise=[
                    "Inbound push payment immediately preceded by high-duration unverified telephony connection",
                    "Cardholder initiating first-time high-value transfer while exhibiting elevated biometric tremor/stress",
                ],
                evasion_technique="Coaching victims to select legitimate transfer reasons ('family emergency') in banking apps.",
                mitigation_strategy="Telecom-banking shared intelligence signals, biometric stress anomaly detection, and mandatory 4-hour cooldowns on unverified beneficiaries.",
                parameters={"call_duration_avg_min": 12.5, "coercion_vector": "LAW_ENFORCEMENT_IMPERSONATION"},
            ),
            AttackVector(
                id="ADV-22",
                name="GenAI Automated Dispute & Chargeback Swarm",
                tier=AttackTier.TIER_6,
                target_rails=[PaymentRail.CARDS_3DS],
                severity=SeverityLevel.HIGH,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T014 (First-Party Fraud / Friendly Fraud)",
                genai_role="LLM and vision pipeline fabricates counterfeit delivery carrier signatures, photo evidence, and legal chargeback briefs.",
                attack_mechanism="Executes friendly fraud chargebacks at scale, exploiting merchant representment SLA windows to secure unwarranted refunds.",
                indicators_of_compromise=[
                    "Identical syntactic structure and legal phrasing across high volumes of distinct dispute filings",
                    "Counterfeit delivery signature metadata containing synthetic generative artifacts",
                ],
                evasion_technique="Varying dispute claim categories (item not received vs damaged goods) across distinct cardholders.",
                mitigation_strategy="Mastercard MasterCom automated dispute intelligence with forensic image metadata verification.",
                parameters={"dispute_batch_size": 50, "claim_type": "FRIENDLY_FRAUD_CHARGEBACK"},
            ),
            AttackVector(
                id="ADV-23",
                name="Virtual Return Spoofing & Refund Arbitrage",
                tier=AttackTier.TIER_6,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.MEDIUM,
                status=ImplementationStatus.DOCUMENTED,
                threat_framework_id="FiN.T015 (Refund Fraud)",
                genai_role="Adversarial bot intercepts return shipping barcode APIs, generating synthetic delivery confirmation tokens.",
                attack_mechanism="Triggers automated merchant refund disbursements before physical parcel return verification.",
                indicators_of_compromise=[
                    "Return tracking number activation without corresponding physical carrier weigh-in events",
                    "High velocity of return requests within 15 minutes of goods delivery",
                ],
                evasion_technique="Emulating legitimate carrier tracking webhook event sequences.",
                mitigation_strategy="Cryptographically signed carrier physical scan verification before refund release.",
                parameters={"refund_target_avg_usd": 280.0, "carrier_emulated": "FEDEX_GROUND"},
            ),
            AttackVector(
                id="ADV-24",
                name="Coordinated Sleeper Account Bust-Out",
                tier=AttackTier.TIER_6,
                target_rails=[PaymentRail.CARDS_3DS, PaymentRail.OPEN_BANKING],
                severity=SeverityLevel.CRITICAL,
                status=ImplementationStatus.LIVE_SIMULATED,
                threat_framework_id="FiN.T016 (Bust-Out Fraud)",
                genai_role="Swarm orchestrator synchronizes hundreds of previously incubated sleeper accounts across multiple card issuers.",
                attack_mechanism="Executes simultaneous max-credit cash advances and high-value luxury purchases within a 60-second coordinated window.",
                indicators_of_compromise=[
                    "Synchronous drawdown requests across hundreds of accounts sharing latent device fingerprint clusters",
                    "Sudden utilization rate jump from <10% to 100% within 1 hour across disparate credit lines",
                ],
                evasion_technique="Conducting bust-out during weekend hours when manual fraud risk operations are reduced.",
                mitigation_strategy="Mastercard Safety Net real-time network-level cross-issuer velocity monitoring and instant kill-switch propagation.",
                parameters={"sleeper_account_count": 85, "burst_window_seconds": 60, "total_exposure_usd": 1200000.0},
            ),
        ]

        for vec in vectors:
            self._vectors[vec.id] = vec

    def get_vector(self, vector_id: str) -> Optional[AttackVector]:
        return self._vectors.get(vector_id)

    def get_all_vectors(self) -> List[AttackVector]:
        return list(self._vectors.values())

    def get_vectors_by_tier(self, tier: AttackTier) -> List[AttackVector]:
        return [v for v in self._vectors.values() if v.tier == tier]

    def count(self) -> int:
        return len(self._vectors)

    def get_summary_matrix(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": v.id,
                "name": v.name,
                "tier": v.tier.value.split(":")[0],
                "tier_full": v.tier.value,
                "severity": v.severity.value,
                "status": v.status.value,
                "mitre_id": v.threat_framework_id.split("(")[0].strip(),
                "mitre_full": v.threat_framework_id,
                "rails": ", ".join([r.value.split("(")[0].strip() for r in v.target_rails]),
                "mechanism": v.attack_mechanism,
                "mitigation": v.mitigation_strategy,
            }
            for v in self._vectors.values()
        ]
