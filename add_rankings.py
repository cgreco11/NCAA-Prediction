import sys
import pandas as pd
from collections import defaultdict

season_results_df = pd.read_csv("data/RegularSeasonDetailedResults.csv", header = 0)
ranking_df = pd.read_csv("team_ranks/MasseyOrdinals.csv", header = 0)

ranking_dict = defaultdict(dict)

years = ranking_df["Season"].unique()
for year in years:
    final_ranks_df = (ranking_df[(ranking_df["Season"] == year) & (ranking_df["RankingDayNum"] == 133) & (ranking_df["SystemName"] == 'RPI')])
    for idx, row in final_ranks_df.iterrows():
        team = row["TeamID"]
        rank = row["OrdinalRank"]
        ranking_dict[year][team] = rank

def mapRanks(row):
    season = row["Season"]
    winningTeam = row["WTeamID"]
    losingTeam = row["LTeamID"]
    try:
        row["WTeamRank"] = ranking_dict[season][winningTeam]
    except:
        row["WTeamRank"] = 0
    try:
        row["LTeamRank"] = ranking_dict[season][losingTeam]
    except:
        row["LTeamRank"] = 0
    return row

season_results_df = season_results_df.apply(mapRanks, axis = 1)
season_results_df.to_csv("data/RankedRegularSeasonDetailedResults.csv")
