import math
import networkx as nx
import numpy as np
import csv
import matplotlib.pyplot as plt

from test import run_bellman_ford_snapshots, generate_process


def plot_probability_vs_r(iterations, num_steps):
    r_values = np.linspace(1e-8, 6e-8, 10)  # Example range for r
    probabilities = []
    avg = 0
    for r in r_values:
        for i in range(iterations):
            avg += run_bellman_ford_snapshots("EUR", num_steps, r)

        probabilities.append(avg / (num_steps * iterations))

    plt.plot(r_values, probabilities)
    plt.title("Probability of Arbitrage vs r")
    plt.xlabel("r (drift)")
    plt.ylabel("Probability of Arbitrage")
    plt.grid()
    plt.show()


def plot_n_vs_arbitrage(n_values, source, r):
    probabilities = np.zeros(len(n_values))
    count = 0
    for n in n_values:
        probabilities[count] = run_bellman_ford_snapshots(source, n, r) / n
        count += 1

    plt.figure(figsize=(10, 5))
    plt.plot(n_values, probabilities)

    plt.title("Probability of Arbitrage vs N (number of steps)")
    plt.xlabel("N (number of steps)")
    plt.ylabel("Probability of Arbitrage")
    plt.grid()
    plt.show()


def plot_process(t_values, S):
    # Convert t_values from minutes to days
    t_values_days = 0.66 * (t_values / 1440)  # 1440 minutes in a day

    plt.figure(figsize=(10, 5))
    plt.plot(t_values_days, S)  # Plot with days as the x-axis

    plt.title("Stochastic Process for Currency Pair")
    plt.xlabel("Time (Days)")  # Update label to reflect days
    plt.ylabel("Currency Price")
    plt.grid()
    plt.show()


num_steps = 100000
r = 10e-8
t_values, S = generate_process("EUR", "GBP", num_steps, r)
plot_process(t_values, S)

# def plot_arbitrage_vs_r(r_values):
