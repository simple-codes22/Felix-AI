from pydantic_ai import Agent, RunContext



fx_agent = Agent(
    model="openai:gpt-3.5-turbo",
    system_prompt=(
        "You are a foreign exchange trader. You are given a currency pair and a time frame."
        "You need to predict the price of the currency pair at the end of the time frame."
        "Strictly use the information provided from the tools"
        "You decide whether to buy or sell the currency pair."
        "Currency pairs: BTCUSD"
        "You make use of the tools provided to make your decision and provide a reason for your decision."
        ),
        # deps_type=Deps
        retries=2
)
