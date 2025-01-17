# Get news from api json
import requests
import json
from dotenv import load_dotenv
from Agent.FXAgent import fx_agent
import datetime
import pytz
import os

load_dotenv()


@fx_agent.tool_plain
def get_news() -> list:
    url = os.getenv('NEWS_API_URL')
    try:
        response = requests.get(url)
        news = response.json()
        countries = ['USD', 'EUR', 'GBP', 'JPY']
        if news is None:
            print('No news to analyze')
            return
        filtered_news_with_forecast = [event for event in news if event['forecast'] != '' and event['country'] in countries and event['impact'] in ['High', "Medium"]]
        # print(filtered_news_with_forecast)
        
        # for event in filtered_news_with_forecast:
        #     print(event['title'])
        #     print(event['country'])
        #     print(event['date'])
        #     print(event['impact'])
        #     print(event['forecast'])
        #     print(event['previous'])
        
        return filtered_news_with_forecast
        
    except Exception as e:
        print('Error getting news:', e)
        return None
    


@fx_agent.tool_plain
def get_utc_time() -> datetime.datetime:
    date_time = datetime.datetime.now()
    utc_time = date_time.astimezone(pytz.utc)
    return utc_time