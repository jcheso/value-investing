import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://postgres:2552JervoisRoad@localhost:5432/myproject')


def get_portfolio(strategy, value, share_index):

    # Pull data from DB for current year, previous year, 2 years ago.
    cash_flow_statement_df = pd.read_sql("app_cashflowstatement", engine)
    income_statement_df = pd.read_sql("app_incomestatement", engine)
    balance_sheet_statement_df = pd.read_sql(
        "app_balancesheetstatement", engine)
    share_index_df = pd.read_sql(
        "app_sandp500", engine)

    # Drop unnecessary columns
    balance_sheet_statement_df.drop(
        ["fillingDate", "acceptedDate", "period", "link", "finalLink"], inplace=True, axis=1)
    income_statement_df.drop(
        ["fillingDate", "acceptedDate", "period", "link", "finalLink"], inplace=True, axis=1)
    cash_flow_statement_df.drop(
        ["netIncome", "fillingDate", "acceptedDate", "period", "link", "finalLink"], inplace=True, axis=1)

    # Separate each DF by year and merge financial data
    years = [0, 1, 2]
    for year in years:
        temp_balance_sheet_statement_df = balance_sheet_statement_df.loc[balance_sheet_statement_df["index"] ==
                                                                         year]

        temp_balance_sheet_statement_df.set_index("symbol", inplace=True)
        temp_income_statement_df = income_statement_df.loc[income_statement_df["index"] ==
                                                           year]

        temp_income_statement_df.set_index("symbol", inplace=True)
        temp_cash_flow_statement_df = cash_flow_statement_df.loc[cash_flow_statement_df["index"] ==
                                                                 year]

        temp_cash_flow_statement_df.set_index("symbol", inplace=True)

        if year == 0:
            df_cy = pd.concat([temp_balance_sheet_statement_df,
                              temp_income_statement_df, temp_cash_flow_statement_df], axis=1)
        elif year == 1:
            df_py = pd.concat([temp_balance_sheet_statement_df,
                              temp_income_statement_df, temp_cash_flow_statement_df], axis=1)
        elif year == 2:
            df_py2 = pd.concat([temp_balance_sheet_statement_df,
                                temp_income_statement_df, temp_cash_flow_statement_df], axis=1)

    f_score = {}
    # Run analysis
    for symbol in share_index_df["symbol"]:
        try:
            ROA_FS = int(df_cy.loc[symbol, "netIncome"]/(
                (df_cy.loc[symbol, "totalAssets"]+df_py.loc[symbol, "totalAssets"])/2) > 0)
            CFO_FS = int(
                df_cy.loc[symbol, "netCashProvidedByOperatingActivities"] > 0)
            ROA_D_FS = int(df_cy.loc[symbol, "netIncome"]/(df_cy.loc[symbol, "totalAssets"]+df_py.loc[symbol, "totalAssets"])/2 >
                           df_py.loc[symbol, "netIncome"]/(df_py.loc[symbol, "totalAssets"]+df_py2.loc[symbol, "totalAssets"])/2)
            CFO_ROA_FS = int(df_cy.loc[symbol, "netCashProvidedByOperatingActivities"]/df_cy.loc[symbol, "totalAssets"]
                             > df_cy.loc[symbol, "netIncome"]/((df_cy.loc[symbol, "totalAssets"]+df_py.loc[symbol, "totalAssets"])/2))
            LTD_FS = int((df_cy.loc[symbol, "longTermDebt"] + df_cy.loc[symbol, "otherLiabilities"]) < (
                df_py.loc[symbol, "longTermDebt"] + df_py.loc[symbol, "otherLiabilities"]))
            CR_FS = int((df_cy.loc[symbol, "totalCurrentAssets"]/df_cy.loc[symbol, "totalCurrentLiabilities"]) > (
                df_py.loc[symbol, "totalCurrentAssets"]/df_py.loc[symbol, "totalCurrentLiabilities"]))
            DILUTION_FS = int(
                df_cy.loc[symbol, "commonStock"] <= df_py.loc[symbol, "commonStock"])
            GM_FS = int((df_cy.loc[symbol, "grossProfit"]/df_cy.loc[symbol, "revenue"]) > (
                df_py.loc[symbol, "grossProfit"]/df_py.loc[symbol, "revenue"]))
            ATO_FS = int(df_cy.loc[symbol, "revenue"]/((df_cy.loc[symbol, "totalAssets"]+df_py.loc[symbol, "totalAssets"])/2)
                         > df_py.loc[symbol, "revenue"]/((df_py.loc[symbol, "totalAssets"]+df_py2.loc[symbol, "totalAssets"])/2))
            f_score[symbol] = [ROA_FS, CFO_FS, ROA_D_FS, CFO_ROA_FS,
                               LTD_FS, CR_FS, DILUTION_FS, GM_FS, ATO_FS]
        except:
            print('Could not calculate Piotroski score for ', symbol)
    f_score_df = pd.DataFrame(f_score, index=[
                              "PosROA", "PosCFO", "ROAChange", "Accruals", "Leverage", "Liquidity", "Dilution", "GM", "ATO"])
    f_score_sorted = f_score_df.sum().sort_values(ascending=False)
    print(f_score_sorted[:10])
    return f_score_sorted


get_portfolio("Piotroski", "10,000", "S&P500")
