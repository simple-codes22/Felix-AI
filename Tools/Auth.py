from Agent.FXAgent import fx_agent
import MetaTrader5 as mt5
# import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


@fx_agent.tool_plain
def login_to_account() -> bool:
    """
    Login to the account
    """
    mt5.initialize()
    login = mt5.login(int(os.getenv("LOGIN")), os.getenv("PASSWORD"), os.getenv("SERVER"))
    if login:
        return True
    else:
        return False