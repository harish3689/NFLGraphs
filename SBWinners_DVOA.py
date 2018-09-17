#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 22:24:40 2018

@author: harish

Compare Off and Def DVOA for SB winners
"""
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from bokeh.plotting import figure
from bokeh.charts import output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import export_svgs

home = str(Path.home())
start_year = 1986  # First year for which DVOA is available
end_year = 2017  # Last year to work on

sb_winners = {}
sbwinners_filename = home + '/Documents/nfl_stats/sb_winners.txt'
sbwinners_file = open(sbwinners_filename)
for line in sbwinners_file:
    line = line.strip().split()
    year, team = int(line[0]), line[1]
    sb_winners[year] = team
sbwinners_file.close()


def read_url(url):
    """
    Read a web page and find a table
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'stats'})
    return table

off_ranks, def_ranks, infos = [], [], []
for year in range(start_year, end_year + 1):
    print(year)
    off_url = 'https://www.footballoutsiders.com/stats/teamoff' + str(year)
    def_url = 'https://www.footballoutsiders.com/stats/teamdef' + str(year)
    off_table, def_table = read_url(off_url), read_url(def_url)
    off_rows, def_rows = off_table.find_all('tr'), def_table.find_all('tr')

    # Assert that headers are correct
    off_header = off_rows[0].find_all('td')
    def_header = def_rows[0].find_all('td')
    off_header = [element.text.strip() for element in off_header]
    def_header = [element.text.strip() for element in def_header]
    assert off_header[1] == 'TEAM' and off_header[2] == 'OFF.DVOA'
    assert def_header[1] == 'TEAM' and def_header[2] == 'DEF.DVOA'

    # Read off table body
    for row in off_rows[2:]:  # Each row of the table
        data = row.find_all('td')
        data = [element.text.strip() for element in data]
        if len(data) > 0 and data[0] != '':  # Not header
            rank, team = int(data[0]), data[1]
            if team == sb_winners[year]:
                off_ranks.append(rank)
                info = team+'-'+str(year)
                infos.append(info)

    # Read def table body
    for row in def_rows[2:]:  # Each row of the table
        data = row.find_all('td')
        data = [element.text.strip() for element in data]
        if len(data) > 0 and data[0] != '':  # Not header
            rank, team = int(data[0]), data[1]
            if team == sb_winners[year]:
                def_ranks.append(rank)

# Plotting
source = ColumnDataSource(data=dict(off_ranks=off_ranks,
                                    def_ranks=def_ranks, infos=infos))
title = 'Super Bowl winners since 1986'
hover = HoverTool(tooltips=[('Team-year', '@infos')])
p = figure(title=title, tools=[hover])
p.circle('off_ranks', 'def_ranks', source=source, size=10)
p.xaxis.axis_label = 'Offensive DVOA rank'
p.yaxis.axis_label = 'Defensive DVOA rank'
output_file('nflgraphs_7_plot1.eps')
save(p)
p.output_backend = "svg"
export_svgs(p, filename="plot.svg")
