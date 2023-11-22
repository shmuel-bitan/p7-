import csv
from brutforce import which_file, max_invest
import time

def knapsack(max_invest, csv_file):
    # Read data from the CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        shares_list = [(row[0], float(row[1]), float(row[2].strip('%'))) for row in csv_reader]

    # Convert percentage values to decimal
    shares_list = [(row[0], row[1], row[2] / 100) for row in shares_list]

    # Filter out shares with non-positive prices
    shares_list = [action for action in shares_list if action[1] > 0]

    num_shares = len(shares_list)
    max_inv = int(max_invest * 100)  # capacity
    shares_total = len(shares_list)
    cost = []  # weights
    profit = []  # values

    for share in shares_list:
        cost.append(int(share[1] * 100))
        profit.append(int(share[2] * share[1] * 100))

    # Find optimal profit
    ks = [[0 for _ in range(max_inv + 1)] for _ in range(shares_total + 1)]

    for i in range(1, shares_total + 1):
        for w in range(1, max_inv + 1):
            if cost[i - 1] <= w:
                ks[i][w] = max(profit[i - 1] + ks[i - 1][w - cost[i - 1]], ks[i - 1][w])
            else:
                ks[i][w] = ks[i - 1][w]

    # Retrieve combination of shares from optimal profit
    best_combo = []
    i, w = shares_total, max_inv

    while i > 0 and w > 0:
        if ks[i][w] != ks[i - 1][w]:
            best_combo.append(shares_list[i - 1])
            w -= cost[i - 1]
        i -= 1

    return best_combo


# Example usage
if __name__ == "__main__":
    csv_file = which_file()  # Corrected the function name
    max_invest_amount = max_invest()
    total_spent = 0
    total_benefit = 0
    start_time = time.time()
    best_combination = knapsack(max_invest_amount, csv_file)
    end_time = time.time()
    # Display the results
    print("\nMeilleur combinaison:")
    for action in best_combination:
        print(f"{action[0]} - Prix: {action[1]} - Benefice: {action[2] * action[1]}")
        total_benefit += action[2] * action[1]
        total_spent += action[1]
    print(f"Total dépensé: {total_spent}")
    print(f"Bénéfice Total ( sans capital ): {total_benefit}")
    print(f"Temps d'exécution: {end_time- start_time} secondes")