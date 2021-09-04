from sqlalchemy import create_engine
from django.conf import settings
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from ...models import (
    BalanceSheetStatement,
    CashFlowStatement,
    IncomeStatement,
    SAndP500,
)
import datetime


class Command(BaseCommand):
    help = "Populates the Database with the annual financial data"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # Pull data from DB for current year, previous year, 2 years ago.

        # cash_flow_statement_df = pd.read_sql("app_cashflowstatement", engine)
        # income_statement_df = pd.read_sql("app_incomestatement", engine)
        # balance_sheet_statement_df = pd.read_sql(
        #     "app_balancesheetstatement", engine)
        # share_index_df = pd.read_sql(
        #     "app_sandp500", engine)
        cash_flow_statement_df = pd.DataFrame(
            list(CashFlowStatement.objects.all().values())
        )
        income_statement_df = pd.DataFrame(list(IncomeStatement.objects.all().values()))
        balance_sheet_statement_df = pd.DataFrame(
            list(BalanceSheetStatement.objects.all().values())
        )
        share_index_df = pd.DataFrame(list(SAndP500.objects.all().values()))

        user = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        database_name = settings.DATABASES["default"]["NAME"]

        database_url = "postgresql://{user}:{password}@ec2-44-195-201-3.compute-1.amazonaws.com:5432/{database_name}".format(
            user=user,
            password=password,
            database_name=database_name,
        )

        engine = create_engine(database_url, echo=False)

        # Drop unnecessary columns
        balance_sheet_statement_df.drop(
            ["fillingDate", "acceptedDate", "period", "link", "finalLink"],
            inplace=True,
            axis=1,
        )
        income_statement_df.drop(
            ["fillingDate", "acceptedDate", "period", "link", "finalLink"],
            inplace=True,
            axis=1,
        )
        cash_flow_statement_df.drop(
            ["netIncome", "fillingDate", "acceptedDate", "period", "link", "finalLink"],
            inplace=True,
            axis=1,
        )

        # Separate each DF by year and merge financial data
        years = [0, 1, 2]
        for year in years:
            temp_balance_sheet_statement_df = balance_sheet_statement_df.loc[
                balance_sheet_statement_df["index"] == year
            ]

            temp_balance_sheet_statement_df.set_index("symbol", inplace=True)
            temp_income_statement_df = income_statement_df.loc[
                income_statement_df["index"] == year
            ]

            temp_income_statement_df.set_index("symbol", inplace=True)
            temp_cash_flow_statement_df = cash_flow_statement_df.loc[
                cash_flow_statement_df["index"] == year
            ]

            temp_cash_flow_statement_df.set_index("symbol", inplace=True)

            if year == 0:
                df_cy = pd.concat(
                    [
                        temp_balance_sheet_statement_df,
                        temp_income_statement_df,
                        temp_cash_flow_statement_df,
                    ],
                    axis=1,
                )
            elif year == 1:
                df_py = pd.concat(
                    [
                        temp_balance_sheet_statement_df,
                        temp_income_statement_df,
                        temp_cash_flow_statement_df,
                    ],
                    axis=1,
                )
            elif year == 2:
                df_py2 = pd.concat(
                    [
                        temp_balance_sheet_statement_df,
                        temp_income_statement_df,
                        temp_cash_flow_statement_df,
                    ],
                    axis=1,
                )

        f_score = {}
        # Run analysis
        for symbol in share_index_df["symbol"]:
            try:
                ROA_FS = int(
                    df_cy.loc[symbol, "netIncome"]
                    / (
                        (
                            df_cy.loc[symbol, "totalAssets"]
                            + df_py.loc[symbol, "totalAssets"]
                        )
                        / 2
                    )
                    > 0
                )
                CFO_FS = int(
                    df_cy.loc[symbol, "netCashProvidedByOperatingActivities"] > 0
                )
                ROA_D_FS = int(
                    df_cy.loc[symbol, "netIncome"]
                    / (
                        df_cy.loc[symbol, "totalAssets"]
                        + df_py.loc[symbol, "totalAssets"]
                    )
                    / 2
                    > df_py.loc[symbol, "netIncome"]
                    / (
                        df_py.loc[symbol, "totalAssets"]
                        + df_py2.loc[symbol, "totalAssets"]
                    )
                    / 2
                )
                CFO_ROA_FS = int(
                    df_cy.loc[symbol, "netCashProvidedByOperatingActivities"]
                    / df_cy.loc[symbol, "totalAssets"]
                    > df_cy.loc[symbol, "netIncome"]
                    / (
                        (
                            df_cy.loc[symbol, "totalAssets"]
                            + df_py.loc[symbol, "totalAssets"]
                        )
                        / 2
                    )
                )
                LTD_FS = int(
                    (
                        df_cy.loc[symbol, "longTermDebt"]
                        + df_cy.loc[symbol, "otherLiabilities"]
                    )
                    < (
                        df_py.loc[symbol, "longTermDebt"]
                        + df_py.loc[symbol, "otherLiabilities"]
                    )
                )
                CR_FS = int(
                    (
                        df_cy.loc[symbol, "totalCurrentAssets"]
                        / df_cy.loc[symbol, "totalCurrentLiabilities"]
                    )
                    > (
                        df_py.loc[symbol, "totalCurrentAssets"]
                        / df_py.loc[symbol, "totalCurrentLiabilities"]
                    )
                )
                DILUTION_FS = int(
                    df_cy.loc[symbol, "commonStock"] <= df_py.loc[symbol, "commonStock"]
                )
                GM_FS = int(
                    (df_cy.loc[symbol, "grossProfit"] / df_cy.loc[symbol, "revenue"])
                    > (df_py.loc[symbol, "grossProfit"] / df_py.loc[symbol, "revenue"])
                )
                ATO_FS = int(
                    df_cy.loc[symbol, "revenue"]
                    / (
                        (
                            df_cy.loc[symbol, "totalAssets"]
                            + df_py.loc[symbol, "totalAssets"]
                        )
                        / 2
                    )
                    > df_py.loc[symbol, "revenue"]
                    / (
                        (
                            df_py.loc[symbol, "totalAssets"]
                            + df_py2.loc[symbol, "totalAssets"]
                        )
                        / 2
                    )
                )
                f_score[symbol] = [
                    ROA_FS,
                    CFO_FS,
                    ROA_D_FS,
                    CFO_ROA_FS,
                    LTD_FS,
                    CR_FS,
                    DILUTION_FS,
                    GM_FS,
                    ATO_FS,
                ]
            except:
                print("Could not calculate Piotroski score for ", symbol)

        f_score_df = pd.DataFrame(
            f_score,
            index=[
                "returnOnAssets",
                "operatingCashFlow",
                "changeInReturnOnAssets",
                "accruals",
                "leverage",
                "liquidity",
                "dilution",
                "grossMargin",
                "assetTurnoverRatio",
            ],
        )
        f_score_df.loc["totalScore", :] = f_score_df.sum(axis=0)
        f_score_df_transposed = f_score_df.transpose()
        # f_score_df_transposed.reset_index(inplace=True)
        f_score_df_transposed.index.rename("symbol", inplace=True)
        # f_score_df_transposed.rename(columns={'index': 'symbol'}, inplace=True)
        f_score_df_transposed.to_sql(
            "app_piotroskiscore", con=engine, if_exists="replace"
        )
