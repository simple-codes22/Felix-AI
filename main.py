from Agent.FXAgent import fx_agent
import asyncio


async def main():
    async with fx_agent:
        # Sample run
        result = await fx_agent.run("Hey Felix, can you login to my metatrader app, and get the information of the pair BTCUSDm and place a trade if you find a trading opportunity")
        print(result)
        # result = await fx_agent.run_sync("use_indicators(pair='BTCUSDm')")
        # print(result)



if __name__ == "__main__":
    asyncio.run(main())
    # fx_agent.run_sync("get_pair_info(pair='BTCUSDm', timeframe=15)")
# fx_agent.run_sync("")