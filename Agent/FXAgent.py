from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from Misc.Indicators import bollinger_bands, moving_average_crossover, analyse_rsi
import datetime
import pytz
import requests
import MetaTrader5 as mt5
import pandas as pd
from Misc.Trade_execute import get_tp_sl
import os

load_dotenv()

# Define dependencies for the agent
class Deps(BaseModel):
    pair: str
    timeframe: int
    login: int
    password: str
    server: str

# Initialize the GPT model with the API key
gpt_model = OpenAIModel('gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))

# Create an agent with the GPT model and dependencies
fx_agent = Agent(
    model=gpt_model,
    deps_type=Deps,
    system_prompt=("You are Felix, a Forex trader. Predict the price at the end of a given time frame. Decide whether to buy, sell, or hold based on the tools provided. If holding, explain why and suggest when to place an entry order. Keep responses concise and precise. You trade on exness so every pair is suffixed with 'm'. If it's weekend, only trade BTCUSD"),
    retries=2
)

# Agent tools

@fx_agent.tool
def login_to_account(ctx: RunContext[Deps]) -> bool:
    """
    Login to the metatrader account with the provided credentials:
    - login
    - password
    - server

    Args:
    ctx: RunContext[Deps]

    Returns:
    bool: True if login is successful, False otherwise
    """
    mt5.initialize()
    login = mt5.login(ctx.deps.login, ctx.deps.password, ctx.deps.server)
    if login:
        return True
    else:
        return False

@fx_agent.tool_plain
def use_indicators(pair: str) -> dict:
    """
    Use technical indicators to analyse the given currency pair and timeframe.
    Returns the last 5 Bollinger Bands, Moving Average Crossover, and RSI details.
    You can use this information to make trading decisions.
    """
    bollinger = bollinger_bands(pair)
    moving_average = moving_average_crossover(pair)
    rsi = analyse_rsi(pair)

    return {
        "bollinger_details": bollinger[-5:],
        "moving_average_details": moving_average,
        "rsi_details": rsi
    }

@fx_agent.tool_plain
async def execute_trade(symbol: str, action: str, lot_size: float=0.01, number_of_orders: int=1) -> str:
    """
    Execute a trade on the MetaTrader 5 platform.

    Args:
    - symbol (str): The trading symbol (e.g., "EURUSD").
    - action (str): "buy" or "sell".
    - lot_size (float): The trade volume in lots.
    - number_of_orders (int): The number of orders to execute (default: 1).

    Returns:
    - str: A message indicating the status of the trade
    """
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"{symbol} not found.")
        return f"{symbol} not found. Check if mt5 is logged in"
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select {symbol}")
            return
    
    sl_tp = get_tp_sl(symbol, action)

    # Define trade request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).ask if action == "buy" else mt5.symbol_info_tick(symbol).bid,
        "deviation": 10,
        "magic": 9997316,
        "comment": "Cool Trading Signature",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "sl": sl_tp['stop_loss'],
        "tp": sl_tp['take_profit']
    }

    for i in range(number_of_orders):
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order failed. Retcode: {result}")
            return f"Order failed. Retcode: {result}"
        else:
            print(f"Order executed. {result}")
            return f"Order executed. {result}"

@fx_agent.tool_plain
def get_news() -> list:
    """
    Get news from the news api for the specific currency: USD, EUR, GBP, JPY
    And filter the news to get only the high and medium impact news with forecast

    Returns:
    list: List
    """
    url = os.getenv('NEWS_API_URL')
    try:
        response = requests.get(url)
        news = response.json()
        countries = ['USD', 'EUR', 'GBP', 'JPY']
        if news is None:
            print('No news to analyze')
            return
        filtered_news_with_forecast = [event for event in news if event['forecast'] != '' and event['country'] in countries and event['impact'] in ['High', "Medium"]]
        return filtered_news_with_forecast
        
    except Exception as e:
        print('Error getting news:', e)
        return None

@fx_agent.tool_plain
def get_utc_time() -> datetime.datetime:
    """
    Get the current UTC time.

    Returns:
    datetime: The current UTC time.
    """
    date_time = datetime.datetime.now()
    utc_time = date_time.astimezone(pytz.utc)
    return utc_time