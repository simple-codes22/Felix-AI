from Agent.FXAgent import fx_agent
import MetaTrader5 as mt5
import pandas as pd


@fx_agent.tool
def login_to_account(login: int, password: str, network: str) -> bool:
    """
    Login to the account
    """
    mt5.initialize()
    mt5.login(login, password, network)
    if mt5.login(login, password, network):
        return True
    else:
        return False

