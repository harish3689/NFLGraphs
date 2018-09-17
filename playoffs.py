#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 13:25:50 2018

@author: harish

Number of wins typically required to make the playoffs.
Number of teams that have a better rec than playoff teams but dont make it.
"""
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib

div_symbol = '*'
wc_symbol = '+'
seasons = [season for season in range(2002, 2018)]


def read_url(season, url):
    """
    Read a web page and find a table
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = []
    tables = soup.find_all('table',
                           attrs={'class':
                                  'suppress_all sortable stats_table'})
    if len(tables) == 0:
        tables = soup.find_all('table',
                               attrs={'class': 'sortable stats_table'})
    assert len(tables) == 2
    return tables

playoff_wins, wc_wins, unlucky_wins = [], [], []
for season in seasons:
    cur_season_playoff_wins = []
    cur_season_nonplayoff_wins = []
    url = 'https://www.pro-football-reference.com/years/' + str(season) + '/'
    tables = read_url(season, url)
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:
            data = row.find_all('td')
            if len(data) > 1:
                assert data[0]['data-stat'] == 'wins'
                data_content = [element.text.strip() for element in data]
                wins = int(data_content[0])
                team = row.find('th').text.strip()
                if team[-1] == div_symbol:
                    if wins == 8:
                        print(season, team, 'Div')
                    playoff_wins.append(wins)
                    cur_season_playoff_wins.append(wins)
                elif team[-1] == wc_symbol:
                    if wins == 8:
                        print(season, team, 'WC')
                    wc_wins.append(wins)
                    playoff_wins.append(wins)
                    cur_season_playoff_wins.append(wins)
                else:
                    cur_season_nonplayoff_wins.append((team, wins))
    for tup in cur_season_nonplayoff_wins:
        team, win = tup
        if win > min(cur_season_playoff_wins):
            unlucky_wins.append(win)
            #print(season, team, win)


playoff_wins_set = set(playoff_wins)
wc_wins_set = set(wc_wins)
unlucky_wins_set = set(unlucky_wins)

playoff_hist, wc_hist, unlucky_hist = {}, {}, {}
for win in playoff_wins_set:
    playoff_hist[win] = playoff_wins.count(win) * 100 / len(playoff_wins)
for win in wc_wins_set:
    wc_hist[win] = wc_wins.count(win) * 100 / len(wc_wins)
for win in unlucky_wins_set:
    unlucky_hist[win] = unlucky_wins.count(win) * 100 / len(unlucky_wins)

#x_ticks = [i for i in range(0, 18)]
#matplotlib.rcParams.update({'font.size': 14})
#
#plt.figure(figsize=(10, 10))
#plt.bar(list(playoff_hist.keys()), list(playoff_hist.values()))
#plt.xlabel('Number of wins')
#plt.ylabel('Frequency (%)')
#plt.title('NFL Playoff teams: 2002-2017')
#plt.xlim([x_ticks[0], x_ticks[-1]])
#plt.ylim([0, 60])
#plt.xticks(x_ticks)
#plt.savefig('nflgraphs_8-1.png', DPI=1000)
#
#plt.figure(figsize=(10, 10))
#plt.bar(list(wc_hist.keys()), list(wc_hist.values()))
#plt.xlabel('Number of wins')
#plt.ylabel('Frequency (%)')
#plt.title('NFL Wild Card teams: 2002-2017')
#plt.xlim([x_ticks[0], x_ticks[-1]])
#plt.ylim([0, 60])
#plt.xticks(x_ticks)
#plt.savefig('nflgraphs_8-2.png', DPI=1000)
#
#plt.figure(figsize=(10, 10))
#plt.bar(list(unlucky_hist.keys()), list(unlucky_hist.values()))
#plt.xlabel('Number of wins')
#plt.ylabel('Frequency (%)')
#plt.title('NFL non-playoff teams with a better record\n' +
#          'than playoff teams: 2002-2017')
#plt.xlim([x_ticks[0], x_ticks[-1]])
#plt.ylim([0, 60])
#plt.xticks(x_ticks)
#plt.savefig('nflgraphs_8-3.png', DPI=1000)
