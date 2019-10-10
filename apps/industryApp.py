import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# My files
from app import app
import udf


""" Load data """
cp = pd.read_csv(r"data/company_profiles.csv")
df = udf.load_df()
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
    ), style={'padding': '0px 5px 50px 20px', 'width': '90%'})],
        style={'display': 'inline-block', 'width': '50%'}),

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
    dfff = udf.df_for_industry_scatter(df, industry, x_value, y_value, range_slider_value)
    return udf.create_scatter(dfff, x_value, y_value, COMP_NAME, COLORS)


@app.callback(
    Output('top-line-plot', 'figure'),
    [Input('crossfilter-scatter1', 'hoverData'),
     Input('crossfilter-xaxis1', 'value'),
     Input('dropdown_industry1', 'value')])
def update_top_line_plot(hoverData, xaxis, industry):
    symbol = hoverData["points"][0]["customdata"]
    dfff_line, dfff_mkt = udf.df_for_industry_plot(df, symbol, xaxis, industry)
    title = f"Line Item: {xaxis} and Company: {COMP_NAME[symbol]}"
    return udf.create_time_series(dfff_line, dfff_mkt, title, xaxis)


@app.callback(
    Output('bottom-line-plot', 'figure'),
    [Input('crossfilter-scatter1', 'hoverData'),
     Input('crossfilter-yaxis1', 'value'),
     Input('dropdown_industry1', 'value')])
def update_top_line_plot(hoverData, yaxis, industry):
    symbol = hoverData["points"][0]["customdata"]
    dfff_line, dfff_mkt = udf.df_for_industry_plot(df, symbol, yaxis, industry)
    title = f"Line Item: {yaxis} and Company: {COMP_NAME[symbol]}"
    return udf.create_time_series(dfff_line, dfff_mkt, title, yaxis)






