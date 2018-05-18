#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:38:43 2018

@author: harish

Examine how good each team has been at drafting

Value of a particular pick is assessed by using PFR's weighted career
approximate value

Jimmy Johnson's trade value chart is used for assessing the value of a
particular pick position
"""
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import numpy as np
import operator
import matplotlib.pyplot as plt
import seaborn as sns

start_year, end_year = 2002, 2014
home = str(Path.home())
tradevalue_filename = home + \
                      '/Documents/nfl_stats/jimmyjohnson_tradevalue_chart.csv'

# Read the trade value chart
picks_values = {}
tradevalue_file = open(tradevalue_filename)
tradevalue_file.readline()  # Ignore header line
for line in tradevalue_file:
    line = line.strip().split(",")
    pick, value = int(line[1]), int(line[2])
    picks_values[pick] = value
tradevalue_file.close()

# Normalize pick values
min_val, max_val = 1, 3000
for pick in picks_values:
    picks_values[pick] = (picks_values[pick] - min_val) / (max_val - min_val)
lowest_pickvalue = (2 - 1) / (max_val - min_val)  # For picks lower than #224

# Read draft results for each year
teams_draftscores, teams_pickvalues = {}, {}
for year in range(start_year, end_year+1):
    print("Collecting data for:", year)
    url = 'https://www.pro-football-reference.com/years/' + \
          str(year)+'/draft.htm'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'sortable stats_table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:  # Read each row of the table
        data = row.find_all('td')
        data = [element.text.strip() for element in data]

        if len(data) > 0:  # Not header line
            pick, team = int(data[0]), data[1]

            # Update names of teams
            if team == "BOS":
                team = "NWE"
            elif team == "RAI":
                team = "OAK"
            elif team == "PHO":
                team = "ARI"
            elif team == "STL":
                team = "RAM"

            if team not in teams_draftscores:
                teams_draftscores[team] = []
                teams_pickvalues[team] = []

            pick_value = 'initialize'
            if pick in picks_values:
                pick_value = picks_values[pick]
            else:
                pick_value = lowest_pickvalue

            if data[9]:
                CarAV = int(data[9])
                score = CarAV / pick_value
                teams_draftscores[team].append(score)
                teams_pickvalues[team].append(pick_value)

for t in teams_draftscores:
    print(t, len(teams_draftscores[t]),
          np.mean(teams_pickvalues[t]), np.mean(teams_draftscores[t]))

# Plotting starts

DPI = 1000

# Plot 1 - Number of picks made by each team
plot1_dict = {}
for team in teams_pickvalues:
    plot1_dict[team] = len(teams_pickvalues[team])
sorted_dict1 = sorted(plot1_dict.items(), key=operator.itemgetter(1))[-1::-1]
x1 = [item[0] for item in sorted_dict1]
y1 = [item[1] for item in sorted_dict1]
f1 = plt.figure()
sns.barplot(x1, y1, color="blue")
plt.xticks(rotation=90)
plt.xlabel("Team")
plt.ylabel("Number of draft picks")
f1.savefig("Draft-1.png", format="png", dpi=DPI)

# Compute average of pick values and draft scores
for team in teams_pickvalues:
    teams_pickvalues[team] = np.mean(teams_pickvalues[team])
    teams_draftscores[team] = np.mean(teams_draftscores[team])

# Plot 2 - Average pick position value
sorted_dict2 = sorted(teams_pickvalues.items(),
                      key=operator.itemgetter(1))[-1::-1]
x2 = [item[0] for item in sorted_dict2]
y2 = [item[1] for item in sorted_dict2]
f2 = plt.figure()
sns.barplot(x2, y2, color="blue")
plt.xticks(rotation=90)
plt.xlabel("Team")
plt.ylabel("Average Draft Pick Trade Value")
f2.savefig("Draft-2.png", format="png", dpi=DPI)

# Plot 3 - Average Draft Score
sorted_dict3 = sorted(teams_draftscores.items(),
                      key=operator.itemgetter(1))[-1::-1]
x3 = [item[0] for item in sorted_dict3]
y3 = [item[1] for item in sorted_dict3]
f3 = plt.figure()
sns.barplot(x3, y3, color="blue")
plt.xticks(rotation=90)
plt.xlabel("Team")
plt.ylabel("Average Draft Score")
f3.savefig("Draft-3.png", format="png", dpi=DPI)
