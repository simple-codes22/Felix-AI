# Get news from api json
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_news():
    url = os.getenv('NEWS_API_URL')
    try:
        response = requests.get(url)
        news = response.json()
        return news
    except Exception as e:
        print('Error getting news:', e)
        return None


def analyze_news(news):
    countries = ['USD', 'EUR', 'GBP', 'JPY']
    if news is None:
        print('No news to analyze')
        return
    filtered_news_with_forecast = [event for event in news if event['forecast'] != '' and event['country'] in countries and event['impact'] in ['High', "Medium"]]
    print(filtered_news_with_forecast)
    
    # for event in filtered_news_with_forecast:
    #     print(event['title'])
    #     print(event['country'])
    #     print(event['date'])
    #     print(event['impact'])
    #     print(event['forecast'])
    #     print(event['previous'])
    
    return filtered_news_with_forecast