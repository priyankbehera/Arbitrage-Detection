import csv

import numpy as np
import pandas as pd


def generate_correlated_wiener(num_steps, dt):
    """
    Generates correlated Wiener processes for multiple assets.

    :param num_steps: Number of time steps in the process.
    :param dt: Time step size.

    :return: An array of shape (num_steps, num_assets) with correlated Wiener processes.
    """

    num_assets = 7
    correlation_matrix = generate_correlation_matrix()
    # Perform Cholesky decomposition to get the lower triangular matrix
    L = np.linalg.cholesky(correlation_matrix)

    # Generate independent Wiener processes (standard normal random values)
    independent_wiener = np.random.normal(0, np.sqrt(dt), (num_steps, num_assets))

    # need a matrix of dimension (21, num_steps)
    # Apply the Cholesky transformation to introduce correlations
    correlated_wiener = np.dot(independent_wiener, L.T)
    correlated_wiener = np.transpose(correlated_wiener)
    return correlated_wiener


def generate_correlation_matrix():
    currencies = ["EUR", "GBP", "AUD", "NZD", "CAD", "CHF", "JPY"]
    num_currencies = len(currencies)
    correlation_matrix = np.zeros((num_currencies, num_currencies))
    log_returns_dict = {currency: [] for currency in currencies}
    # read each file
    for i in range(num_currencies):
        for j in range(i, num_currencies):
            if i != j:
                file_path = "Data Streams/" + currencies[i] + ":" + currencies[j] + ".csv"
                prices = []
                try:
                    with open(file_path, 'r') as file:
                        reader = csv.reader(file)
                        count = 0
                        for row in reader:
                            if count > 190000:
                                break
                            prices.append(float(row[1]))
                            count += 1
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                    continue

                # Calculate log returns for the currency pair
                prices = np.array(prices)
                log_returns = np.log(prices[1:] / prices[:-1])  # Calculate log returns

                # Store log returns in both currency columns (i and j)
                log_returns_dict[currencies[i]].extend(log_returns)
                log_returns_dict[currencies[j]].extend(log_returns)
            else:
                correlation_matrix[i][i] = 1

    # Convert log_returns_dict to DataFrame and calculate correlation matrix
    log_returns_df = pd.DataFrame(log_returns_dict)
    correlation_matrix = log_returns_df.corr().to_numpy()

    return correlation_matrix


generate_correlated_wiener(15, 1)