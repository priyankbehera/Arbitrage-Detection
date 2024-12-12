import networkx as nx
import numpy as np

from generate_process import generate_process
from generate_correlated_processes import generate_correlated_process


def generate_graph(num_steps, r, spread):
    # EUR, GBP, AUD, NZD, CAD, CHF, JPY
    currencies = ["EUR", "GBP", "AUD", "NZD", "CAD", "CHF", "JPY"]
    num_currencies = len(currencies)
    # initialize graph and add nodes
    G = nx.MultiDiGraph()
    G.add_nodes_from(currencies)

    # Generate time series weights for the upper triangle and reciprocals for the lower triangle
    # Model 1: Independent Wiener Processes
    # for i in range(num_currencies):
    #    for j in range(i, num_currencies):
    #        if i != j:
    #            # Generate a time series for the upper triangle
    #            _, edge_weight = generate_process(currencies[i], currencies[j], num_steps, r)

    #           # take the log of each value, and add it accordingly
    #            for k in range(len(edge_weight)):
    #                edge_weight[k] = np.log(edge_weight[k])
    #            # Add edges to the graph with corresponding weights
    #            G.add_edge(currencies[i], currencies[j], exchange_rate=edge_weight + np.log(1 + spread))
    #            G.add_edge(currencies[j], currencies[i], exchange_rate=-edge_weight - np.log(1 - spread))

    _, S = generate_correlated_process(num_steps, r)
    for i in range(num_currencies):
        for j in range(i, num_currencies):
            if S[i][j][0] != 0:
                for k in range(len(S[i][j])):
                    S[i][j][k] = np.log(S[i][j][k])

            if i != j:
                G.add_edge(currencies[i], currencies[j], exchange_rate=S[i][j] + np.log(1 + spread))
                G.add_edge(currencies[i], currencies[j], cooldown=0)
                G.add_edge(currencies[j], currencies[i], exchange_rate=-S[i][j] - np.log(1 - spread))
                G.add_edge(currencies[j], currencies[i], cooldown=0)
    return G
