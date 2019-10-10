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


# Base dfff
base_industry = "Airlines"
base_x_value = "Consolidated Income"
base_y_value = "Cost of Revenue"
dff = df[df.industry == base_industry]
dfff = dff[(dff.line_item == base_x_value) | (dff.line_item == base_y_value)]
dfff = pd.pivot_table(pd.melt(dfff, id_vars=["symbol", "line_item"],
                              value_vars=["2009", "2010", "2011", "2012",
                                          "2013", "2014", "2015", "2016",
                                          "2017", "2018"]),
                      index=["symbol", "variable"],
                      columns="line_item", values="value", fill_value=0).reset_index()
dfff = dfff.rename(columns={"variable": "year"})
dfff["year"] = dfff["year"].astype(int)

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


def create_time_series(dff, dff_mkt, title: str, line_item):
    traces = []
    # company data
    traces.append(go.Scatter(
            x=dff.iloc[:, 1],
            y=dff.loc[:, line_item],
            name="company actual",
            mode='lines+markers'
        ))

    traces.append(go.Scatter(
        x=dff_mkt.iloc[:, 0],
        y=dff_mkt.loc[:, line_item],
        name="industry average",
        mode='lines+markers'
    ))

    return {"data": traces,
            'layout': {'height': 225,
            'margin': {'l': 30, 'b': 30, 'r': 10, 't': 40},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title, 'font': {'size': 14, 'color': "black"},
                'bordercolor': 'black', 'borderwidth':2,
                'borderpad':4, 'bgcolor': 'white',
                'opacity':0.5
            }],
            'xaxis': {'showgrid': False},
            'yaxis': {'automargin': True}}}




""" Layout """


layout = html.Div([
    html.Div([html.Div([

            html.Div([html.H6("Text title"),

                        dcc.Dropdown(
                            id="dropdown_industry1",
                            options=[{'label': str(i), 'value': i} for i in list_of_industries],
                            value="Airlines"),

                        html.Div([dcc.RadioItems(
                            id='choice-items1',
                            options=[{'label': k, 'value': k} for k in ["income statement",
                                                                        "balance sheet", "metrics"]],
                            value='income statement',
                            inputStyle={'display': 'inline-block'})], style={'display': 'inline-block'})
                      ], style={'width': '30%', 'margin': '5px', 'display': 'inline-block'})
]),

            html.Div([

                html.Div([html.H6("Text title"),
                    dcc.Dropdown(
                        id="crossfilter-xaxis1",

                    )], style={"width": "49%", 'display': 'inline-block',
                               'color': COLORS["darktext"]}),

                html.Div([html.H6("Text title"),
                    dcc.Dropdown(
                        id='crossfilter-yaxis1'

                    )], style={'width': '49%', 'float': 'right', 'display': 'inline-block',
                               'color': COLORS["darktext"]})],
                style={'borderBottom': 'thin lightgrey solid',
                       'backgroundColor': COLORS['background'],
                       'padding': '2px 5px', 'color': COLORS["text"]})
        ]),

    html.Div([html.Div([
            dcc.Graph(
                id='crossfilter-scatter1',
                hoverData={'points': [{'customdata': 'AMC',
                                       'text': 'AMC-AMC Entertainment Holdings Inc. Class A'}]}
            )
        ],
            ),

    html.Div(dcc.RangeSlider(
        id='crossfilter-year-range-slider1',
        min=min(YEARS),
        max=max(YEARS),
        value=[min(YEARS), max(YEARS)],
        step=None,
        marks={str(year): str(year) for year in YEARS}
    ), style={'padding': '0px 0px 50px 20px'})],
        style={'display': 'inline-block', 'width': '49%'}),

        html.Div([
                    dcc.Graph(id='top-line-plot'),
                    dcc.Graph(id='bottom-line-plot')
                ], style={'display': 'inline-block', 'width': '50%'}),


        html.Div([
                dcc.Link('Navigate back home', href='/',
                             style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                    'padding': '5px 10px 500px'}),
                html.Br(),
                dcc.Link('Navigate to Company Analysis', href='/apps/companyApp',
                         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                'padding': '5px 10px 500px', 'color': 'red'})
        ])
])


@app.callback(
    Output('crossfilter-xaxis1', 'options'),
    [Input('choice-items1', 'value'),
     Input('dropdown_industry1', 'value')])
def set_dropdown_options(selected_column, industry):
    all_options = {"income statement": [], "balance sheet": [], "metrics": []}
    for i in all_options.keys():
        all_options[i] = sorted(df[(df.type == i) & (df.industry == industry)]["line_item"].unique())
    return [{'label': str(i), 'value': i} for i in all_options[selected_column]]


@app.callback(
    Output('crossfilter-xaxis1', 'value'),
    [Input('crossfilter-xaxis1', 'options')])
def set_dropdown_value(available_options):
    if len(available_options) > 0:
        return available_options[0]["value"]
    else:
        return "Consolidated Income"


@app.callback(
    Output('crossfilter-yaxis1', 'options'),
    [Input('choice-items1', 'value'),
     Input('dropdown_industry1', 'value')])
def set_dropdown_options(selected_column, industry):
    all_options = {"income statement": [], "balance sheet": [], "metrics": []}
    for i in all_options.keys():
        all_options[i] = sorted(df[(df.type == i) & (df.industry == industry)]["line_item"].unique())
    return [{'label': str(i), 'value': i} for i in all_options[selected_column]]


@app.callback(
    Output('crossfilter-yaxis1', 'value'),
    [Input('crossfilter-yaxis1', 'options')])
def set_dropdown_value(available_options):
    if len(available_options) > 0:
        return available_options[1]["value"]
    else:
        return "Cost of Revenue"


@app.callback(
    Output('crossfilter-scatter1', 'figure'),
    [Input('crossfilter-xaxis1', 'value'),
     Input('crossfilter-yaxis1', 'value'),
     Input('crossfilter-year-range-slider1', 'value'),
     Input('dropdown_industry1', 'value')])
def update_graph(x_value, y_value, range_slider_value, industry):
    global dfff
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
    dfff_yrsl = dfff[dfff.year.between(range_slider_value[0],
                range_slider_value[1], inclusive=True)]

    return {
        'data': [go.Scatter(
            x=dfff_yrsl[x_value],
            y=dfff_yrsl[y_value],
            text=["-".join([i, COMP_NAME [i]]) for i in dfff["symbol"]],
            customdata=dfff_yrsl["symbol"],
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
            margin={'l': 70, 'b': 50, 't': 50, 'r': 40},
            height=420,
            hovermode='closest'
        )
    }


@app.callback(
    Output('top-line-plot', 'figure'),
    [Input('crossfilter-scatter1', 'hoverData'),
     Input('crossfilter-xaxis1', 'value')])
def update_top_line_plot(hoverData, xaxis):
    global dfff
    symbol = hoverData["points"][0]["customdata"]
    dfff_line = dfff[dfff.symbol == symbol]
    dfff_mkt = dfff.groupby(["year"], as_index=False).mean()
    title = f"Line Item: {xaxis} and Company: {COMP_NAME[symbol]}"
    return create_time_series(dfff_line, dfff_mkt, title, xaxis)


@app.callback(
    Output('bottom-line-plot', 'figure'),
    [Input('crossfilter-scatter1', 'hoverData'),
     Input('crossfilter-yaxis1', 'value')])
def update_top_line_plot(hoverData, yaxis):
    global dfff
    symbol = hoverData["points"][0]["customdata"]
    dfff_line = dfff[dfff.symbol == symbol]
    dfff_mkt = dfff.groupby(["year"], as_index=False).mean()
    title = f"Line Item: {yaxis} and Company: {COMP_NAME[symbol]}"
    return create_time_series(dfff_line, dfff_mkt, title, yaxis)




