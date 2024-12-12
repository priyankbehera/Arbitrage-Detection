import networkx as nx

from detect_arbitrage_opportunities import detect_arbitrage_opportunities
from generate_graph import generate_graph


def run_bellman_ford_snapshots(source, num_steps, r, spread):

    G_multi = generate_graph(num_steps, r, spread)

    # snapshots = []
    #for t in range(num_steps):
        # Create a directed graph snapshot for the time step
    #    G_snapshot = nx.MultiDiGraph()
    #    for u, v, data in G_multi.edges(data=True):
    #        # Use the weight at the current time step
    #        exchange_rate = data['exchange_rate'][t]
    #        G_snapshot.add_edge(u, v, exchange_rate=exchange_rate)

    #    snapshots.append(G_snapshot)

    #count = 0
    #time_step = 0
    #for G_snapshot in snapshots:
    #    time_step += 1 a
    #    negative_cycle = detect_arbitrage_opportunities(G_snapshot, source)
    #    if negative_cycle:
    #        count += 1

    count = 0
    for t in range(num_steps):
        # Create a directed graph snapshot for the time step
        G_snapshot = nx.MultiDiGraph()
        for u, v, data in G_multi.edges(data=True):
            # Use the weight at the current time step
            if data.get('cooldown', 0) == 0:
                exchange_rate = data['exchange_rate'][t]
                G_snapshot.add_edge(u, v, exchange_rate=exchange_rate)
            else:
                data['cooldown'] -= 1

        negative_cycle, u, v = detect_arbitrage_opportunities(G_snapshot, source)
        if negative_cycle:
            count += 1
            for a, b, data in G_multi.edges(data=True):
                if a == u & b == v:
                    data['cooldown'] = 60

    return count
