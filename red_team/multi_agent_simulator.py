"""
AegisPay-AI: Multi-Agent Swarm Simulator (Pillar 2 - GENERATE)
Simulates coordinated multi-agent adversarial fraud campaigns:
1. Synthetic Identity Seasoning Swarms (SISS)
2. Autonomous Multi-Rail Smurfing Rings (DAG flow)
3. Synchronized Sleeper Bust-Out Swarms
4. Agentic Commerce Indirect Prompt Injection Campaigns
"""
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import networkx as nx

from .generator import SyntheticTransactionEngine, TransactionRecord


@dataclass
class SwarmAgent:
    agent_id: str
    role: str  # "MASTER_COORDINATOR", "MULE_LAYER_1", "MULE_LAYER_2", "CASH_OUT_NODE", "SYNTHETIC_BUYER"
    balance: float
    credit_limit: float
    seasoning_days: int
    stealth_rating: float
    device_id: str
    ip_subnet: str


@dataclass
class SwarmCampaignResult:
    campaign_id: str
    campaign_type: str
    total_agents: int
    total_volume_extracted: float
    duration_seconds: float
    transaction_records: List[TransactionRecord]
    network_graph: Dict[str, Any]  # serialized nodes and edges for Vis.js visualization
    evasion_metrics: Dict[str, Any]


class MultiAgentSwarmSimulator:
    """
    Orchestrates complex multi-agent attack swarms executing coordinated fraud campaigns.
    """

    def __init__(self, seed: int = 1337):
        self.rng = random.Random(seed)
        self.tx_engine = SyntheticTransactionEngine(seed=seed)

    def simulate_smurfing_swarm(
        self,
        target_amount: float = 50000.0,
        mule_count: int = 24,
        stealth_level: float = 0.8
    ) -> SwarmCampaignResult:
        """
        Simulates an Autonomous Multi-Rail Smurfing Swarm (ADV-06):
        Splits high-value illicit funds across a multi-layer directed acyclic graph (DAG)
        of mule agents, hopping across rails before consolidating at off-ramps.
        """
        campaign_id = f"CAMP_SMURF_{uuid.uuid4().hex[:8].upper()}"
        graph = nx.DiGraph()
        tx_records: List[TransactionRecord] = []

        # 1. Initialize Master Source & Final Cashout Nodes
        source_id = "SRC_ILLICIT_001"
        graph.add_node(source_id, label="Illicit Origin", type="SOURCE", volume=target_amount, risk=0.99)

        cashout_nodes = [f"OFFRAMP_CRYPTO_{i+1:02d}" for i in range(3)]
        for cnode in cashout_nodes:
            graph.add_node(cnode, label="Crypto On-Ramp / Off-Ramp", type="CASHOUT", volume=0.0, risk=0.95)

        # 2. Initialize Layer 1 (Fan-out) and Layer 2 (Obfuscation) Mule Agents
        l1_count = mule_count // 3
        l2_count = mule_count - l1_count

        l1_nodes = [f"MULE_L1_{i+1:03d}" for i in range(l1_count)]
        l2_nodes = [f"MULE_L2_{j+1:03d}" for j in range(l2_count)]

        for n in l1_nodes:
            graph.add_node(n, label=f"Mule Hop L1", type="MULE_L1", volume=0.0, risk=0.75)
        for n in l2_nodes:
            graph.add_node(n, label=f"Mule Hop L2", type="MULE_L2", volume=0.0, risk=0.65)

        # 3. Simulate Hop 1: Source -> Layer 1 Mules
        base_time = time.time()
        l1_slice = target_amount / len(l1_nodes)
        
        for l1 in l1_nodes:
            amt = round(l1_slice * self.rng.uniform(0.92, 1.08), 2)
            tx = self.tx_engine.generate_adversarial_transaction(
                vector_id="ADV-06",
                stealth_level=stealth_level,
                current_time=base_time + self.rng.uniform(1.0, 15.0)
            )
            tx.amount = amt
            tx.account_id = source_id
            tx.merchant_id = l1
            tx.payment_rail = "UPI / Instant Payment Rails"
            tx.remittance_memo = f"P2P Layer 1 Fanout - Ref {uuid.uuid4().hex[:6]}"
            tx_records.append(tx)
            graph.add_edge(source_id, l1, amount=amt, timestamp=tx.timestamp, rail="UPI")

        # 4. Simulate Hop 2: Layer 1 Mules -> Layer 2 Mules (Cross-rail smurfing)
        for l1 in l1_nodes:
            # Each L1 sends to 2 distinct L2 mules
            targets = self.rng.sample(l2_nodes, k=min(2, len(l2_nodes)))
            sub_slice = (l1_slice * 0.98) / len(targets)
            for t_node in targets:
                amt = round(sub_slice * self.rng.uniform(0.90, 1.10), 2)
                # Structured just below threshold if stealth is high
                if stealth_level > 0.6 and amt > 4900.0:
                    amt = round(self.rng.uniform(920.0, 1950.0), 2)
                
                tx = self.tx_engine.generate_adversarial_transaction(
                    vector_id="ADV-06",
                    stealth_level=stealth_level,
                    current_time=base_time + self.rng.uniform(30.0, 120.0)
                )
                tx.amount = amt
                tx.account_id = l1
                tx.merchant_id = t_node
                tx.payment_rail = "FedNow / SEPA Instant"
                tx.remittance_memo = f"Split Transfer - Tranche {uuid.uuid4().hex[:4]}"
                tx_records.append(tx)
                graph.add_edge(l1, t_node, amount=amt, timestamp=tx.timestamp, rail="FedNow")

        # 5. Simulate Hop 3: Layer 2 Mules -> Crypto Offramps (Re-aggregation)
        for l2 in l2_nodes:
            dest = self.rng.choice(cashout_nodes)
            amt = round(self.rng.uniform(1800.0, 4900.0), 2)
            tx = self.tx_engine.generate_adversarial_transaction(
                vector_id="ADV-06",
                stealth_level=stealth_level,
                current_time=base_time + self.rng.uniform(140.0, 300.0)
            )
            tx.amount = amt
            tx.account_id = l2
            tx.merchant_id = dest
            tx.payment_rail = "Cross-Border Remittance & Crypto On-Ramp"
            tx.remittance_memo = f"Exchange Liquidity Deposit #{self.rng.randint(1000, 9999)}"
            tx_records.append(tx)
            graph.add_edge(l2, dest, amount=amt, timestamp=tx.timestamp, rail="Crypto/CrossBorder")

        # Package Vis.js graph structure
        vis_nodes = []
        for n, data in graph.nodes(data=True):
            color = "#EF4444" if data.get("type") == "SOURCE" else "#F59E0B" if "MULE" in data.get("type", "") else "#8B5CF6"
            vis_nodes.append({
                "id": n,
                "label": f"{n}\n({data.get('type')})",
                "color": color,
                "shape": "dot",
                "size": 25 if data.get("type") in ["SOURCE", "CASHOUT"] else 15,
                "type": data.get("type"),
                "risk": data.get("risk", 0.5)
            })

        vis_edges = []
        for u, v, data in graph.edges(data=True):
            vis_edges.append({
                "from": u,
                "to": v,
                "label": f"${data['amount']} ({data.get('rail')})",
                "arrows": "to",
                "color": {"color": "#64748B", "highlight": "#F97316"}
            })

        return SwarmCampaignResult(
            campaign_id=campaign_id,
            campaign_type="Autonomous Multi-Rail Smurfing Swarm (ADV-06)",
            total_agents=mule_count + 4,
            total_volume_extracted=target_amount,
            duration_seconds=300.0,
            transaction_records=tx_records,
            network_graph={"nodes": vis_nodes, "edges": vis_edges},
            evasion_metrics={
                "stealth_level": stealth_level,
                "fan_out_ratio": l1_count / 1.0,
                "fan_in_ratio": l2_count / len(cashout_nodes),
                "avg_hop_dwell_seconds": 45.2,
                "below_reporting_threshold_pct": 94.2 if stealth_level > 0.6 else 62.5
            }
        )

    def simulate_siss_campaign(
        self,
        swarm_size: int = 15,
        stealth_level: float = 0.85
    ) -> SwarmCampaignResult:
        """
        Simulates Synthetic Identity Seasoning Swarms (SISS - ADV-01):
        Incubated synthetic identities that perform seasoning micro-transactions
        before executing a synchronized bust-out.
        """
        campaign_id = f"CAMP_SISS_{uuid.uuid4().hex[:8].upper()}"
        tx_records: List[TransactionRecord] = []
        graph = nx.DiGraph()

        base_time = time.time() - (86400 * 30)  # 30-day historical window

        # Create synthetic accounts
        synthetic_agents = [f"SYNTH_ID_{i+1:03d}" for i in range(swarm_size)]
        seasoning_merchants = [f"SEASONING_UTIL_{k+1:02d}" for k in range(4)]
        bustout_merchants = ["LUXURY_JEWELRY_01", "HIGH_END_ELECTRONICS_02", "GIFT_CARD_EXCHANGE_03"]

        for sa in synthetic_agents:
            graph.add_node(sa, label=sa, type="SYNTHETIC_ID", risk=0.92)

        for sm in seasoning_merchants:
            graph.add_node(sm, label=sm, type="SEASONING_HUB", risk=0.2)
        for bm in bustout_merchants:
            graph.add_node(bm, label=bm, type="BUSTOUT_MERCHANT", risk=0.88)

        # Phase 1: Incubation & Seasoning (Small transactions building credit)
        for sa in synthetic_agents:
            for day in range(10):
                t = base_time + (day * 86400 * 3) + self.rng.uniform(100, 5000)
                merch = self.rng.choice(seasoning_merchants)
                amt = round(self.rng.uniform(12.50, 48.00), 2)
                tx = self.tx_engine.generate_benign_transaction(current_time=t)
                tx.account_id = sa
                tx.merchant_id = merch
                tx.amount = amt
                tx.remittance_memo = f"Monthly Subscription / Utility {uuid.uuid4().hex[:4]}"
                tx_records.append(tx)
                graph.add_edge(sa, merch, amount=amt, phase="SEASONING")

        # Phase 2: Synchronized Bust-Out (Maximum credit drawdown in 10 minutes)
        bustout_time = time.time()
        total_extracted = 0.0
        for sa in synthetic_agents:
            merch = self.rng.choice(bustout_merchants)
            amt = round(self.rng.uniform(4200.0, 9800.0), 2)
            total_extracted += amt
            tx = self.tx_engine.generate_adversarial_transaction(
                vector_id="ADV-01",
                stealth_level=stealth_level,
                current_time=bustout_time + self.rng.uniform(1.0, 60.0)
            )
            tx.account_id = sa
            tx.merchant_id = merch
            tx.amount = amt
            tx.remittance_memo = f"Direct Checkout - High Value Goods #{self.rng.randint(10000, 99999)}"
            tx_records.append(tx)
            graph.add_edge(sa, merch, amount=amt, phase="BUST_OUT")

        # Vis.js graph
        vis_nodes = []
        for n, data in graph.nodes(data=True):
            color = "#EC4899" if data.get("type") == "SYNTHETIC_ID" else "#10B981" if data.get("type") == "SEASONING_HUB" else "#DC2626"
            vis_nodes.append({
                "id": n,
                "label": f"{n}\n({data.get('type')})",
                "color": color,
                "shape": "dot",
                "size": 22 if "MERCHANT" in data.get("type", "") else 14,
                "type": data.get("type"),
                "risk": data.get("risk", 0.5)
            })

        vis_edges = []
        for u, v, data in graph.edges(data=True):
            is_bustout = data.get("phase") == "BUST_OUT"
            vis_edges.append({
                "from": u,
                "to": v,
                "label": f"${data['amount']} [{data.get('phase')}]",
                "arrows": "to",
                "color": {"color": "#EF4444" if is_bustout else "#10B981", "highlight": "#F43F5E"},
                "width": 3 if is_bustout else 1
            })

        return SwarmCampaignResult(
            campaign_id=campaign_id,
            campaign_type="Synthetic Identity Seasoning Swarms (ADV-01)",
            total_agents=swarm_size,
            total_volume_extracted=round(total_extracted, 2),
            duration_seconds=600.0,
            transaction_records=tx_records,
            network_graph={"nodes": vis_nodes, "edges": vis_edges},
            evasion_metrics={
                "stealth_level": stealth_level,
                "seasoning_ratio": len([t for t in tx_records if not t.is_fraud]) / len(tx_records),
                "bustout_velocity_spike": "18.4x over baseline",
                "mean_credit_utilization": "98.7%"
            }
        )
