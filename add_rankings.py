import sys, collections
import pandas as pd


ranking_df = pd.read_csv("team_ranks/MasseyOrdinals.csv", header = 0)
teams_df = pd.read_csv("data/Teams.csv", header = 0)
season_results_df = pd.read_csv("data/RegularSeasonDetailedResults.csv", header = 0)

ranking_dict = collections.defaultdict(lambda: collections.defaultdict( lambda: collections.defaultdict(dict)))

for idx, row in ranking_df.iterrows():
    team = row["TeamID"]
    season = row["Season"]
    day = row["RankingDayNum"]
    rank = row["OrdinalRank"]
    ranking_dict[team][season][day] = rank

def addTeamRank(row):
    wteam = row["WTeamID"]
    lteam = row["LTeamID"]
    day = row["DayNum"]
    season = row["Season"]

    days = ranking_dict[wteam][season].keys()
    last_ranking_day = [i for i in days if i <= day]
    print(day, last_ranking_day) #Rankings don't come out til Day 30 or so
    row["WTeamRank"] = ranking_dict[wteam][season][last_ranking_day]

    last_ranking_day = max([i for i in days if i <= day])
    row["LTeamRank"] = ranking_dict[lteam][season][last_ranking_day]

season_results_df = season_results_df.apply(addTeamRank, axis = 1)
season_results_df.to_csv("data/RankedRegularSeasonDetailedResults.csv")
