#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 2019

@author: harish

Calculate % of 3rd down converted by rushing and by passing
Compute yards to go on 3rd down for each play type
Also compute % of yards needed that was gained when failed
"""

import pandas as pd
import operator
import matplotlib.pyplot as plt
import matplotlib

file_name = 'nfl_playbyplay_2009-2018.csv'

play_types = ['run', 'pass']
groups = ['1-3', '4-6', '7-10', '>10']  # Yards to go categories

total_plays, count, count_success, = 0, {}, {}
yards_to_go = {}
for g in groups:
    yards_to_go[g] = {}
    for play in play_types:
        yards_to_go[g][play] = {}
        yards_to_go[g][play]['Converted'] = 0
        yards_to_go[g][play]['Not converted'] = 0
yards_gained_failed = {}  # Yards gained when failed on 3rd down
frac_gained_failed = {}  # Perc of yards gained when failed on 3rd down
for play in play_types:
    count[play], count_success[play] = 0, 0
    frac_gained_failed[play], yards_gained_failed[play] = [], []

content = pd.read_csv(file_name, low_memory=False)

for index, row in content.iterrows():

    down, play_type, ydstogo = row['down'], row['play_type'], row['ydstogo']
    yards_gained = row['yards_gained']
    third_down_converted = row['third_down_converted']
    third_down_failed = row['third_down_failed']
    desc = row['desc']

    group = ''
    if 1 <= ydstogo <= 3:
        group = '1-3'
    elif 4 <= ydstogo <= 6:
        group = '4-6'
    elif 7 <= ydstogo <= 10:
        group = '7-10'
    elif ydstogo > 10:
        group = '>10'

    if down == 3 and play_type in play_types:
        count[play_type] += 1
        if third_down_converted == 1 and third_down_failed == 0:
            count_success[play_type] += 1
            yards_to_go[group][play_type]['Converted'] += 1
        elif third_down_failed == 1 and third_down_converted == 0:
            if yards_gained < ydstogo:  # Because of fumble, recovery, etc.
                yards_gained_failed[play_type].append(yards_gained)
                frac_gained = round(yards_gained / ydstogo, 2)
                frac_gained_failed[play_type].append(frac_gained)
                yards_to_go[group][play_type]['Not converted'] += 1

print('Total plays:', count)
print('Successful plays:', count_success)
print(yards_to_go)

DPI = 1000
matplotlib.rcParams.update({'font.size': 14})

colors = {}
colors['run'] = 'red'
colors['pass'] = 'blue'

# Plot 1 - Yards to go for run/pass plays
"""f1 = plt.figure(figsize=(8, 8))
for play in play_types:
    d = {}
    for yds in yards_to_go[play]:
        if yds in d:
            d[yds] += 1
        else:
            d[yds] = 1
    for yds in d:
        d[yds] = d[yds] * 100 / len(yards_to_go[play])
    sorted_dict = sorted(d.items(), key=operator.itemgetter(1))[-1::-1]
    x = [item[0] for item in sorted_dict]
    y = [item[1] for item in sorted_dict]
    plt.scatter(x, y, color=colors[play], label=play.capitalize())
plt.xlabel("Yards to go")
plt.ylabel("Frequency")
plt.title("All third down plays: 2009-2018")
plt.legend()
plt.tight_layout()
f1.savefig("Third_Down-1.png", format="png", dpi=DPI)"""

plt.clf()

# Plot 2 - Fraction of yards gained on failed third downs
f2 = plt.figure(figsize=(8, 8))
for play in play_types:
    d = {}
    for frac in frac_gained_failed[play]:
        f = max(0, frac)
        if f in d:
            d[f] += 1
        else:
            d[f] = 1
    for f in d:
        d[f] = d[f] * 100 / len(frac_gained_failed[play])
    sorted_dict = sorted(d.items(), key=operator.itemgetter(1))[-1::-1]
    x = [item[0] for item in sorted_dict]
    y = [item[1] for item in sorted_dict]
    plt.scatter(x, y, color=colors[play], label=play.capitalize())
plt.xlabel("Fraction of yards needed gained")
plt.ylabel("Frequency")
plt.title("Third down plays not converted: 2009-2018")
plt.legend()
plt.tight_layout()
f2.savefig("Third_Down-2.png", format="png", dpi=DPI)

# Plot 3 - Yards gained on failed third downs
f3 = plt.figure(figsize=(8, 8))
for play in play_types:
    d = {}
    for yds in yards_gained_failed[play]:
        if yds in d:
            d[yds] += 1
        else:
            d[yds] = 1
    for yds in d:
        d[yds] = d[yds] * 100 / len(yards_gained_failed[play])
    sorted_dict = sorted(d.items(), key=operator.itemgetter(1))[-1::-1]
    x = [item[0] for item in sorted_dict]
    y = [item[1] for item in sorted_dict]
    plt.scatter(x, y, color=colors[play], label=play.capitalize())
plt.xlabel("Yards gained")
plt.ylabel("Frequency")
plt.title("Third down plays not converted: 2009-2018")
plt.legend()
plt.tight_layout()
f3.savefig("Third_Down-3.png", format="png", dpi=DPI)
