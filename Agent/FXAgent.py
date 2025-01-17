from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
import os

load_dotenv()


class TradeResult(BaseModel):
    signal: str
    reason: str
    tp: float | None
    sl: float | None
    entry: float | None

class Deps(BaseModel):
    pair: str
    timeframe: int
    login: int
    password: str
    server: str
    # utc_time: str


gpt_model = OpenAIModel('gpt-3.5-turbo', api_key=os.getenv('OPENAI_API_KEY'))

fx_agent = Agent(
    model=gpt_model,
    deps_type=Deps,
    system_prompt=(
        "Your name is Felix. You are a Forex trader. You are given a currency pair and a time frame."
        "You need to predict the price of the currency pair at the end of the time frame."
        "Strictly use the information provided from tools"
        "You decide whether to buy or sell or hold a bit on the currency pair."
        "If your decision is to hold, provide a reason for your decision. Then predict when the price should be okay for a buy or sell one should place an entry order"
        "Currency pairs: BTCUSD"
        "You make use of the tools provided to make your decision and provide a reason for your decision."
        "Your responses are not much, just straight to the point."
        ),
        # deps_type=Deps
        retries=2
)
