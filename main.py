from matplotlib import pyplot as plt

from detect_arbitrage_opportunities import arbitrage_currencies
from run_bellman_ford_snapshots import run_bellman_ford_snapshots


num_steps = 10000
iterations = 3
avg = 0
avg_two = 0
r = 3.8e-8
spread = 0.0015 # in basis points, 0.0001 is 1 basis point, take a range between 1 and 20

for i in range(iterations):
    count = run_bellman_ford_snapshots("EUR", num_steps, r, spread)
    avg += count


print(f"Average probability of arbitrage for n = {num_steps} is {100 * avg / (iterations * num_steps)}%")

# NOTE: r should stay between the values of 1e-8 and 10e-8
# NOTE: choosing the source currency does not affect arbitrage
# probability, nor locations where arbitrage happens.
# Find a way to reduce arbitrage possibility using location of arbitrage detection
# Nov 1st, 2024
# (1) introduced spread to create a difference in bid and ask
# (2) adjusted the threshold accordingly, should be from 1e-3 to 10e-3, accounting for transaction costs, fees, etc
# Nov 6th, 2024
# (1) came up with correlated Wiener process
# @todo
# (1) create a histogram of all the values of arbitrage probability for n = 10000
# (2) try to create a distribution
# create graphs to show dependency of arbitrage on n (steps) and r (interest rate)
