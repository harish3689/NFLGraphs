#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 08:45:41 2018

@author: harish

Compute Passer Rating+ for each QB
- Per season and avg over his career
"""

from bs4 import BeautifulSoup
import requests
import numpy as np

start_year, end_year = 1970, 2017  # Start and end year for analysis
att_cutoff = 200  # Min number of attempts to consider
years_cutoff = 8  # Min number of seasons played to consider


class QBPasserRatingPlus():
    """
    PR+ for each QB for each season
    """
    def __init__(self, name, year, score):
        self.name = name
        self.year = year
        self.score = score

    def __repr__(self):
        return str(self.name) + " - "+str(self.year) + " , "+str(self.score)


class QBPasserRatingPlusAvg():
    """
    Avg PR+ for each QB over his entire career
    """
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return str(self.name) + " - " + str(self.score)

season_avgrate, qbs_passrateplus = {}, []
for year in range(start_year, end_year + 1):
    print(year)
    passer_ratings, qbs_ratings = [], {}

    # Gather info from website
    url = "https://www.pro-football-reference.com/years/" + str(year) + \
          "/passing.htm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'sortable stats_table'})

    # Confirm that column headings are correct
    header = table.find('thead')
    header_row = header.find('tr')
    header_row_cols = header_row.find_all('th')
    att_head = header_row_cols[9].get_text()
    rate_head = header_row_cols[21].get_text()
    assert att_head == "Att"
    assert rate_head == "Rate"

    # Read table body
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:  # Read each row of the table
        data = row.find_all('td')
        data = [element.text.strip() for element in data]
        if len(data) > 0:  # Not header
            player, att, rate = data[0], int(data[8]), float(data[20])
            player = player.strip("*+")
            if att >= att_cutoff:
                passer_ratings.append(rate)
                qbs_ratings[player] = rate

    # Compute the average
    avg_rate = round(np.mean(passer_ratings), 2)
    season_avgrate[year] = avg_rate

    # Store the info in a list
    for player in qbs_ratings:
        pass_rate_plus = round(qbs_ratings[player] * 100 / avg_rate, 2)
        qb_psr_obj = QBPasserRatingPlus(player, year, pass_rate_plus)
        qbs_passrateplus.append(qb_psr_obj)

qbs_passrateplus.sort(key=lambda x: x.score, reverse=True)

# Compute avg of pass rate plus for each player with min years
qbs_prpavg_dict, qbs_prpavg = {}, []
for obj in qbs_passrateplus:
    name, score = obj.name, obj.score
    if name not in qbs_prpavg_dict:
        qbs_prpavg_dict[name] = []
    qbs_prpavg_dict[name].append(score)

for name in qbs_prpavg_dict:
    scores = qbs_prpavg_dict[name]
    if len(scores) >= years_cutoff:
        avg_score = round(np.mean(scores), 2)
        obj = QBPasserRatingPlusAvg(name, avg_score)
        qbs_prpavg.append(obj)

qbs_prpavg.sort(key=lambda x: x.score, reverse=True)

for season in season_avgrate:
    print(season, season_avgrate[season])

print(len(qbs_passrateplus))
print(qbs_passrateplus[:25])
print(len(qbs_prpavg))
print(qbs_prpavg[:25])
