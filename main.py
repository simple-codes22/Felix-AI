from Agent.FXAgent import fx_agent
import asyncio


def main():
    # Sample run
    result = fx_agent.run_sync("Hey Felix, can you login to my metatrader app, and get the information of the pair BTCUSDm and place a trade if you find a trading opportunity")
    print(result)
        # result = await fx_agent.run_sync("use_indicators(pair='BTCUSDm')")
        # print(result)


main()
