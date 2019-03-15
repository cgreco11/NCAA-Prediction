import sys
import pandas as pd
from collections import defaultdict
pd.set_option('display.max_columns', 500)
seasonResults = pd.read_csv("data/RankedRegularSeasonDetailedResults.csv", header = 0, low_memory = False)

ranking_df = pd.read_csv("team_ranks/MasseyOrdinals.csv", header = 0)

winningCols = [i for i in seasonResults if i.startswith("W") and not i.startswith("WTeamRank")]
losingCols = [i for i in seasonResults if i.startswith("L") and not i.startswith("LTeamRank")]

outDict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

for idx, row in seasonResults.iterrows():
    season = row["Season"]
    wteamid = row["WTeamID"]
    lteamid = row["LTeamID"]

    wteamposs = row["WFGA"] + (0.475 * row["WFTA"]) - row["WOR"] + row["WTO"]
    lteamposs = row['LFGA'] + (0.475 * row["LFTA"]) - row["LOR"] + row["LTO"]


    wteamoffrating = 100 * (row["WScore"] / wteamposs)
    lteamoffrating = 100 * (row["LScore"] / lteamposs)

    wteamdefrating = lteamoffrating
    lteamdefrating = wteamoffrating

    outDict[season][wteamid]["Poss"] += wteamposs
    outDict[season][lteamid]["Poss"] += lteamposs
    outDict[season][wteamid]["OffRating"] += wteamoffrating
    outDict[season][lteamid]["OffRating"] += lteamoffrating
    outDict[season][wteamid]["DefRating"] += wteamdefrating
    outDict[season][lteamid]['DefRating'] += lteamdefrating
    outDict[season][wteamid]["NetRating"] += (wteamoffrating - wteamdefrating)
    outDict[season][lteamid]["NetRating"] += (lteamoffrating - lteamdefrating)
    #Winning Info
    for col in winningCols:
        if col == 'WLoc':
            if row[col] == "N":
                outDict[season][wteamid]["Neutral Win"] += 1
            elif row[col] == "H":
                outDict[season][wteamid]["Home Win"] += 1
            else:
                outDict[season][wteamid]["Away Win"] += 1
        else:
            if col.startswith("W"):
                outDict[season][wteamid][col[1:]] += int(row[col])
            else:
                outDict[season][wteamid][col] += int(row[col])
    if 0 < int(row["LTeamRank"]) <= 25:
        outDict[season][wteamid]["Top 25 Wins"] += 1
    if 0 < int(row["LTeamRank"]) <= 10:
        outDict[season][wteamid]["Top 10 Wins"] += 1
    if int(row["WTeamRank"]) > int(row["LTeamRank"]):
        outDict[season][wteamid]["Upsets"] += 1
    outDict[season][wteamid]["Win Rank Cumulative"] += row["LTeamRank"]
    outDict[season][wteamid]["Wins"] += 1
    outDict[season][wteamid]["Games"] += 1

    #Losing Info
    for col in losingCols:
        if col == 'WLoc':
            if row[col] == "N":
                outDict[season][wteamid]["Neutral Loss"] += 1
            elif row[col] == "H":
                outDict[season][wteamid]["Home Loss"] += 1
            else:
                outDict[season][wteamid]["Away Loss"] += 1
        else:
            if col.startswith("L"):
                outDict[season][lteamid][col[1:]] += int(row[col])
            else:
                outDict[season][lteamid][col] += int(row[col])
    outDict[season][lteamid]["Loss Rank Cumulative"] += row["WTeamRank"]
    outDict[season][lteamid]["Games"] += 1
    outDict[season][lteamid]["Losses"] += 1

newOutDict = defaultdict(lambda: defaultdict(int))
for season, team_dict in outDict.items():
    for team, col in team_dict.items():
        games = float(col["Games"])
        avgPoss = (col["Poss"] / games)
        avgOffRating = (col["OffRating"] / games)
        avgDefRating = (col["DefRating"] / games)
        avgNetRating = (col["NetRating"] / games)
        avgTo = (col["TO"] / games)
        avgFGA3 = (col["FGA3"] / games)
        avgScore = (col["Score"] / games)
        avgBlk = (col['Blk'] / games)
        avgDr = (col["DR"] / games)
        avgFGM3 = (col["FGM3"] / games)
        avgAst = (col["Ast"] / games)
        avgFGM = (col["FGM"] / games)
        avgPf = (col["PF"] / games)
        avgFGA = (col["FGA"] / games)
        avgStl = (col["Stl"] / games)
        avgFTA = (col["FTA"] / games)
        avgFTM = (col["FTM"] / games)
        avgOR = (col["OR"] / games)
        if col["Wins"] != 0:
            avgWinRank = (col["Win Rank Cumulative"] / float(col["Wins"]))
        else:
            avgWinRank = 0
        if col["Losses"] != 0:
            avgLossRank = (col["Loss Rank Cumulative"] / float(col["Losses"]))
        else:
            avgLossRank = 0

        avgFG3P = round((avgFGM3 / avgFGA3) * 100, 2)
        avgFGP = round((avgFGM / avgFGA) * 100, 2)
        avgFTP = round((avgFTM / avgFTA) * 100, 2)
        new_index = str(season) + "_" + str(team)
        newOutDict[new_index] = {"Season" : season,
                                    "Team" : team,
                                    "Avg FG3%" : avgFG3P,
                                    "Avg FG%" : avgFGP,
                                    "Avg FT%" : avgFTP,
                                    "AvgTO" : round(avgTo,2),
                                    "avgScore" : round(avgScore,2),
                                    "avgBlk" : round(avgBlk,2),
                                    "avgDr" : round(avgDr,2),
                                    "avgAst" : round(avgAst,2),
                                    "avgPf" : round(avgPf,2),
                                    'avgStl' : round(avgStl,2),
                                    'avgOR' : round(avgOR,2),
                                    "Home Win": col["Home Win"],
                                    "Neutral Win" : col["Neutral Win"],
                                    "Away Win" : col["Away Win"],
                                    "Wins": col["Wins"],
                                    "Losses" : col["Losses"],
                                    "Upsets" : col["Upsets"],
                                    "Games" : col["Games"],
                                    "AvgWinRank" : round(avgWinRank,2),
                                    "AvgLossRank" : round(avgLossRank,2),
                                    "AvgOffRating" : round(avgOffRating,2),
                                    "AvgDefRating" : round(avgDefRating,2),
                                    "AvgNetRating" : round(avgNetRating,2),
                                    'Top 25 Wins' : col["Top 25 Wins"],
                                    "Top 10 Wins" : col["Top 10 Wins"]}

out_df = pd.DataFrame.from_dict(newOutDict, orient = 'index')
out_df.to_csv("data/SeasonAverages.csv")
