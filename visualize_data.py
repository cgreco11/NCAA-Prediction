import pandas as pd
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
#-------------------------------------------#
# Loading Necessary Information
def load_model(model = 'finalized_model.sav'):
    model = pickle.load(open(model, 'rb'))
    return model

def load_data(data = 'data/SeasonAverages.csv', encoding = 'utf-8', index_col = None):
    df = pd.read_csv(data, header = 0, encoding = encoding, index_col = index_col)
    return df

finalModel = load_model()
seasonAverages = load_data(index_col = 0)

def compareMatchups(season_team1_team2, regSeasonDf):
    season, team1, team2 = season_team1_team2.split("_")
    team1_idx = str(season) + "_" + str(team1)
    team2_idx = str(season) + "_" + str(team2)
    team1_dict = regSeasonDf.loc[team1_idx].to_dict()
    team2_dict = regSeasonDf.loc[team2_idx].to_dict()

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
        #'deltaWins' : round(deltaWins,2),
        'deltaLossRank' : round(deltaLossRank,2),
        'deltaDR' : round(deltaDR,2),
        'deltaGames' : round(deltaGames,2),
        'deltaAvgScore' : round(deltaAvgScore,2),
        'deltaUpsets' : round(deltaUpsets,2),
        'deltaHomeWins' : round(deltaHomeWins,2),
        'deltaTo' : round(deltaTo,2)
    }
    return out_dict

teamNames = load_data("data/Teams.csv", encoding = 'latin-1ß')
teamNameMap = dict(zip(teamNames["TeamName"].str.lower(), teamNames["TeamID"]))

altTeamNames = load_data("data/TeamSpellings.csv", encoding = 'latin-1')
altTeamNameMap = dict(zip(altTeamNames['TeamNameSpelling'].str.lower(), teamNames["TeamID"]))

finalTeamNameMap = {**teamNameMap, **altTeamNameMap}

def checkMatchupByName(season, team1, team2, teamNameMap, seasonAverages, model):
    team1_id = teamNameMap[team1.lower()]
    team2_id = teamNameMap[team2.lower()]
    print(team1_id, team2_id)
    search_term = str(season) + "_" + str(team1_id) + "_" + str(team2_id)

    outResultDict = {search_term: compareMatchups(search_term, seasonAverages)}
    #testMatrix = xgb.DMatrix(pd.DataFrame.from_dict(outResultDict, orient = 'index').values)
    #pred = model.predict(testMatrix)
    testDf = pd.DataFrame.from_dict(outResultDict, orient = 'index')
    pred = model.predict_proba(testDf)[:,1] # pred[:,0] is the reverse probability
    return team1, round(pred[0] * 100,2), team2

#--------------------------------------------#
#Layout Dash App
app = dash.Dash(__name__)

app.layout = html.Div(children = [
    html.H1(children = "Average Field Goal Percentage 2003-2017"),
    dcc.Dropdown(
        id = 'metadata-category',
        options=[{'label': i, 'value': i} for i in seasonAverages.columns if i != "Season"],
                value='Avg FG%'
    ),
    dcc.Graph(
        id = 'bar-chart',
        figure = {
            'data' : [
            {'x' : seasonAverages["Season"].unique(), 'y' : seasonAverages.groupby("Season")["Avg FG%"].mean()}
            ]
        }
    )
])



if __name__ == "__main__":
    app.run_server(debug = True)

#print(checkMatchupByName(2017, 'North Carolina', "Villanova", finalTeamNameMap, seasonAverages, finalModel))
