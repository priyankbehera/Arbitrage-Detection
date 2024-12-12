import math

import numpy as np

from get_volatility import get_volatility


def generate_process(currency_one, currency_two, num_steps, r):
    filename = "Data Streams/" + currency_one + ":" + currency_two + ".csv"
    sigma, s_initial = get_volatility(filename)

    dt = 1  # in minutes
    t_values = np.arange(0, num_steps + 1)  # Time in minutes

    wiener_value = np.zeros(num_steps + 1)
    for i in range(len(wiener_value)):
        W = np.random.normal(0, np.sqrt(dt))
        wiener_value[i] = W

    S = np.zeros(num_steps + 1)
    S[0] = s_initial  # Set the initial value

    # Generate the stochastic process using GBM
    for i in range(1, num_steps + 1):
        S[i] = S[i - 1] * math.exp((r - (sigma ** 2) / 2) * (-dt) - sigma * wiener_value[i])

    return t_values, S
