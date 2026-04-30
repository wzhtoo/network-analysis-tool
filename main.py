"""
5BB Home Network Analysis — Python (networkx)
=============================================
အသုံးပြုထားသော IP များ:
  - 192.168.100.1 (Router)
  - 192.168.100.6 (WinZawHtoo PC)
  - 192.168.100.9, 100.11, 100.19 (Other Devices)
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


# ─────────────────────────────────────────────
# 1. Graph တည်ဆောက်ခြင်း
# ─────────────────────────────────────────────

def build_graph(edges, directed=False):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_edges_from(edges)
    return G


# ─────────────────────────────────────────────
# 2. Network Statistics Summary
# ─────────────────────────────────────────────

def network_summary(G):
    print("=" * 45)
    print("  HOME NETWORK SUMMARY")
    print("=" * 45)
    print(f"  Total Devices (Nodes) : {G.number_of_nodes()}")
    print(f"  Connections (Edges)   : {G.number_of_edges()}")

    if not G.is_directed():
        print(f"  Connected Properly    : {nx.is_connected(G)}")
        print(f"  Avg Path Length       : {nx.average_shortest_path_length(G):.4f}")

    degrees = [d for _, d in G.degree()]
    print(f"  Average Connections   : {np.mean(degrees):.2f}")
    print(f"  Network Density       : {nx.density(G):.4f}")
    print("=" * 45)


# ─────────────────────────────────────────────
# 3. Centrality Analysis (ဘယ်စက်က အရေးကြီးဆုံးလဲ)
# ─────────────────────────────────────────────

def centrality_analysis(G, top_n=3):
    results = {}
    results["degree"] = nx.degree_centrality(G)
    results["betweenness"] = nx.betweenness_centrality(G)
    results["pagerank"] = nx.pagerank(G)

    print("\n── Network Analysis (Top Devices) ──")
    for measure, scores in results.items():
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        print(f"\n  {measure.capitalize()} Importance:")
        for rank, (node, score) in enumerate(top, 1):
            print(f"    {rank}. {node:<15}  →  {score:.4f}")


# ─────────────────────────────────────────────
# 4. Visualization (ပုံဖော်ခြင်း)
# ─────────────────────────────────────────────

def visualize_graph(G, title="5BB Home Network", save_path=None):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.axis("off")

    # Layout
    pos = nx.spring_layout(G, seed=42)

    # Node sizes based on connections
    scores = nx.degree_centrality(G)
    max_score = max(scores.values()) or 1
    node_sizes = [500 + 2000 * (scores[n] / max_score) for n in G.nodes()]

    # Draw
    nx.draw_networkx_edges(G, pos, edge_color="#cccccc", width=1.5, alpha=0.7)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#5B8DB8", alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"\n[✓] Saved → {save_path}")
    else:
        plt.show()


# ─────────────────────────────────────────────
# Main Execution - အစားထိုးထားသောအပိုင်း
# ─────────────────────────────────────────────

# if __name__ == "__main__":
#     # Nmap scan မှ ရလာသော တကယ့် IP များ
#     router_ip = "192.168.100.1"
#     my_pc = "192.168.100.6"
#     device_1 = "192.168.100.9"
#     device_2 = "192.168.100.11"
#     device_3 = "192.168.100.19"
#
#     # Router နှင့် ကျန်စက်များ ချိတ်ဆက်ပုံ (Star Topology)
#     home_edges = [
#         (router_ip, my_pc),
#         (router_ip, device_1),
#         (router_ip, device_2),
#         (router_ip, device_3)
#     ]
#
#     print("\n▶ Analyzing your 5BB Home Network...")
#     G = build_graph(home_edges)
#
#     # Run Analysis
#     network_summary(G)
#     centrality_analysis(G)
#
#     # Visualization
#     visualize_graph(G, title="WinZawHtoo's Home Network (5BB)", save_path="5bb_network_analysis.png")
#
#     print("\n[!] Analysis complete. Please check '5bb_network_analysis.png' in your project folder.")

if __name__ == "__main__":
    # စက်တစ်ခုချင်းစီမှာ ပွင့်နေတဲ့ Services များ (Nmap Result အရ)
    services = {
        "192.168.100.1": "Router\n(DNS, HTTP)",
        "192.168.100.6": "WinZawHtoo PC\n(SMB, HTTP, HTTPS)",
        "192.168.100.9": "Device .9\n(SIP-Filtered)",
        "192.168.100.19": "Device .19\n(SSH, HTTP, HTTPS)"
    }

    # Router ကို ဗဟိုထားပြီး ချိတ်ဆက်မှုများ တည်ဆောက်ခြင်း
    home_edges = [
        (services["192.168.100.1"], services["192.168.100.6"]),
        (services["192.168.100.1"], services["192.168.100.9"]),
        (services["192.168.100.1"], services["192.168.100.19"])
    ]

    print("\n▶ Analyzing Network with Service Information...")
    G = build_graph(home_edges)

    # Summary နှင့် Centrality ကိုလည်း ဆက်လက် run ပါ
    network_summary(G)
    centrality_analysis(G)

    # Visualization ကို run ပြီး ပုံအသစ်အဖြစ် သိမ်းပါ
    visualize_graph(G, title="5BB Home Network with Services", save_path="5bb_service_map.png")

    print("\n✓ Done! '5bb_service_map.png' ကို ကြည့်ပါ။")