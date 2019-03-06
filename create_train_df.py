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

    team1_list = team1_row.tolist()
    team2_list = team2_row.tolist()
    outVals = team1_list + team2_list


    team1_row.columns = ["Team1_" + str(col) for col in seasonAverages]
    team2_row.columns = ["Team2_" + str(col) for col in seasonAverages]

    outCols = team1_row.columns + team2_row.columns + ["Target"]

    if row["WTeamID"] == team1:
        outVals.append(1)
    else:
        outVals.append(0)

    out_dict = dict(zip(outCols, outVals))

    key = str(season) + "_" + str(team1) + "_" + str(team2)
    realOutDict[key] = out_dict


outDf = pd.DataFrame.from_dict(realOutDict, orient = 'index')
outDf.to_csv("RegularSeasonResults.csv")
