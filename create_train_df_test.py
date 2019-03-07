import sys
import pandas as pd
from collections import defaultdict
pd.set_option('display.max_columns', 500)


seasonAverages = pd.read_csv("data/SeasonAverages.csv", header = 0, index_col = 0)

results_df = pd.read_csv("data/RegularSeasonCompactResults.csv", header = 0)
results_df = results_df[results_df["Season"] >= 2003][["WTeamID", "LTeamID", "Season"]]

realOutDict = defaultdict(dict)
for idx, row in results_df.iterrows():
    season = row["Season"]
    team1 = min(row["WTeamID"], row["LTeamID"])
    team2 = max(row["WTeamID"], row["LTeamID"])
    team1_idx = str(row["Season"]) + "_" + str(team1)
    team2_idx = str(row["Season"]) + "_" + str(team2)
    team1_row = seasonAverages.loc[team1_idx]
    team2_row = seasonAverages.loc[team2_idx]

    team1_dict = team1_row.to_dict()
    team2_dict = team2_row.to_dict()

    if row["WTeamID"] == team1:
        target = 1
    else:
        target = 0

    deltaOR = team1_dict['avgOR'] - team2_dict['avgOR']
    deltaStl = team1_dict['avgStl'] - team2_dict['avgStl']
    deltaFTP = team1_dict['Avg FT%'] - team2_dict['Avg FT%']
    deltaAst = team1_dict['avgAst'] - team2_dict['avgAst']
    deltaNeutWin = team1_dict['Neutral Win'] - team2_dict['Neutral Win']
    deltaPF = team1_dict['avgPf'] - team2_dict["avgPf"]
    deltaAwayWin = team1_dict['Away Win'] - team2_dict['Away Win']
    deltaFGP = team1_dict['Avg FG%'] - team2_dict["Avg FG%"]
    deltaWinRank = team1_dict["AvgWinRank"] - team2_dict['AvgWinRank']
    deltaBlk = team1_dict['avgBlk'] - team2_dict['avgBlk']
    deltaFG3 = team1_dict['Avg FG3%'] - team2_dict["Avg FG3%"]
    deltaWins = team1_dict['Wins'] - team2_dict['Losses']
    deltaLossRank = team1_dict["AvgLossRank"] - team2_dict["AvgLossRank"]
    deltaDR = team1_dict['avgDr'] - team2_dict['avgDr']
    deltaGames = team1_dict['Games'] - team2_dict['Games']
    deltaAvgScore = team1_dict['avgScore'] - team2_dict["avgScore"]
    deltaUpsets = team1_dict["Upsets"] - team2_dict["Upsets"]
    deltaHomeWins = team1_dict["Home Win"] - team2_dict["Home Win"]
    deltaTo = team1_dict["AvgTO"] - team2_dict["AvgTO"]

    out_dict = {
        'target' : round(target,2),
        'deltaOR' : round(deltaOR,2),
        'deltaStl' : round(deltaStl,2),
        'deltaFTP' : round(deltaFTP,2),
        'deltaAst' : round(deltaAst,2),
        'deltaNeutWin' : round(deltaNeutWin,2),
        'deltaPF' : round(deltaPF,2),
        'deltaAwayWin' : round(deltaAwayWin,2),
        'deltaFGP' : round(deltaFGP,2),
        'deltaWinRank' : round(deltaWinRank,2),
        'deltaBlk' : round(deltaBlk,2),
        'deltaFG3' : round(deltaFG3,2),
        'deltaWins' : round(deltaWins,2),
        'deltaLossRank' : round(deltaLossRank,2),
        'deltaDR' : round(deltaDR,2),
        'deltaGames' : round(deltaGames,2),
        'deltaAvgScore' : round(deltaAvgScore,2),
        'deltaUpsets' : round(deltaUpsets,2),
        'deltaHomeWins' : round(deltaHomeWins,2),
        'deltaTo' : round(deltaTo,2)
    }

    key = str(season) + "_" + str(team1) + "_" + str(team2)
    realOutDict[key] = out_dict


outDf = pd.DataFrame.from_dict(realOutDict, orient = 'index')
outDf.to_csv("RegularSeasonResults.csv")
