#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 16:14:36 2018

@author: harish

Computes p-value using Wald-Wolfowittz runs test
to check for effect of 'momentum' -
i.e. if wins and losses are IID
"""

from pathlib import Path
from math import sqrt
import scipy.stats as st

home = str(Path.home())
start_year = 2002
data_file_name = home+"/Documents/nfl_stats/nfl_elo.csv"  # Input file path


def calcNumRuns(seq):
    """
    Calculate the number of runs given a sequence
    """
    r = 1
    i = 1
    cur_run = seq[0]
    while i < len(seq):
        new_result = seq[i]
        if new_result != cur_run:
            r += 1
            cur_run = new_result
        i += 1
    return r


def calcPercs(team):
    """
    Calculate games won/lost after a game won/lost
    """
    res_after_win, res_after_loss = [], []
    seq = result_seq[team]
    i = 1
    cur_run = seq[0]
    while i < len(seq):
        new_result = seq[i]
        if cur_run == "W":
            res_after_win.append(new_result)
        else:
            res_after_loss.append(new_result)
        cur_run = new_result
        i += 1
    return res_after_win, res_after_loss


def calcZ(seq):
    """
    Calc z score and p-value for a normal distribution
    given a sequence of wins and losses
    """
    n1, n2 = seq.count("L"), seq.count("W")
    n = n1 + n2
    assert len(set(seq)) == 2
    assert n == len(seq)
    mean = ((2 * n1 * n2) / n) + 1
    variance = ((mean - 1) * (mean - 2)) / (n - 1)
    std_dev = sqrt(variance)
    r = calcNumRuns(seq)
    z = (r - mean) / std_dev
    p_value = st.norm.sf(abs(z))*2
    return z, p_value

result_seq = {}  # Results seq for each team

data_file = open(data_file_name)
data_file.readline()  # Ignore header line
for line in data_file:

    line_split = line.strip().split(",")
    season, playoff = int(line_split[1]), line_split[3]

    if season >= start_year and playoff == "":

        home_team, away_team = line_split[4], line_split[5]
        home_score, away_score = int(line_split[-2]), int(line_split[-1])

        if home_team not in result_seq:
            result_seq[home_team] = []
        if away_team not in result_seq:
            result_seq[away_team] = []

        if home_score > away_score:
            result_seq[home_team].append("W")
            result_seq[away_team].append("L")

        elif away_score > home_score:
            result_seq[away_team].append("W")
            result_seq[home_team].append("L")

data_file.close()

for team in result_seq:
    seq = result_seq[team]
    z, p_value = calcZ(seq)
    print(team, abs(z), p_value)

    momentum_win_seq, momentum_loss_seq = calcPercs(team)
    win_perc = round(seq[1:].count("W") * 100 / len(seq[1:]), 2)
    loss_perc = round(seq[1:].count("L") * 100 / len(seq[1:]), 2)
    momentum_win_perc = round(momentum_win_seq.count("W") * 100 /
                              len(momentum_win_seq), 2)
    momentum_loss_perc = round(momentum_loss_seq.count("L") * 100 /
                               len(momentum_loss_seq), 2)
    #print(team, win_perc, momentum_win_perc, loss_perc, momentum_loss_perc)
