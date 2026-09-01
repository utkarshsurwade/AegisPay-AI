"""
AegisPay-AI: Graph Topology & Fraud Ring Detector (Pillar 3 - DEFEND Level 3)
Production Graph Analytics Engine (<10ms):
Computes dynamic topological features:
1. Real-time PageRank & Ego-network Centrality
2. Flow Conservation & Velocity Disparity (Mule pass-through detection)
3. Subgraph Clustering Coefficient & Density (Fraud ring discovery)
4. Multi-hop structured fan-out and fragmentation metrics
"""
import time
from typing import Dict, Any, List, Optional
import networkx as nx
import numpy as np

from red_team.generator import TransactionRecord


class GraphTopologyDetector:
    """
    Maintains dynamic streaming transaction graph and computes topological risk
    using rigorous graph theory and network centrality algorithms.
    """

    def __init__(self, max_nodes: int = 10000, pagerank_interval: int = 50):
        self.graph = nx.DiGraph()
        self.max_nodes = max_nodes
        self.tx_counter = 0
        self.pagerank_interval = pagerank_interval
        self.cached_pagerank: Dict[str, float] = {}
        self.node_in_volume: Dict[str, float] = {}
        self.node_out_volume: Dict[str, float] = {}
        self.node_tx_timestamps: Dict[str, List[float]] = {}

    def ingest_transaction(self, tx: TransactionRecord):
        """
        Updates dynamic transaction graph with incoming transaction edge.
        """
        u = tx.account_id
        v = tx.merchant_id
        now = tx.timestamp
        self.tx_counter += 1

        # Add or update nodes
        if not self.graph.has_node(u):
            self.graph.add_node(u, total_volume=0.0, tx_count=0)
            self.node_in_volume[u] = 0.0
            self.node_out_volume[u] = 0.0
            self.node_tx_timestamps[u] = []
        if not self.graph.has_node(v):
            self.graph.add_node(v, total_volume=0.0, tx_count=0)
            self.node_in_volume[v] = 0.0
            self.node_out_volume[v] = 0.0
            self.node_tx_timestamps[v] = []

        self.graph.nodes[u]["tx_count"] += 1
        self.graph.nodes[u]["total_volume"] += tx.amount
        self.graph.nodes[v]["tx_count"] += 1
        self.graph.nodes[v]["total_volume"] += tx.amount

        self.node_out_volume[u] += tx.amount
        self.node_in_volume[v] += tx.amount
        self.node_tx_timestamps[u].append(now)
        self.node_tx_timestamps[v].append(now)

        # Add or update weighted edge
        if self.graph.has_edge(u, v):
            self.graph[u][v]["weight"] += tx.amount
            self.graph[u][v]["count"] += 1
            self.graph[u][v]["last_seen"] = now
        else:
            self.graph.add_edge(
                u, v,
                weight=tx.amount,
                count=1,
                first_seen=now,
                last_seen=now,
                rail=tx.payment_rail
            )

        # Periodically compute PageRank across entire graph
        if self.tx_counter % self.pagerank_interval == 0 or not self.cached_pagerank:
            try:
                if len(self.graph) > 1:
                    self.cached_pagerank = nx.pagerank(
                        self.graph,
                        alpha=0.85,
                        weight="weight",
                        max_iter=30
                    )
            except Exception:
                pass

    def score_ego_subgraph(self, tx: TransactionRecord) -> Dict[str, Any]:
        """
        Computes topological fraud risk based on network structure, flow conservation,
        ego-network density, and centrality anomalies.
        """
        self.ingest_transaction(tx)
        u = tx.account_id
        v = tx.merchant_id

        # 1. Degree & Topology Centrality
        out_deg_u = self.graph.out_degree(u) if self.graph.has_node(u) else 1
        in_deg_u = self.graph.in_degree(u) if self.graph.has_node(u) else 0
        in_deg_v = self.graph.in_degree(v) if self.graph.has_node(v) else 1
        out_deg_v = self.graph.out_degree(v) if self.graph.has_node(v) else 0

        # 2. PageRank Centrality
        pr_u = self.cached_pagerank.get(u, 1.0 / max(1, len(self.graph)))
        pr_v = self.cached_pagerank.get(v, 1.0 / max(1, len(self.graph)))
        mean_pr = 1.0 / max(1, len(self.graph))
        pr_anomaly_u = min(1.0, pr_u / max(1e-6, mean_pr * 5.0))

        # 3. Flow Conservation & Rapid Pass-Through Metric (Mule transit detection)
        # Genuine consumers: In-volume (salary/transfer) is much higher or equal to out-volume over time
        # Mule nodes: In-volume almost exactly equals Out-volume within short time window, with high fan-in/fan-out
        in_vol_u = self.node_in_volume.get(u, 0.0)
        out_vol_u = self.node_out_volume.get(u, tx.amount)

        is_rapid_transit = False
        transit_risk = 0.0
        if in_vol_u > 0 and out_vol_u > 0:
            vol_ratio = min(in_vol_u, out_vol_u) / max(in_vol_u, out_vol_u)
            if vol_ratio > 0.70 and (in_deg_u >= 2 and out_deg_u >= 2):
                is_rapid_transit = True
                transit_risk = 0.82 * vol_ratio

        # 4. Dispersion / Smurfing Fan-Out Detection
        # High out-degree with structured micro-amounts sent to multiple distinct endpoints
        avg_amt_u = out_vol_u / max(1, out_deg_u)
        is_smurfing = (out_deg_u >= 3 and 100.0 <= avg_amt_u <= 2500.0)
        smurfing_risk = 0.0
        if is_smurfing:
            smurfing_risk = min(0.95, 0.45 + (out_deg_u * 0.08))

        # 5. Ego-Subnetwork Density (Synthetic Ring Clustering)
        ego_density = 0.0
        try:
            ego_u = nx.ego_graph(self.graph, u, radius=1)
            if len(ego_u) > 2:
                ego_density = nx.density(ego_u)
        except Exception:
            ego_density = 0.0

        ring_risk = 0.0
        if ego_density > 0.40 and len(self.graph.nodes) > 10:
            ring_risk = min(0.90, ego_density * 1.2)

        # 6. Combined Topological Anomaly Score
        base_topological_risk = 0.05

        scores = [
            base_topological_risk,
            transit_risk,
            smurfing_risk,
            ring_risk,
            pr_anomaly_u * 0.35 if out_deg_u > 5 else 0.0
        ]
        combined_risk = float(np.clip(max(scores), 0.02, 0.98))

        # Subgraph Motifs Explanation
        motifs = []
        if is_smurfing:
            motifs.append(f"Smurfing Fan-Out Dispersion (Degree: {out_deg_u}, Avg: ${avg_amt_u:.0f})")
        if is_rapid_transit:
            motifs.append("Rapid Flow Pass-Through (Mule Transit In≈Out)")
        if ring_risk > 0.5:
            motifs.append(f"High Subgraph Clustering Density ({ego_density:.2f})")
        if out_deg_u >= 6:
            motifs.append(f"Central Dispersion Hub ({out_deg_u} Target Endpoints)")

        return {
            "graph_topology_risk": round(combined_risk, 4),
            "account_out_degree": out_deg_u,
            "account_in_degree": in_deg_u,
            "merchant_in_degree": in_deg_v,
            "pagerank_centrality": round(float(pr_u), 6),
            "ego_clustering_density": round(float(ego_density), 4),
            "smurfing_signature_detected": is_smurfing,
            "mule_transit_detected": is_rapid_transit,
            "subgraph_motifs": motifs[:4]
        }
