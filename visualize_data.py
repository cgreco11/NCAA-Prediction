import pandas as pd
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
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
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.config.suppress_callback_exceptions = True
metadataDict = {
    'avgOR' : "Average Offensive Rebounds per Game",
    'avgStl' : "Average Steals per Game",
    'avgAst' : "Average Assists per Game",
    'Neutral Win' : "Number of Neutral Site Wins",
    'avgPf' : "Average Personal Fouls per Game",
    'Away Win' : "Number of Away Wins",
    'Avg FG%' : "Average Field Goal Percentage per Game",
    'AvgWinRank' : "Average Rank of Team's Beaten that Season",
    "avgBlk" : "Average Blocks per Game",
    'Avg FG3%' : "Average 3 Point Field Goal Percentage per Game",
    'Wins' : "Number of Wins",
    "AvgLossRank" : "Average Rank of Team's lost to that Season",
    'avgDr' : "Average Defensive Rebounds per Game",
    "Games" : "Average Number of Games Played that Season",
    "avgScore" : "Average Score per Game",
    'Upsets' : "Average Number of Upset's per Season",
    "Home Win" : "Number of Home Wins",
    "AvgTO" : "Average Number of Turnovers",
    'Avg FT%' : "Average Free Throw Percentage",
    "Losses" : "Number of Losses"
}

teamIDtoName = {v:k for k, v in teamNameMap.items()}


tab1 = html.Div(children = [
    dcc.Dropdown(
        id = 'metadata-category',
        options=[{'label': metadataDict[i], 'value': i} for i in sorted(seasonAverages.columns) if i not in  ["Season", "Team"]],
        value='Avg FG%'
    ),
    dcc.Dropdown(
        id = 'team-selection-metadata',
        placeholder = "Select a Team to view Historical Data.",
        options = [{"label" : teamIDtoName[i].title(), 'value' : i} for i in seasonAverages["Team"].unique()],
        value = '',
        multi = True
    ),
    dcc.Graph(
        id = 'line-graph')
])

#Update Line Graph on Main Page
@app.callback(
    dash.dependencies.Output('line-graph', 'figure'),
    [dash.dependencies.Input('metadata-category', 'value'),
    dash.dependencies.Input("team-selection-metadata", 'value')]
)
def update_line(category, teams):
    traces = []
    if teams:
        for team in teams:
            teamSeasonAverages = seasonAverages[seasonAverages["Team"] == team]
            x_vals = teamSeasonAverages["Season"].unique()
            y_vals = teamSeasonAverages.groupby("Season")[category].mean()
            traces.append(go.Scatter(x = x_vals, y = y_vals, name = teamIDtoName[team].title()))
    x_vals = seasonAverages["Season"].unique()
    y_vals = seasonAverages.groupby("Season")[category].mean()
    traces.append(go.Scatter(x = x_vals, y = y_vals, name = "All"))

    return {
        'data' : traces,
        'layout' : go.Layout(
            xaxis = {"title" : "Season"},
            yaxis = {"title" : category}
        )
    }

#Visualize Pre
tab2 = html.Div(children = [
    dcc.Dropdown(
        id = 'pred-team-1',
        options = [{"label" : teamIDtoName[i].title(), 'value' : i} for i in seasonAverages["Team"].unique()],
        value='',
        placeholder = 'Pick Team 1 for Prediction'
    ),
    dcc.Dropdown(
        id = 'pred-team-2',
        options = [{"label" : teamIDtoName[i].title(), 'value' : i} for i in seasonAverages["Team"].unique()],
        value = '',
        placeholder = "Pick Team 2 for Prediction"
    ),
    dcc.Dropdown(
        id = 'pred-year',
        options = [{'label' : i, "value" : i} for i in seasonAverages["Season"].unique()],
        value = '',
        placeholder = "Pick a Year for the Comparison to take place."
    ),
    html.Div(id = 'pred-text'),

])

@app.callback(
    dash.dependencies.Output('pred-text', 'children'),
    [dash.dependencies.Input('pred-team-1', 'value'),
    dash.dependencies.Input('pred-team-2', 'value'),
    dash.dependencies.Input('pred-year', 'value')]
)
def make_predictions(team1, team2, year):
    team1 = str(team1)
    team2 = str(team2)
    year = str(year)
    team1_pred, pred, team2_pred = checkMatchupByName(year, team1, team2, teamNameMap, seasonAverages, finalModel)
    return "{} has a {} % chance of beating {} in {}".format(team1_pred, pred, team2_pred, year)

app.layout = html.Div(children = [
    dcc.Tabs(
    id = "tabsID",
    children=[
        dcc.Tab(label = "Historical Comparisons",
                children = [tab1]),
        dcc.Tab(label = 'Prediction',
                children = [tab2]),
    ],
    value = "Historical Comparisons"
    )
])


if __name__ == "__main__":
    app.run_server(debug = True, host = '0.0.0.0')

#print(checkMatchupByName(2017, 'North Carolina', "Villanova", finalTeamNameMap, seasonAverages, finalModel))
