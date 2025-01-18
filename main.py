from Agent.FXAgent import fx_agent, Deps
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def main():
    # Sample run

    print("Hello I'm Felix, your trading assistant. How can I help you today?")
    print("Type 'exit' to quit")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            break
        dependencies = Deps(pair='BTCUSDm', timeframe=15, login=int(os.getenv("LOGIN")), password=os.getenv("PASSWORD"), server=os.getenv("SERVER")) 
        result = await fx_agent.run(user_input, deps=dependencies)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
