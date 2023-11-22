import csv
from itertools import combinations
import time


def which_file():
    print("sur quel donnée appliquer l algorithme?")
    print("0: données de test ")
    print("1: données du dataset 1")
    print("2: données du dataset 2")
    file_to_use = int(input("votre choix"))
    if file_to_use == 0:
        return 'dataset.csv'
    if file_to_use == 1:
        return 'dataset1.csv'
    if file_to_use == 2:
        return 'dataset2.csv'


def max_invest():
    budget_limit = input("rentrez un budget (budget de base 500)")
    if not budget_limit.isnumeric():
        budget_limit = 500
    else:
        budget_limit = int(budget_limit)
    print("budget_limit: ", budget_limit)
    return budget_limit


def find_all_combinations(csv_file, budget_limit=500):
    # complexité de
    all_combinations = []

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # pas lire la premiere ligne

        share_data = [(row[0], float(row[1]), float(row[2].strip('%')) / 100)
                      for row in csv_reader]
        share_data = [share for share in share_data if share[1] > 0]
        s = 1
        t = 1

        for r in range(1, len(share_data) + 1):
            # Pour tout element du dataset (donc n)
            print(s, t)
            t = t + 1
            # pour toute les actions on va tester toute les combinaison avec cette action
            for combination in combinations(share_data, r):
                s = s + 1
                # on fait les diffenretes combinaisons
                total_price = sum(share[1] for share in combination)
                # on additionne les prix des actions pour chaque combinaison
                total_profit = sum(share[1] * share[2] for share in combination)
                # on calcul le profit par action et on l additionee au profit total
                if total_price <= budget_limit:
                    # si le prix de la combinaison < limite de budget on retourne la combinaison
                    combination_info = {
                        'actions': [share[0] for share in combination],
                        'total_spent': total_price,
                        'total_profit': total_profit
                    }
                    all_combinations.append(combination_info)

    # plus grand benefice d abord
    all_combinations = sorted(all_combinations,
                              key=lambda x: x['total_profit'],
                              reverse=True)

    return all_combinations


if __name__ == "__main__":
    csv_file = which_file()
    budget_limit = max_invest()
    start_time = time.time()
    all_combinations = find_all_combinations(csv_file, budget_limit)
    end_time = time.time()
    i = 0
    for idx, combination in enumerate(all_combinations):
        i = +1
        if idx == 10:
            break
        print(f"Combinaison {idx + 1}:")
        print(
            f"Il faut acheter les actions: {', '.join(combination['actions'])}")
        print(f"Total Dépensé: {combination['total_spent']}")
        print(f"Profit total (hors capital): {combination['total_profit']}")
    print(f"Temps d'exécution: {end_time - start_time} secondes")
