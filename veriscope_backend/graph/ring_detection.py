import pandas as pd
import networkx as nx
from pathlib import Path
from networkx.algorithms.community import louvain_communities

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"

def get_graph_risk():

    # Load the data
    features = pd.read_csv(DATA_DIR / "features.csv")

    # Create graph of accounts
    G = nx.Graph()

    for account_id in features["account_id"].unique():
        G.add_node(account_id, type="account")

    # Connect accounts sharing the same Device
    for device_id, group in features.groupby("device_id"):
        accounts = group["account_id"].unique()
        for i in range(len(accounts)):
            for j in range(i + 1, len(accounts)):
                G.add_edge(accounts[i], accounts[j], relation="shared_device")

    # Connect accounts sharing the same IP address
    for ip_address, group in features.groupby("ip_address"):
        accounts = group["account_id"].unique()
        for i in range(len(accounts)):
            for j in range(i + 1, len(accounts)):
                G.add_edge(accounts[i], accounts[j], relation="shared_ip")

    # Connect accounts having the same Card
    for card_fingerprint, group in features.groupby("card_fingerprint"):
        accounts = group["account_id"].unique()
        for i in range(len(accounts)):
            for j in range(i + 1, len(accounts)):
                G.add_edge(accounts[i], accounts[j], relation="shared_card")

    # Detect communities using Louvain
    communities = louvain_communities(G, seed=42)

    # Analyze each community

    community_results = []

    for community_id, community in enumerate(communities):
        community_data = features[
            features["account_id"].isin(community)
        ]

        fraud_count = community_data["is_fraud"].sum()
        total_transactions = len(community_data)

        if total_transactions > 0:
            fraud_rate = fraud_count / total_transactions
        else:
            fraud_rate = 0

        community_results.append({
            "community_id": community_id,
            "num_accounts": len(community),
            "total_transactions": total_transactions,
            "fraud_count": fraud_count,
            "fraud_rate": fraud_rate
        })

    community_df = pd.DataFrame(community_results)

    # Calculate graph density

    for result, community in zip(community_results, communities):
        subgraph = G.subgraph(community)
        result["edges"] = subgraph.number_of_edges()
        result["density"] = nx.density(subgraph)

    community_df = pd.DataFrame(community_results)

    # Calculate ring score

    MIN_RING_SIZE = 3
    IDEAL_MAX_RING_SIZE = 15

    valid_communities = community_df[
        community_df["num_accounts"] >= MIN_RING_SIZE
    ].copy()

    # Density score
    valid_communities["density_score"] = valid_communities["density"]

    # Edge score

    max_edges = valid_communities["edges"].max()

    if max_edges > 0:
        valid_communities["edge_score"] = (
            valid_communities["edges"] / max_edges
        )
    else:
        valid_communities["edge_score"] = 0

    # Ring size score

    def calculate_size_score(size):
        if size <= IDEAL_MAX_RING_SIZE:
            return 1.0
        return IDEAL_MAX_RING_SIZE / size

    valid_communities["size_score"] = (
        valid_communities["num_accounts"]
        .apply(calculate_size_score)
    )

    # Final ring score
    valid_communities["ring_score"] = (
        valid_communities["density_score"] * 0.60
        + valid_communities["edge_score"] * 0.20
        + valid_communities["size_score"] * 0.20
    )

    # Create community → score mapping

    community_score_map = {}

    for _, row in valid_communities.iterrows():
        community_id = int(row["community_id"])
        community_score_map[community_id] = float(
            row["ring_score"]
        )

    # Create account-level graph risk

    account_graph_risk = []

    for community_id, community in enumerate(communities):
        score = community_score_map.get(
            community_id,
            0.0
        )
        for account_id in community:
            account_graph_risk.append({
                "account_id": account_id,
                "community_id": community_id,
                "graph_ring_score": score
            })

    account_graph_risk_df = pd.DataFrame(
        account_graph_risk
    )

    return account_graph_risk_df


if __name__ == "__main__":

    graph_risk = get_graph_risk()

    print("\nGraph risk detection complete!")