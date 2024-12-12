import numpy as np

currencies = ["EUR", "GBP", "AUD", "NZD", "CAD", "CHF", "JPY"]
currency_to_index = {currency: index for index, currency in enumerate(currencies)}

arbitrage_currencies = [[0 for j in range(7)] for i in range(7)]


def detect_arbitrage_opportunities(G, source):
    """
    Detects arbitrage opportunities using the Bellman-Ford algorithm on a graph of currency exchange rates.

    :param G: A networkx directed graph where each edge has an 'exchange_rate' attribute
    :param source: The starting currency node for Bellman-Ford

    :return: True if an arbitrage opportunity (negative weight cycle) exists, False otherwise
    """

    # Step 1: Initialize distances
    distances = {node: float('inf') for node in G.nodes}
    distances[source] = 0  # Start from the source currency node

    # Step 2: Relax edges |V| - 1 times
    threshold = np.log(1 + 5e-3)  # threshold considering floating point errors, transaction costs, etc.
    for _ in range(len(G.nodes) - 1):
        for u, v, data in G.edges(data=True):
            weight = data['exchange_rate']
            if distances[u] + weight < distances[v] - threshold:
                distances[v] = distances[u] + weight

    # Step 3: Check for negative cycles (arbitrage opportunities)
    for u, v, data in G.edges(data=True):
        weight = data['exchange_rate']
        if distances[u] + weight < distances[v] - threshold:  # A negative cycle exists
            arbitrage_currencies[currency_to_index[u]][currency_to_index[v]] += 1
            return True, u, v  # Arbitrage opportunity found

    return False  # No arbitrage opportunity found
