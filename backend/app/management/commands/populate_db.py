import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from urllib.request import urlopen
import json
import os
from django.conf import settings
from sqlalchemy import create_engine


class Command(BaseCommand):
    def handle(self, *args, **options):

        user = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        database_name = settings.DATABASES["default"]["NAME"]
        # host = settings.DATABASES['default']['HOST']
        # port = settings.DATABASES['default']['PORT']

        database_url = (
            "postgresql://{user}:{password}@localhost:5432/{database_name}".format(
                user=user,
                password=password,
                database_name=database_name,
            )
        )

        engine = create_engine(database_url, echo=False)

        load_dotenv()

        # Load API Key from environment variables
        MY_API_KEY = os.environ.get("MY_API_KEY")

        # Function to perform API call and parse JSON
        def get_jsonparsed_data(url):
            response = urlopen(url)
            data = response.read().decode("utf-8")
            return json.loads(data)

        # List of Tickers to populate DB for
        dir_path = os.path.dirname(os.path.realpath(__file__))
        s_and_p_df = pd.read_csv(dir_path + "/SAndP500.csv")

        # Add list to database
        # s_and_p_df.to_sql(
        #     "app_sandp500", con=engine, if_exists='replace', index=False)

        # # API Call for Income Statements
        # income_statement_df = pd.DataFrame([])
        # for (
        #     index,
        #     symbol,
        # ) in enumerate(s_and_p_df["symbol"]):
        #     print("Fetching Income Statement for: ", symbol)
        #     print(str(index) + " of " + str(len(s_and_p_df["symbol"])))
        #     print("---------------------------------------------------------")
        #     url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=3&apikey={MY_API_KEY}"
        #     symbol_data = get_jsonparsed_data(url)
        #     symbol_data_df = pd.DataFrame(data=symbol_data)
        #     income_statement_df = income_statement_df.append(symbol_data_df)

        # income_statement_df.to_sql(
        #     "app_incomestatement", con=engine, if_exists="replace"
        # )

        # # API Call for Balance Sheet Statements
        # balance_sheet_statement_df = pd.DataFrame([])
        # for (
        #     index,
        #     symbol,
        # ) in enumerate(s_and_p_df["symbol"]):
        #     print("Fetching Balance Sheet Statement for: ", symbol)
        #     print(str(index) + " of " + str(len(s_and_p_df["symbol"])))
        #     print("---------------------------------------------------------")
        #     url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=3&apikey={MY_API_KEY}"
        #     symbol_data = get_jsonparsed_data(url)
        #     symbol_data_df = pd.DataFrame(data=symbol_data)
        #     symbol_data_df
        #     balance_sheet_statement_df = balance_sheet_statement_df.append(
        #         symbol_data_df
        #     )

        # balance_sheet_statement_df.to_sql(
        #     "app_balancesheetstatement", con=engine, if_exists="replace"
        # )

        # # API Call for Cash Flow Statements
        # cash_flow_statement_df = pd.DataFrame([])
        # for (
        #     index,
        #     symbol,
        # ) in enumerate(s_and_p_df["symbol"]):
        #     print("Fetching Cash Flow Statement for: ", symbol)
        #     print(str(index) + " of " + str(len(s_and_p_df["symbol"])))
        #     print("---------------------------------------------------------")
        #     url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?limit=3&apikey={MY_API_KEY}"
        #     symbol_data = get_jsonparsed_data(url)
        #     symbol_data_df = pd.DataFrame(data=symbol_data)
        #     cash_flow_statement_df = cash_flow_statement_df.append(symbol_data_df)

        # cash_flow_statement_df.to_sql(
        #     "app_cashflowstatement", con=engine, if_exists="replace"
        # )

        # API Call for Company Profile
        company_profile_df = pd.DataFrame([])
        for (
            index,
            symbol,
        ) in enumerate(s_and_p_df["symbol"]):
            print("Fetching Company Profile for: ", symbol)
            print(str(index) + " of " + str(len(s_and_p_df["symbol"])))
            print("---------------------------------------------------------")
            url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={MY_API_KEY}"
            symbol_data = get_jsonparsed_data(url)
            symbol_data_df = pd.DataFrame(data=symbol_data)
            company_profile_df = company_profile_df.append(symbol_data_df)

        company_profile_df.to_sql(
            "app_companyprofile", con=engine, if_exists="replace", index=False
        )
