#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 23:52:31 2018

@author: harish

This script looks at kickers' stats -
FG made and FG perc.

Computes correlation between college stats and
pro career, using weighted career approx value as the metric
to measure a player's pro career's value
"""
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns

url = "https://www.pro-football-reference.com/play-index/draft-finder.cgi?" + \
      "request=1&year_min=1936&year_max=2017&type=B&draft_slot_min=1&draft_slot" + \
      "_max=500&pick_type=overall&pos%5B%5D=k&conference=any&show=p&order_by=def" + \
      "ault"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table', attrs={'class': 'sortable stats_table'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')

AVs, FGMs, FGPs = [], [], []
for row in rows:  # Read each row of the table
    data = row.find_all('td')
    data = [element.text.strip() for element in data]
    if len(data) > 0 and data[13]:
        links = row.find_all('a')
        if len(links) > 4:
            player, AV = data[3], int(data[12])
            college_link = links[-1].get('href')
            college_page = requests.get(college_link)
            soup2 = BeautifulSoup(college_page.content, 'html.parser')
            table2 = soup2.find('table', attrs={'class': 'sortable stats_table',
                                                'id': 'kicking'})
            if table2:  # Table 2 exists
                table2_foot = table2.find('tfoot')
                rows2 = table2_foot.find_all('tr')
                for row2 in rows2:
                    college_data = row2.find_all('td')
                    college_data = [element.text.strip() for element in college_data]
                    FGM, FGP = int(college_data[8]), float(college_data[10])
                    AVs.append(AV)
                    FGMs.append(FGM)
                    FGPs.append(FGP)
                    print(player, college_link, AV, FGM, FGP)

# Plotting

DPI = 1000

f1, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

corr1, pval1 = pearsonr(FGMs, AVs)
ax1.scatter(FGMs, AVs)
ax1.annotate('Corr coeff: ' + str(round(corr1, 2)),
             xy=(0.6, 0.9), xycoords='axes fraction')
ax1.set_xlabel('Field Goals Made')
ax1.set_ylabel('AV')
ax1.set_xlim([20, 100])

corr2, pval2 = pearsonr(FGPs, AVs)
ax2.scatter(FGPs, AVs)
ax2.annotate('Corr coeff: ' + str(round(corr2, 2)),
             xy=(0.6, 0.9), xycoords='axes fraction')
ax2.set_xlabel('Field Goals Percentage')
ax2.set_xlim([50, 100])

plt.tight_layout()
f1.savefig("Kicking.png", format="png", dpi=DPI)
