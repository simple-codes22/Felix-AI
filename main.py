from Agent.FXAgent import fx_agent, Deps
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    # Sample run
    dependencies = Deps(pair='BTCUSDm', timeframe=15, login=int(os.getenv("LOGIN")), password=os.getenv("PASSWORD"), server=os.getenv("SERVER")) 
    result = fx_agent.run_sync("Hey Felix, can you login to my metatrader app, and get the information of the pair BTCUSDm and place a trade if you find a trading opportunity", deps=dependencies)
    print(result)
        # result = await fx_agent.run_sync("use_indicators(pair='BTCUSDm')")
        # print(result)


main()
