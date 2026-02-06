'''
Docstring for Basketball-player-analysis
This script analyzes basketball player statistics from a TSV file and computes various performance metrics.
It outputs individual player metrics to a txt file and generates top 100 lists for each metric.
Author: Mohamad El-Chal
Date: Feb 2026



'''

import os.path as os

import numpy as np

import csv



# Data Loading 


data = np.genfromtxt(
'Downloads/NBA_Player_Stats.tsv',
delimiter='\t',
names=True,
dtype=None,
encoding='utf-8'
)


#  Helper Function 


def safeDivide(numerator, denominator):
    return np.where(denominator > 0, numerator / denominator, np.nan)


# Metric Calculations


fgAccuracy = safeDivide(data['FGM'], data['FGA'])
threePtAccuracy = safeDivide(data['3PM'], data['3PA'])
ftAccuracy = safeDivide(data['FTM'], data['FTA'])
pointsPerGame = safeDivide(data['PTS'], data['GP'])


overallShootingAccuracy = safeDivide(
data['FGM'] + data['3PM'] + data['FTM'],
data['FGA'] + data['3PA'] + data['FTA']
)


blocksPerGame = safeDivide(data['BLK'], data['GP'])
stealsPerGame = safeDivide(data['STL'], data['GP'])


metrics = {
'fieldGoalAccuracy': fgAccuracy,
'threePtAccuracy': threePtAccuracy,
'ftAccuracy': ftAccuracy,
'pointsPerGame': pointsPerGame,
'overallShootingAccuracy': overallShootingAccuracy,
'blocksPerGame': blocksPerGame,
'stealsPerGame': stealsPerGame
}


#  Individual Player Metrics Output 


with open('individual_metrics.txt', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Player', 'Season', 'FG_Accuracy', '3PT_Accuracy', 'FT_Accuracy', 'Points_per_Game', 'Overall_Shooting_Accuracy', 'Blocks_per_Game', 'Steals_per_Game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(data)):
        writer.writerow({
            'Player': data['Player'][i],
            'Season': data['Season'][i],
            'FG_Accuracy': f"{fgAccuracy[i]:.3f}",
            '3PT_Accuracy': f"{threePtAccuracy[i]:.3f}",
            'FT_Accuracy': f"{ftAccuracy[i]:.3f}",
            'Points_per_Game': f"{pointsPerGame[i]:.3f}",
            'Overall_Shooting_Accuracy': f"{overallShootingAccuracy[i]:.3f}",
            'Blocks_per_Game': f"{blocksPerGame[i]:.3f}",
            'Steals_per_Game': f"{stealsPerGame[i]:.3f}"
        })

print("Individual metrics saved to individual_metrics.txt")


#  Top 100 Extraction


def top100(metricArray):
    valid = ~np.isnan(metricArray)
    sortedIdx = np.argsort(metricArray[valid])[::-1][:100]


    players = data['Player'][valid][sortedIdx]
    seasons = data['Season'][valid][sortedIdx]
    values = metricArray[valid][sortedIdx]


    return list(zip(players, seasons, values))


# Results 


for metricName, metricArray in metrics.items():
    filename = f"top100_{metricName}.txt"
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Player', 'Season', metricName])
        for player, season, value in top100(metricArray):
            writer.writerow([player, season, f"{value:.3f}"])
    print(f"Top 100 for {metricName} saved to {filename}")
