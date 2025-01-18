from Agent.FXAgent import fx_agent, Deps
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

async def main():
    # Sample run

    # Greet the user
    print("Hello I'm Felix, your trading agent. How can I help you today?")
    print("Type 'exit' to quit")
    
    # Main loop to interact with the user
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            break
        
        # Create dependencies object with environment variables
        dependencies = Deps(pair='BTCUSDm', timeframe=15, login=int(os.getenv("LOGIN")), password=os.getenv("PASSWORD"), server=os.getenv("SERVER")) 
        
        # Run the trading agent with user input and dependencies
        result = await fx_agent.run(user_input, deps=dependencies)
        
        # Print the result data and usage information
        print(result.data)
        # print(result.usage())

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())
