import pandas as pd


""" get company profiles """
""" this was previously scraped by myself """

# Drop na for clean dataset
comp_prof = pd.read_csv(r"data/company_profiles.csv")
comp_prof.dropna(inplace=True)

list_of_industry = comp_prof["industry"].unique()

df = pd.DataFrame()
industries_processed = []
for industry in list_of_industry:
    list_of_tickers = comp_prof[comp_prof.industry == industry]["symbol"].unique()
    for ticker in list_of_tickers:
        url = r"https://financialmodelingprep.com/api/v3/financials/income-statement/%s" % ticker
        income_statement = pd.read_json(url)
        if len(income_statement) != 0:
            income_statement.drop("symbol", axis=1, inplace=True)
            data = []
            for i in range(income_statement.shape[0]):
                data.append(income_statement.iloc[i][0])
            df_is = pd.DataFrame(data).T
            df_is.columns = [i[:4] for i in pd.DataFrame(data).T.loc["date"]]
            df_is.drop("date", axis=0, inplace=True)
            df_is["symbol"] = ticker
            df_is["industry"] = industry
            df_is["type"] = "income statement"
            df_is = df_is.loc[:, ~df_is.columns.duplicated()]
            df = pd.concat([df, df_is], axis=0, sort=True)


    # Print statement for check
    industries_processed.append(industry)
    if len(industries_processed)%10 == 0:
        print("Processed so far ", len(industries_processed))


df.fillna(0, inplace=True)
df = df.reset_index().rename(columns={"index": "line_item"})
df = df[['line_item', '2009', '2010', '2011', '2012',
       '2013', '2014', '2015', '2016', '2017', '2018', 'industry',
       'symbol', 'type']]
df.to_csv("data/df_is_full.csv")
