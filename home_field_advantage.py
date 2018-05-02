#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 16:40:45 2018

@author: harish

This script reads FiveThirtyEight's NFL data file and
tests for home field advantage.
Chi square test is used for hypothesis testing.
Games are divided into regular season games and
playoff games (minus SB)
"""
from scipy.stats import chisquare
import matplotlib.pyplot as plt
import seaborn as sns

start_year = 1970  # Since AFL-NFL merger
data_file_name = "nfl_elo.csv"  # Input file containing data on all the games

num_games = {}  # Number of reg season and playoff games
num_games["reg"], num_games["playoff"] = 0, 0
home_wins = {}  # Number of wins by the home team
home_wins["reg"], home_wins["playoff"] = 0, 0
away_wins = {}  # Number of wins by the away team
away_wins["reg"], away_wins["playoff"] = 0, 0
ties = 0
season_games, season_homewins = {}, {}

data_file = open(data_file_name)
data_file.readline()  # Ignore header line
for line in data_file:

    line_split = line.strip().split(",")
    season = int(line_split[1])

    if season >= start_year:

        playoff = line_split[3]
        game_type = "reg" if playoff == "" else "playoff"
        if playoff == "s":  # Ignore SB
            continue

        home_score, away_score = int(line_split[-2]), int(line_split[-1])

        num_games[game_type] += 1

        if home_score == away_score:
            ties += 1
        elif home_score > away_score:
            home_wins[game_type] += 1
        else:
            away_wins[game_type] += 1

        if game_type == "reg":
            if season in season_games:
                season_games[season] += 1
            else:
                season_games[season] = 1
            if home_score > away_score:
                if season in season_homewins:
                    season_homewins[season] += 1
                else:
                    season_homewins[season] = 1

data_file.close()

assert num_games["reg"] == home_wins["reg"] + away_wins["reg"] + ties
assert num_games["playoff"] == home_wins["playoff"] + away_wins["playoff"]

# Calc perc of games won by home team
home_reg_perc = round(100 * home_wins["reg"] / num_games["reg"], 2)
home_playoff_perc = round(100 * home_wins["playoff"] / num_games["playoff"], 2)

# Perform chi square test
reg_array = [home_wins["reg"], away_wins["reg"]]
playoff_array = [home_wins["playoff"], away_wins["playoff"]]
chisq_reg, pvalue_reg = chisquare(reg_array)
chisq_playoff, pvalue_playoff = chisquare(playoff_array)

print("Number of ties: ", ties)
print("Number of regular season games: ", num_games["reg"])
print("Number of games won by home team: ", home_wins["reg"])
print("Percentage of games won by home team: ", home_reg_perc)
print("p-value from chi square test: ", pvalue_reg)
print("Number of playoff games: ", num_games["playoff"])
print("Number of games won by home team: ", home_wins["playoff"])
print("Percentage of games won by home team: ", home_playoff_perc)
print("p-value from chi square test: ", pvalue_playoff)

# Plotting
for season in season_games:
    season_homewins[season] = round(100 * season_homewins[season] /
                                    season_games[season], 2)
x = list(season_homewins.keys())
y = list(season_homewins.values())

DPI = 1000
plt.figure()
sns.barplot(x, y, color="blue")
plt.ylim(0, 100)
plt.xticks(rotation=90)
plt.xlabel("Season")
plt.ylabel("Percentage of games won by home team")
plt.title("Home field advantage in the NFL - regular season games")
plt.savefig("Home_Field_Advantage.eps", format="eps", dpi=DPI)
