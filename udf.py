import plotly.graph_objs as go
import pandas as pd

""" General load and merge to full dataset"""
def load_df():
    df_is = pd.read_csv(r"data/df_is_full.csv")
    df_bs = pd.read_csv(r"data/df_bs_full.csv")
    df_m = pd.read_csv(r"data/df_metrics_full.csv")
    df_is["type"] = "income statement"
    df_bs["type"] = "balance sheet"
    df_m["type"] = "metrics"
    df = pd.concat([df_is, df_bs, df_m], axis=0)
    df.dropna(inplace=True)
    return df


""" INDUSTRY APP"""
""" SCATTER DF """
def df_for_industry_scatter(df, industry, x_value, y_value, range_slider_value):
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
    return dfff


""" PLOT DF """
def df_for_industry_plot(df, symbol, axis, industry):
    dff = df[df.industry == industry]
    dfff = dff[dff.line_item == axis]
    dfff = pd.pivot_table(pd.melt(dfff, id_vars=["symbol", "line_item"],
                                  value_vars=["2009", "2010", "2011", "2012",
                                              "2013", "2014", "2015", "2016",
                                              "2017", "2018"]),
                          index=["symbol", "variable"],
                          columns="line_item", values="value", fill_value=0).reset_index()
    dfff = dfff.rename(columns={"variable": "year"})
    dfff["year"] = dfff["year"].astype(int)
    dfff_line = dfff[dfff.symbol == symbol]
    dfff_mkt = dfff.groupby(["year"], as_index=False).mean()
    return dfff_line, dfff_mkt


""" CREATE PLOT """
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
            'margin': {'l': 40, 'b': 30, 'r': 10, 't': 40},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title, 'font': {'size': 14, 'color': "black"},
                'bordercolor': 'black', 'borderwidth':2,
                'borderpad': 4, 'bgcolor': 'white',
                'opacity': 0.5
            }],
            'xaxis': {'showgrid': False},
            'yaxis': {'automargin': True}}}


""" CREATE SCATTER """


def create_scatter(dfff, x_value, y_value, COMP_NAME, COLORS):
    return {
        'data': [go.Scatter(
            x=dfff[x_value],
            y=dfff[y_value],
            text=["<br>".join([dfff.iloc[i]["symbol"],
                               COMP_NAME[dfff.iloc[i]["symbol"]],
                              str(dfff.iloc[i]["year"])]
                              ) for i in range(len(dfff))],

            customdata=dfff["symbol"],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            title={'text': "Financial indicators by company", 'font': {
                'family': "Open Sans",
                'size': 18,
                'color': COLORS["darktext"]}},
            xaxis={'automargin': True,
                'title': x_value
            },
            yaxis={'automargin': True,
                'title': y_value
            },
            margin={'l': 60, 'b': 50, 't': 50, 'r': 20},
            height=420,
            hovermode='closest'
        )
    }
