import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

## reward table

new_win_0 = {"gold": 0,"ticket": 0,"jackpot": 0}
new_win_1 = {"gold": 0,"ticket": 0,"jackpot": 0}
new_win_2 = {"gold": 35,"ticket": 0,"jackpot": 0}
new_win_3 = {"gold": 55,"ticket": 0,"jackpot": 0}
new_win_4 = {"gold": 100,"ticket": 0,"jackpot": 0}
new_win_5 = {"gold": 0,"ticket": 1,"jackpot": 0}
new_win_6 = {"gold": 0,"ticket": 1,"jackpot": 0.05}
new_win_7 = {"gold": 0,"ticket": 2,"jackpot": 0.06}
new_win_8 = {"gold": 0,"ticket": 2,"jackpot": 0.07}
new_win_9 = {"gold": 0,"ticket": 2,"jackpot": 0.08}
new_win_10 = {"gold": 0,"ticket": 2,"jackpot": 0.09}
new_win_11 = {"gold": 0,"ticket": 2,"jackpot": 0.1}
new_win_12 = {"gold": 0,"ticket": 2,"jackpot": 0.11}
new_win_12_l_1 = {"gold": 0,"ticket": 2,"jackpot": 0.12}
new_win_12_l_0 = {"gold": 0,"ticket": 2,"jackpot": 0.13}

# Define the old reward table

old_win_0 = {"gold": 0,"ticket": 0,"jackpot": 9}
old_win_1 = {"gold": 0,"ticket": 0,"jackpot": 11}
old_win_2 = {"gold": 0,"ticket": 0,"jackpot": 15}
old_win_3 = {"gold": 30,"ticket": 0,"jackpot": 7}
old_win_4 = {"gold": 55,"ticket": 0,"jackpot": 7}
old_win_5 = {"gold": 55,"ticket": 0,"jackpot": 17}
old_win_6 = {"gold": 75,"ticket": 0,"jackpot": 17}
old_win_7 = {"gold": 155,"ticket": 0,"jackpot": 7}
old_win_8 = {"gold": 155,"ticket": 0,"jackpot": 15}
old_win_9 = {"gold": 155,"ticket": 0,"jackpot": 27}
old_win_10 = {"gold": 175,"ticket": 0,"jackpot": 45}
old_win_11 = {"gold": 200,"ticket": 0,"jackpot": 56}
old_win_12 = {"gold": 250,"ticket": 0,"jackpot": 49}







reward_table = [new_win_0, new_win_1, new_win_2, new_win_3, new_win_4, new_win_5, new_win_6, new_win_7, new_win_8, new_win_9, new_win_10, new_win_11, new_win_12, new_win_12_l_1, new_win_12_l_0]
reward_table_old = [old_win_0, old_win_1, old_win_2, old_win_3, old_win_4, old_win_5, old_win_6, old_win_7, old_win_8, old_win_9, old_win_10, old_win_11, old_win_12]

def get_gold(win):
    return reward_table[win]["gold"]+reward_table[win]["ticket"]*150+stats.bernoulli.rvs(reward_table[win]["jackpot"],size=1)[0]*2000

def get_gold_old(win):
    return reward_table_old[win]["gold"]+reward_table_old[win]["jackpot"]

def arena_result(winrate, model="new"):
    if model == "new":
        lose = 0
        win = 0
        while lose <3 and win <12:
            if stats.bernoulli.rvs(winrate, size=1)[0] == 1:
                win += 1
            else:
                lose += 1
        return [get_gold(win+lose-3), win, lose]
    else:
        lose = 0
        win = 0
        while lose <3 and win <12:
            if stats.bernoulli.rvs(winrate, size=1)[0] == 1:
                win += 1
            else:
                lose += 1
        return [get_gold_old(win+lose-3), win, lose]


i = 0
number_of_tests = 1000
max_game = 200
results = []
old_results = []
starting_gold = 3000
winrate = 0.727


for i in range(number_of_tests):
    gold = starting_gold
    game = 0
    player_win_games = 0
    while gold > 300 and game < max_game:
    # while game < max_game:
        gold += -300
        result = arena_result(winrate)
        player_win_games += result[1]
        gold += result[0]
        game += 1
    player_win_games_avg = player_win_games / game
    results.append([game,gold,player_win_games_avg])

    # old model
    # while gold > 300 and game < max_game:

for i in range(number_of_tests):
    gold = starting_gold
    game = 0
    player_win_games = 0
    while gold > 150 and game < max_game:
    # while game < max_game:
        gold += -150
        old_result = arena_result(winrate, model="old")
        player_win_games += old_result[1]
        gold += old_result[0]
        game += 1
    player_win_games_avg = player_win_games / game
    old_results.append([game,gold,player_win_games_avg])

results = pd.DataFrame(results, columns=["games", "gold", "player_win_games_avg"])
old_results = pd.DataFrame(old_results, columns=["games", "gold", "player_win_games_avg"])

# histogram of games played: new model
plt.figure(figsize=(10, 6))
sns.histplot(results["games"], bins=max_game, kde=True)
plt.title("Distribution of Games Played")
plt.xlabel("Number of Games Played")
plt.ylabel("Frequency")
plt.axvline(results["games"].mean(), color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.legend()
plt.show()
plt.savefig("games_played_distribution_new.png")

# histogram of games played: old model
plt.figure(figsize=(10, 6))
sns.histplot(old_results["games"], bins=max_game, kde=True)
plt.title("Distribution of Games Played (Old Model)")
plt.xlabel("Number of Games Played")
plt.ylabel("Frequency")
plt.axvline(old_results["games"].mean(), color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.legend()
plt.show()
plt.savefig("games_played_distribution_old.png")



# histogram of gold: new model
plt.figure(figsize=(10, 6))
sns.histplot(results["gold"], bins=30, kde=True)
plt.title("Distribution of Gold at End of Games")
plt.xlabel("Gold")
plt.ylabel("Frequency")
plt.axvline(results["gold"].mean(), color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(results["gold"].quantile(0.5), color='green', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(results["gold"].quantile(0.75), color='blue', linestyle='dashed', linewidth=1, label='75th Percentile')
plt.axvline(results["gold"].quantile(0.25), color='orange', linestyle='dashed', linewidth=1, label='25th Percentile')
plt.legend()
plt.show()
plt.savefig("gold_distribution_new.png")
# Print summary statistics

# histogram of gold: old model
plt.figure(figsize=(10, 6))
sns.histplot(old_results["gold"], bins=30, kde=True)
plt.title("Distribution of Gold at End of Games (Old Model)")
plt.xlabel("Gold")
plt.ylabel("Frequency")
plt.axvline(old_results["gold"].mean(), color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(old_results["gold"].quantile(0.5), color='green', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(old_results["gold"].quantile(0.75), color='blue', linestyle='dashed', linewidth=1, label='75th Percentile')
plt.axvline(old_results["gold"].quantile(0.25), color='orange', linestyle='dashed', linewidth=1, label='25th Percentile')
plt.legend()
plt.show()
plt.savefig("gold_distribution_old.png")


# Print summary statistics: new model
print("Average winning:", results["player_win_games_avg"].mean())
print("More than max games:", results["games"][results["games"] >= max_game].count())
print("Median games played:", results["games"].median())
print("Average games played:", results["games"].mean())
print("Average gold:", results["gold"].mean())
print("Median gold:", results["gold"].median())
print("75th percentile gold:", results["gold"].quantile(0.75))
print("25th percentile gold:", results["gold"].quantile(0.25))

# Print summary statistics: old model
print("Average winning (old model):", old_results["player_win_games_avg"].mean())
print("More than max games (old model):", old_results["games"][old_results["games"] >= max_game].count())
print("Median games played (old model):", old_results["games"].median())
print("Average games played (old model):", old_results["games"].mean())
print("Average gold (old model):", old_results["gold"].mean())
print("Median gold (old model):", old_results["gold"].median())
print("75th percentile gold (old model):", old_results["gold"].quantile(0.75))
print("25th percentile gold (old model):", old_results["gold"].quantile(0.25))