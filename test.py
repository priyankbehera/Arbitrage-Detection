from detect_arbitrage_opportunities import arbitrage_currencies
from run_bellman_ford_snapshots import run_bellman_ford_snapshots


num_steps = 10000
num_steps_two = 100
iterations = 1
avg = 0
avg_two = 0
r = 3.8e-8
spread = 0.0015 # in basis points, 0.0001 is 1 basis point, take a range between 1 and 20

for i in range(iterations):
    avg += run_bellman_ford_snapshots("EUR", num_steps, r, spread)

print(f"Average probability of arbitrage for n = {num_steps} is {100 * avg / (iterations * num_steps)}%")
print(arbitrage_currencies)

# NOTE: r should stay between the values of 1e-8 and 10e-8
# NOTE: choosing the source currency does not affect arbitrage
# probability, nor locations where arbitrage happens.
# Find a way to reduce arbitrage possibility using location of arbitrage detection
# @todo
# (1) introduced spread
# create graphs to show dependency of arbitrage on n (steps) and r (interest rate)
