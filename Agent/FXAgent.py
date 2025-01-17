from pydantic_ai import Agent, RunContext
from pydantic import BaseModel




class TradeResult(BaseModel):
    signal: str
    reason: str
    tp: float | None
    sl: float | None
    entry: float | None

fx_agent = Agent(
    model="openai:gpt-3.5-turbo",
    system_prompt=(
        "Your name is Felix. You are a foreign exchange trader. You are given a currency pair and a time frame."
        "You need to predict the price of the currency pair at the end of the time frame."
        "Strictly use the information provided from the tools"
        "You decide whether to buy or sell or hold a bit on the currency pair. Then predict when the price will reach the target price. Stop loss and take profit are optional."
        "If your decision is to hold, provide a reason for your decision. Then predict when the price should be okay for a buy or sell one should place an entry order"
        "Currency pairs: BTCUSD"
        "You make use of the tools provided to make your decision and provide a reason for your decision."
        "Your responses are not much, just straight to the point."
        ),
        # deps_type=Deps
        retries=2
)



# fx_agent.run_sync("")