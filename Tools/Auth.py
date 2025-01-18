from Agent.FXAgent import fx_agent, Deps
from pydantic_ai import RunContext
import MetaTrader5 as mt5
# import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


@fx_agent.tool
def login_to_account(ctx: RunContext[Deps]) -> bool:
    """
    Login to the metatrader account with the provided credentials:
    - login
    - password
    - server

    Args:
    ctx: RunContext[Deps]

    Returns:
    bool: True if login is successful, False otherwise

    """
    mt5.initialize()
    login = mt5.login(ctx.deps.login, ctx.deps.password, ctx.deps.server)
    if login:
        return True
    else:
        return False