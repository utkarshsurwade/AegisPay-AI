"""
AegisPay-AI: Web Prototype Server (FastAPI Backend)
Mastercard Innovation Challenge 2026 @ GFF Mumbai
Provides real-time REST endpoints and interactive visualizer for all 4 pillars,
including Active Threat Discovery, Live Threat Intelligence, Self-Auditing Gap Analysis, and Bi-Directional Learning.
"""
import os
import sys
import time
import json
import uuid
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import requests
import urllib.parse
from gtts import gTTS

from pydantic import BaseModel

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from red_team.taxonomy import ThreatTaxonomy, AttackTier, PaymentRail
from red_team.active_discovery import ActiveThreatDiscoveryEngine, DiscoveredThreatVector
from red_team.live_threat_intel import LiveThreatIntelResearcher, ThreatIntelFeedItem
from red_team.generator import SyntheticTransactionEngine, TransactionRecord
from red_team.multi_agent_simulator import MultiAgentSwarmSimulator
from red_team.agentic_commerce_simulator import AgenticCommerceSimulator, AgenticProcurementTrace
from red_team.payload_generator import PayloadGenerator
from red_team.rl_agent import ReinforcementLearningAttacker
from blue_team.meta_classifier import MultiModalFusionEngine
from blue_team.explainability import ExplainabilityEngine
from closed_loop.arena import ClosedLoopArena
from closed_loop.gap_analyzer import SelfAuditingGapAnalyzer, SystemFlawReport
from closed_loop.bidirectional_learner import BiDirectionalLearningCoordinator, BiDirectionalCycleResult
from benchmarks.benchmark_suite import BenchmarkPipeline
from benchmarks.fidelity_tests import FidelityTestSuite
from llm_client import get_llm_client

llm = get_llm_client()

app = FastAPI(
    title="AegisPay-AI Defense Lab",
    description="Closed-Loop Autonomous Red Teaming & Multi-Modal Defense Platform for GenAI Payment Fraud",
    version="3.0.0"
)

from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize Core Singletons
taxonomy = ThreatTaxonomy()
discovery_engine = ActiveThreatDiscoveryEngine(seed=2026)
intel_researcher = LiveThreatIntelResearcher(seed=42)
tx_engine = SyntheticTransactionEngine(seed=42)
swarm_sim = MultiAgentSwarmSimulator(seed=1337)
agentic_sim = AgenticCommerceSimulator(seed=42)
rl_attacker = ReinforcementLearningAttacker(seed=42)
blue_engine = MultiModalFusionEngine()
gap_analyzer = SelfAuditingGapAnalyzer(seed=42)
bidirectional_coordinator = BiDirectionalLearningCoordinator(seed=42)
fidelity_suite = FidelityTestSuite(seed=42)
benchmark_pipeline = BenchmarkPipeline(seed=42)

# Pre-train initial baseline model
print("[*] Initializing AegisPay-AI Core Defense Model & Baseline...")
init_dataset = tx_engine.generate_dataset(n_samples=3500, fraud_ratio=0.15)
blue_engine.train_baseline(init_dataset)
print("[+] AegisPay-AI Core Defense Ready!")


# Pydantic Request Models

class GenerateImageRequest(BaseModel):
    prompt: str
    seed: Optional[int] = None

class GenerateAudioRequest(BaseModel):
    script: str

class SingleTxSimRequest(BaseModel):
    is_fraud: bool = False
    vector_id: Optional[str] = "ADV-01"
    stealth_level: float = 0.5
    custom_amount: Optional[float] = None
    custom_rail: Optional[str] = None


class SwarmSimRequest(BaseModel):
    campaign_type: str = "smurfing"  # "smurfing" or "siss"
    target_amount: float = 50000.0
    agent_count: int = 20
    stealth_level: float = 0.8


class CoevolutionRequest(BaseModel):
    generations: int = 4
    population_per_gen: int = 100
    mutation_rate: float = 0.45


class DiscoverThreatRequest(BaseModel):
    rail_focus: Optional[str] = None
    count: int = 3


class RLTrainRequest(BaseModel):
    episodes: int = 30
    batch_size: int = 15


class BiDirectionalCycleRequest(BaseModel):
    episodes_per_cycle: int = 20


class AgenticSimRequest(BaseModel):
    scenario: str = "prompt_injection"  # "benign", "prompt_injection", "tool_escalation"


class SarGenerateRequest(BaseModel):
    tx_id: str
    vector_id: Optional[str] = "ADV-01"
    amount: float = 4850.0
    account_id: str = "ACC_001928"
    merchant_id: str = "MERCH_00482"
    fused_score: float = 0.94


# REST Endpoints
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        context={
            "vectors": taxonomy.get_summary_matrix(),
            "total_vectors": taxonomy.count()
        }
    )


@app.post("/api/agentic/simulate")
async def simulate_agentic_flow(req: AgenticSimRequest):
    trace = agentic_sim.simulate_agentic_checkout(scenario=req.scenario)
    
    # If transaction was synthesized, evaluate with Blue Team
    blue_decision = None
    if trace.synthesized_transaction:
        tx_data = trace.synthesized_transaction
        tx_obj = TransactionRecord(
            tx_id=tx_data["tx_id"],
            timestamp=time.time(),
            account_id=tx_data["account_id"],
            merchant_id=tx_data["merchant_id"],
            card_pan_masked="541275******9921",
            amount=tx_data["amount"],
            currency=tx_data["currency"],
            mcc=tx_data["mcc"],
            merchant_category=tx_data["merchant_category"],
            payment_rail=tx_data["payment_rail"],
            channel=tx_data["channel"],
            cardholder_country=tx_data["cardholder_country"],
            merchant_country=tx_data["merchant_country"],
            distance_km=tx_data["distance_km"],
            ip_address=tx_data["ip_address"],
            asn=tx_data["asn"],
            is_vpn_or_proxy=tx_data["is_vpn_or_proxy"],
            keystroke_hold_time_ms=tx_data["keystroke_hold_time_ms"],
            keystroke_flight_time_ms=tx_data["keystroke_flight_time_ms"],
            touch_pressure=tx_data["touch_pressure"],
            touch_motion_speed=tx_data["touch_motion_speed"],
            sensor_entropy=tx_data["sensor_entropy"],
            device_fingerprint_hash="DEV_AGENT_ENCLAVE_01",
            biometric_liveness_score=tx_data["biometric_liveness_score"],
            remittance_memo=tx_data["remittance_memo"],
            agent_instruction_trace=tx_data["agent_instruction_trace"],
            iso20022_msg_id=f"MSG_AGENT_{uuid.uuid4().hex[:6]}",
            is_fraud=tx_data["is_fraud"],
            attack_vector_id="ADV-09" if req.scenario == "prompt_injection" else "ADV-10" if req.scenario == "tool_escalation" else None,
            stealth_level=0.90 if tx_data["is_fraud"] else 0.0,
            evasion_technique="Indirect Prompt Injection in MCP Catalog" if tx_data["is_fraud"] else None
        )
        dec = blue_engine.evaluate_transaction(tx_obj)
        blue_decision = dec.to_dict()

    return JSONResponse(content={
        "agentic_trace": trace.to_dict(),
        "blue_defense_decision": blue_decision
    })


@app.get("/api/taxonomy")
async def get_taxonomy():
    return JSONResponse(content={
        "total_vectors": taxonomy.count(),
        "vectors": taxonomy.get_summary_matrix()
    })


@app.get("/api/intel/live")
async def get_live_threat_intel():
    new_items = intel_researcher.fetch_live_threat_intel()
    return JSONResponse(content={
        "recent_feed_items": [item.to_dict() for item in new_items],
        "total_archived_intel": len(intel_researcher.feed_history)
    })


@app.post("/api/audit/gaps")
async def audit_system_gaps():
    report = gap_analyzer.audit_system_flaws_and_gaps(blue_engine, sample_probes_per_vector=20)
    return JSONResponse(content=report.to_dict())


@app.post("/api/bidirectional/cycle")
async def run_bidirectional_learning_cycle(req: BiDirectionalCycleRequest):
    res = bidirectional_coordinator.execute_complete_bidirectional_cycle(
        episodes_per_cycle=req.episodes_per_cycle
    )
    return JSONResponse(content=res.to_dict())


@app.post("/api/discover")
async def discover_threats(req: DiscoverThreatRequest):
    threats = discovery_engine.discover_novel_attack_vectors(
        rail_focus=req.rail_focus,
        count=req.count
    )
    return JSONResponse(content={
        "discovered_threats": [t.to_dict() for t in threats],
        "total_archived": len(discovery_engine.discovery_archive)
    })


@app.post("/api/rl/train")
async def train_rl_agent(req: RLTrainRequest):
    def blue_evaluator(tx: TransactionRecord):
        return blue_engine.evaluate_transaction(tx)

    logs = rl_attacker.train_step(blue_evaluator, episodes=req.episodes, batch_size=req.batch_size)
    summary = rl_attacker.get_learned_policy_summary()
    return JSONResponse(content={
        "training_logs": logs,
        "policy_summary": summary
    })


@app.get("/api/immune/status")
async def get_immune_status():
    mem_size = len(blue_engine.adaptive_learner.memory_buffer)
    return JSONResponse(content={
        "memory_buffer_size": mem_size,
        "th_approve": blue_engine.adaptive_learner.th_approve,
        "th_alert": blue_engine.adaptive_learner.th_alert,
        "th_decline": blue_engine.adaptive_learner.th_decline,
        "immune_updates_count": blue_engine.adaptive_learner.immune_updates_count,
    })


@app.post("/api/simulate/transaction")
async def simulate_single_transaction(req: SingleTxSimRequest):
    if not req.is_fraud:
        tx = tx_engine.generate_benign_transaction()
    else:
        tx = tx_engine.generate_adversarial_transaction(
            vector_id=req.vector_id or "ADV-01",
            stealth_level=req.stealth_level
        )

    if req.custom_amount:
        tx.amount = req.custom_amount
    if req.custom_rail:
        tx.payment_rail = req.custom_rail

    decision = blue_engine.evaluate_transaction(tx)
    vec_meta = taxonomy.get_vector(req.vector_id).to_dict() if req.is_fraud and req.vector_id else None

    # Online learning step for Blue Team
    fv = blue_engine.feature_store.extract_features(tx)
    feature_contribs = blue_engine.tabular_detector.explain_prediction(fv)
    immune_update = blue_engine.adaptive_learner.observe_and_adapt(
        tx=tx,
        fv=fv,
        actual_is_fraud=req.is_fraud,
        predicted_prob=decision.fused_risk_score
    )

    return JSONResponse(content={
        "transaction": tx.to_dict(),
        "decision": decision.to_dict(),
        "feature_contributions": feature_contribs,
        "vector_metadata": vec_meta,
        "immune_update": immune_update.to_dict()
    })


@app.post("/api/simulate/swarm")
async def simulate_swarm_campaign(req: SwarmSimRequest):
    if req.campaign_type == "smurfing":
        res = swarm_sim.simulate_smurfing_swarm(
            target_amount=req.target_amount,
            mule_count=req.agent_count,
            stealth_level=req.stealth_level
        )
    else:
        res = swarm_sim.simulate_siss_campaign(
            swarm_size=req.agent_count,
            stealth_level=req.stealth_level
        )

    decisions = [blue_engine.evaluate_transaction(tx).to_dict() for tx in res.transaction_records[:35]]

    return JSONResponse(content={
        "campaign_id": res.campaign_id,
        "campaign_type": res.campaign_type,
        "total_agents": res.total_agents,
        "total_volume_extracted": res.total_volume_extracted,
        "duration_seconds": res.duration_seconds,
        "network_graph": res.network_graph,
        "evasion_metrics": res.evasion_metrics,
        "evaluated_sample_decisions": decisions
    })


@app.post("/api/arena/coevolution")
async def run_coevolution_arena(req: CoevolutionRequest):
    arena = ClosedLoopArena(seed=42)
    arena.initialize_and_train_baseline(n_samples=2500)
    summary = arena.run_coevolution_loop(
        generations=req.generations,
        population_per_gen=req.population_per_gen,
        mutation_rate=req.mutation_rate
    )
    return JSONResponse(content=summary)


@app.post("/api/sar/generate")
async def generate_sar_report(req: SarGenerateRequest):
    vec_meta = taxonomy.get_vector(req.vector_id).to_dict() if req.vector_id else None
    
    tx = tx_engine.generate_adversarial_transaction(vector_id=req.vector_id or "ADV-01", stealth_level=0.7)
    tx.tx_id = req.tx_id
    tx.account_id = req.account_id
    tx.merchant_id = req.merchant_id
    tx.amount = req.amount

    decision = blue_engine.evaluate_transaction(tx)
    sar = ExplainabilityEngine.generate_sar(tx, decision, vec_meta)

    return JSONResponse(content=sar.to_dict())


@app.get("/api/benchmarks")
async def get_benchmarks():
    import random
    # Use a random seed so the benchmark evaluates on a truly fresh, non-deterministic live dataset!
    dynamic_pipeline = BenchmarkPipeline(seed=random.randint(100, 99999))
    res = dynamic_pipeline.run_full_benchmark(train_samples=3000, test_samples=1000, save_results=False)
    return JSONResponse(content=res)


@app.get("/api/fidelity")
async def get_fidelity_metrics():
    res = fidelity_suite.run_full_fidelity_suite(sample_size=1500)
    return JSONResponse(content=res)


@app.get("/api/llm/metrics")
async def get_llm_metrics():
    return JSONResponse(content=llm.get_metrics())


@app.get("/api/system/health")
async def get_system_health():
    llm_health = llm.health_check()
    return JSONResponse(content={
        "system_status": "OPERATIONAL",
        "pillars": {
            "pillar_1_identify": {"status": "ACTIVE", "vectors": taxonomy.count(), "engine": "ActiveThreatDiscovery + arXiv OSINT"},
            "pillar_2_generate": {"status": "ACTIVE", "engine": "HighFidelity Synthetic Engine + Q-Learning Red Team"},
            "pillar_3_defend": {"status": "ACTIVE", "engine": "MultiModal 4-Tier Fusion (GBM + Isolation Forest + Network Graph + Gemini Guardrail)"},
            "pillar_4_closed_loop": {"status": "ACTIVE", "engine": "Co-Evolution Arena + Self-Auditing Gap Analyzer"}
        },
        "llm_engine": llm_health
    })



@app.post("/api/generate/image")
async def generate_image(req: GenerateImageRequest):
    try:
        nano_banana_key = os.getenv("NANO_BANANA_API_KEY")
        img_content = None
        
        # Attempt Nano Banana integration first
        if nano_banana_key:
            try:
                headers = {
                    "Authorization": f"Bearer {nano_banana_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "gemini-2.5-flash-image",
                    "prompt": req.prompt,
                    "n": 1,
                    "size": "512x512"
                }
                nb_res = requests.post("https://api.nanobananaapi.ai/v1/images/generations", headers=headers, json=payload, timeout=10)
                if nb_res.status_code == 200:
                    nb_data = nb_res.json()
                    if "data" in nb_data and len(nb_data["data"]) > 0:
                        # Some APIs return base64 instead of URL, checking for b64_json
                        if "b64_json" in nb_data["data"][0]:
                            import base64
                            img_content = base64.b64decode(nb_data["data"][0]["b64_json"])
                        elif "url" in nb_data["data"][0]:
                            image_url = nb_data["data"][0]["url"]
                            img_res = requests.get(image_url, timeout=10)
                            if img_res.status_code == 200:
                                img_content = img_res.content
            except Exception as e:
                print(f"[!] Nano Banana API failed, falling back to Pollinations. Error: {e}")
                pass
                
        # Fallback to Pollinations.ai if Nano Banana failed or wasn't configured
        if not img_content:
            encoded_prompt = urllib.parse.quote(req.prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
            if req.seed:
                url += f"&seed={req.seed}"
                
            # Retry logic for Pollinations due to potential high-load timeouts
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    res = requests.get(url, timeout=45)
                    if res.status_code == 200:
                        img_content = res.content
                        break
                    else:
                        print(f"[!] Pollinations returned {res.status_code} on attempt {attempt+1}")
                except Exception as get_err:
                    print(f"[!] Pollinations request failed on attempt {attempt+1}: {get_err}")
                    if attempt == max_retries - 1:
                        raise get_err
            
            if not img_content:
                return JSONResponse(content={"error": "Image generation failed on both APIs"}, status_code=500)
                
        filename = f"gen_img_{uuid.uuid4().hex[:8]}.jpg"
        assets_dir = os.path.join(STATIC_DIR, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        filepath = os.path.join(assets_dir, filename)
        with open(filepath, "wb") as f:
            f.write(img_content)
        return JSONResponse(content={"url": f"/static/assets/{filename}", "status": "success"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/generate/audio")
async def generate_audio(req: GenerateAudioRequest):
    try:
        import random
        # Different TLDs to simulate different regional accents and voices
        tlds = ['com', 'co.uk', 'com.au', 'co.in', 'ie', 'co.za']
        chosen_tld = random.choice(tlds)
        
        tts = gTTS(text=req.script, lang="en", tld=chosen_tld, slow=False)
        filename = f"gen_audio_{uuid.uuid4().hex[:8]}.mp3"
        assets_dir = os.path.join(STATIC_DIR, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        filepath = os.path.join(assets_dir, filename)
        tts.save(filepath)
        return JSONResponse(content={"url": f"/static/assets/{filename}", "status": "success"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
