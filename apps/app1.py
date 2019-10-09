import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import app



""" Load data """
cp = pd.read_csv(r"data/company_profiles.csv")
df_is = pd.read_csv(r"data/df_is_full.csv")
df_bs = pd.read_csv(r"data/df_bs_full.csv")
df_m = pd.read_csv(r"data/df_metrics_full.csv")
df_is["type"] = "income statement"
df_bs["type"] = "balance sheet"
df_m["type"] = "metrics"
df = pd.concat([df_is, df_bs, df_m], axis=0)

df.dropna(inplace=True)

list_of_industries = sorted(df["industry"].unique())


YEARS = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

for yr in YEARS:
    df[str(yr)] = df[str(yr)].astype(int)

COMP_NAME = {}
for i, sym in enumerate(cp["symbol"].unique()):
    COMP_NAME[sym] = cp.iloc[i]["name"]

""" STYLING """
COLORS = {
    'background': '#556B2F',
    'text': '#FFFFF0',
    'border': '#BCEE68',
    'darktext': '#050505'
}
MY_COLS = {
    "blue": "#00688B",
    "grey": "#9E9E9E"}

""" Layout """

layout = html.Div([
    html.Div([html.Div([

            html.Div([html.H6("Text title"),

                        dcc.Dropdown(
                            id="dropdown_industry",
                            options=[{'label': str(i), 'value': i} for i in list_of_industries],
                            value="Airlines"),

                        html.Div([dcc.RadioItems(
                            id='choice-items',
                            options=[{'label': k, 'value': k} for k in ["income statement",
                                                                        "balance sheet", "metrics"]],
                            value='income statement',
                            inputStyle={'display': 'inline-block'})], style={'display': 'inline-block'})
                      ], style={'width': '30%', 'margin': '5px', 'display': 'inline-block'})
]),

            html.Div([

                html.Div([html.H6("Text title"),
                    dcc.Dropdown(
                        id="crossfilter-xaxis",

                    )], style={"width": "49%", 'display': 'inline-block',
                               'color': COLORS["darktext"]}),

                html.Div([html.H6("Text title"),
                    dcc.Dropdown(
                        id='crossfilter-yaxis'

                    )], style={'width': '49%', 'float': 'right', 'display': 'inline-block',
                               'color': COLORS["darktext"]})],
                style={'borderBottom': 'thin lightgrey solid',
                       'backgroundColor': COLORS['background'],
                       'padding': '2px 5px', 'color': COLORS["text"]})
        ]),

    html.Div([
            dcc.Graph(
                id='crossfilter-scatter',
                hoverData={'points': [{'customdata': 'AMC',
                                       'text': 'AMC-AMC Entertainment Holdings Inc. Class A'}]})
        ],
            style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div(dcc.RangeSlider(
        id='crossfilter-year-range-slider',
        min=min(YEARS),
        max=max(YEARS),
        value=[min(YEARS), max(YEARS)],
        step=None,
        marks={str(year): str(year) for year in YEARS}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    Output('crossfilter-xaxis', 'options'),
    [Input('choice-items', 'value'),
     Input('dropdown_industry', 'value')])
def set_dropdown_options(selected_column, industry):
    all_options = {"income statement": [], "balance sheet": [], "metrics": []}
    for i in df[df.industry == industry]["type"].unique():
        all_options[i] = sorted(df[df.type == i]["line_item"].unique())
    return [{'label': str(i), 'value': i} for i in all_options[selected_column]]


@app.callback(
    Output('crossfilter-xaxis', 'value'),
    [Input('crossfilter-xaxis', 'options')])
def set_dropdown_value(available_options):
    if len(available_options) > 0:
        return available_options[0]["value"]
    else:
        return "Consolidated Income"


@app.callback(
    Output('crossfilter-yaxis', 'options'),
    [Input('choice-items', 'value'),
     Input('dropdown_industry', 'value')])
def set_dropdown_options(selected_column, industry):
    all_options = {"income statement": [], "balance sheet": [], "metrics": []}
    for i in df[df.industry == industry]["type"].unique():
        all_options[i] = sorted(df[df.type == i]["line_item"].unique())
    return [{'label': str(i), 'value': i} for i in all_options[selected_column]]


@app.callback(
    Output('crossfilter-yaxis', 'value'),
    [Input('crossfilter-yaxis', 'options')])
def set_dropdown_value(available_options):
    if len(available_options) > 0:
        return available_options[0]["value"]
    else:
        return "Cost of Revenue"


@app.callback(
    Output('crossfilter-scatter', 'figure'),
    [Input('crossfilter-xaxis', 'value'),
     Input('crossfilter-yaxis', 'value'),
     Input('crossfilter-year-range-slider', 'value'),
     Input('dropdown_industry', 'value')])
def update_graph(x_value, y_value, range_slider_value, industry):
    print(industry)
    dff = df[df.industry == industry]
    dfff = dff[(dff.line_item == x_value) | (dff.line_item == y_value)]
    dfff = pd.pivot_table(pd.melt(dfff, id_vars=["symbol", "line_item"],
                                  value_vars=["2009", "2010", "2011", "2012",
                                              "2013", "2014", "2015", "2016",
                                              "2017", "2018"]),
                          index=["symbol", "variable"],
                          columns="line_item", values="value", fill_value=0).reset_index()
    dfff = dfff.rename(columns={"variable": "year"})
    dfff["year"] = dfff["year"].astype(int)
    dfff = dfff[dfff.year.between(range_slider_value[0],
                range_slider_value[1], inclusive=True)]

    return {
        'data': [go.Scatter(
            x=dfff[x_value],
            y=dfff[y_value],
            text=["-".join([i, COMP_NAME [i]]) for i in dfff["symbol"]],
            customdata=dfff["symbol"],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            title={'text': "Total permit count by zip code area (all years)", 'font': {
                'family': "Open Sans",
                'size': 18,
                'color': COLORS["darktext"]}},
            xaxis={'automargin': True,
                'title': x_value
            },
            yaxis={'automargin': True,
                'title': y_value
            },
            margin={'l': 70, 'b': 30, 't': 50, 'r': 40},
            height=420,
            hovermode='closest'
        )
    }

