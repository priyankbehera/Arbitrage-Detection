import csv
import math

import numpy as np


def get_volatility(file_name):
    """
    :param file_name:

    :return:
    sigma
        the volatility of the exchange rate of the currency

    s_initial
        initial exchange rate of the currency
    """

    currency_prices = []
    try:
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                currency_prices.append(float(row[1]))
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the file '{file_name}': {e}")
        return None

    s_initial = currency_prices[0]
    currency_prices = np.array(currency_prices)

    log_currency_prices = np.log(currency_prices[1:] / currency_prices[:-1])
    variance = np.var(log_currency_prices, ddof=1)

    sigma = math.sqrt(variance)
    adjustment = 3
    sigma = sigma / adjustment
    return sigma, s_initial
