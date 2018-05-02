#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 10:22:36 2018

@author: harish

This script reads the kicking and punting file from
PFR and plots how the punting and kicking metrics have evolved
over time
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

start_year = 1970  # Since AFL-NFL merger
data_file_name = "kick_punt.csv"  # Input file

df = pd.read_csv(data_file_name)

df = df.loc[df['Year'] >= start_year]  # Extract relevant rows

DPI = 1000

f, axes = plt.subplots(1, 3)

corr1 = round(df['Year'].corr(df['Pnt']), 2)
sns.regplot(x="Year", y="Pnt", data=df, ci=None, ax=axes[0])
axes[0].annotate('Corr coeff: ' + str(corr1),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[0].set_ylabel('Times punted')

corr2 = round(df['Year'].corr(df['Yds']), 2)
sns.regplot(x="Year", y="Yds", data=df, ci=None, ax=axes[1])
axes[1].annotate('Corr coeff: ' + str(corr2),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[1].set_ylabel('Total punt yardage')

corr3 = round(df['Year'].corr(df['Y/P']), 2)
sns.regplot(x="Year", y="Y/P", data=df, ci=None, ax=axes[2])
axes[2].annotate('Corr coeff: ' + str(corr3),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[2].set_ylabel('Yards per punt')
axes[2].set_ylim([30, 50])

plt.tight_layout()
f.savefig("Punting_stats.eps", format="eps", dpi=DPI)
