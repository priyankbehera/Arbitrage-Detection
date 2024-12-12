import math

import numpy as np

from generate_correlated_wiener import generate_correlated_wiener
from get_volatility import get_volatility


def generate_correlated_process(num_steps, r):
    currencies = ["EUR", "GBP", "AUD", "NZD", "CAD", "CHF", "JPY"]
    num_currencies = len(currencies)
    sigmas = np.zeros((num_currencies, num_currencies))
    s_initial = np.zeros((num_currencies, num_currencies))

    for i in range(num_currencies):
        for j in range(i, num_currencies):
            if i != j:
                currency_one = currencies[i]
                currency_two = currencies[j]
                filename = "Data Streams/" + currency_one + ":" + currency_two + ".csv"
                sigmas[i][j], s_initial[i][j] = get_volatility(filename)

    dt = 1  # in minutes
    t_values = np.arange(0, num_steps)  # Time in minutes

    wiener_values = generate_correlated_wiener(num_steps, dt)

    S = np.zeros((num_currencies, num_currencies, num_steps))
    for i in range(num_currencies):
        for j in range(num_currencies):
            S[i][j][0] = s_initial[i][j]  # Set the initial value

    # Generate the stochastic process using GBM
    for j in range(num_currencies):
        for k in range(j, num_currencies):
            if j != k:
                for i in range(1, num_steps):
                    S[j][k][i] = S[j][k][i - 1] * math.exp((r - (sigmas[j][k] ** 2) / 2) * (-dt)
                                                           - sigmas[j][k] * wiener_values[j][i])
    return t_values, S
