#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 16:59:11 2018

@author: harish

This script reads the offense file from
PFR and plots how the points, rushing and passing yards
have changed over the years
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

home = str(Path.home())
start_year = 1970  # Since AFL-NFL merger
data_file_name = home+"/Documents/nfl_stats/teamoffense_leagueaverage.csv"

df = pd.read_csv(data_file_name)

df = df.loc[df['Year'] >= 1970]  # Extract relevant rows

DPI = 1000

f, axes = plt.subplots(1, 1)
corr1 = round(df['Year'].corr(df['Points scored']), 2)
sns.regplot(x="Year", y="Points scored", data=df, ci=None, ax=axes)
axes.annotate('Corr coeff: ' + str(corr1),
              xy=(0.1, 0.9), xycoords='axes fraction')
axes.set_ylim([15, 25])
f.savefig("Offense_Stats-1.png", format="png", dpi=DPI)

f, axes = plt.subplots(1, 3)

corr2 = round(df['Year'].corr(df['Total Yds']), 2)
sns.regplot(x="Year", y="Total Yds", data=df, ci=None, ax=axes[0])
axes[0].annotate('Corr coeff: ' + str(corr2),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[0].set_ylim([100, 380])

corr3 = round(df['Year'].corr(df['Pass Yds']), 2)
sns.regplot(x="Year", y="Pass Yds", data=df, ci=None, ax=axes[1])
axes[1].annotate('Corr coeff: ' + str(corr3),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[1].set_ylim([100, 380])

corr4 = round(df['Year'].corr(df['Rush Yds']), 2)
sns.regplot(x="Year", y="Rush Yds", data=df, ci=None, ax=axes[2])
axes[2].annotate('Corr coeff: ' + str(corr4),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[2].set_ylim([100, 380])

plt.tight_layout()
f.savefig("Offense_Stats-2.png", format="png", dpi=DPI)

f, axes = plt.subplots(1, 3)

corr5 = round(df['Year'].corr(df['Y/P']), 2)
sns.regplot(x="Year", y="Y/P", data=df, ci=None, ax=axes[0])
axes[0].annotate('Corr coeff: ' + str(corr5),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[0].set_ylabel('Yards per play')
axes[0].set_ylim([3, 7])

corr6 = round(df['Year'].corr(df['PassY/A']), 2)
sns.regplot(x="Year", y="PassY/A", data=df, ci=None, ax=axes[1])
axes[1].annotate('Corr coeff: ' + str(corr6),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[1].set_ylabel('Passing yards per attempt')
axes[1].set_ylim([3, 7])

corr7 = round(df['Year'].corr(df['RushY/A']), 2)
sns.regplot(x="Year", y="RushY/A", data=df, ci=None, ax=axes[2])
axes[2].annotate('Corr coeff: ' + str(corr7),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[2].set_ylabel('Rushing yards per attempt')
axes[2].set_ylim([3, 7])

plt.tight_layout()
f.savefig("Offense_Stats-3.png", format="png", dpi=DPI)

f, axes = plt.subplots(1, 3)

corr8 = round(df['Year'].corr(df['Num Plays']), 2)
sns.regplot(x="Year", y="Num Plays", data=df, ci=None, ax=axes[0])
axes[0].annotate('Corr coeff: ' + str(corr8),
                 xy=(0.1, 0.5), xycoords='axes fraction')
axes[0].set_ylabel('Num plays')
axes[0].set_ylim([20, 70])

corr9 = round(df['Year'].corr(df['PassAtt']), 2)
sns.regplot(x="Year", y="PassAtt", data=df, ci=None, ax=axes[1])
axes[1].annotate('Corr coeff: ' + str(corr9),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[1].set_ylabel('Passing attempts')
axes[1].set_ylim([20, 70])

corr10 = round(df['Year'].corr(df['RushAtt']), 2)
sns.regplot(x="Year", y="RushAtt", data=df, ci=None, ax=axes[2])
axes[2].annotate('Corr coeff: ' + str(corr10),
                 xy=(0.1, 0.9), xycoords='axes fraction')
axes[2].set_ylabel('Rushing attempts')
axes[2].set_ylim([20, 70])

plt.tight_layout()
f.savefig("Offense_Stats-4.png", format="png", dpi=DPI)
