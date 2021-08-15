
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from urllib.request import urlopen
import json
import os
from app.models import IncomeStatement
from django.conf import settings
from sqlalchemy import create_engine


class Command(BaseCommand):
    help = 'Populates the Database with the annual financial data'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']
        # host = settings.DATABASES['default']['HOST']
        # port = settings.DATABASES['default']['PORT']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )

        engine = create_engine(database_url, echo=False)

        load_dotenv()

        # Load API Key from environment variables
        MY_API_KEY = os.environ.get("MY_API_KEY")

        def get_jsonparsed_data(url):
            response = urlopen(url)
            data = response.read().decode("utf-8")
            return json.loads(data)

        tickers = ["AAPL", "TSLA", "NVDA"]

        for ticker in tickers:
            url = (
                f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={MY_API_KEY}")
            stock_data = get_jsonparsed_data(url)
            print(stock_data)
            stock_data_frame = pd.DataFrame(data=stock_data)
            stock_data_frame['key'] = stock_data_frame['symbol'] + \
                ": " + stock_data_frame['date']
            print(stock_data_frame)
            stock_data_frame.to_sql(
                "app_incomestatement", con=engine, if_exists='replace')
