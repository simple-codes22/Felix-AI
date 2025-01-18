from Agent.FXAgent import fx_agent, Deps
from pydantic_ai import RunContext
import MetaTrader5 as mt5
import pandas as pd


@fx_agent.tool
def get_pair_info(ctx: RunContext[Deps]) -> pd.DataFrame:
    """
    Get the information of a pair from MetaTrader5 app
    example pair is "BTCUSDm" on the 15 minutes timeframe

    Args:
    pair: str
    timeframe: int

    Returns:
    pd.DataFrame: The information of the pair
    """
    if not mt5.initialize():
        return {"error": "Failed to initialize MetaTrader5"}
    pair_info = mt5.copy_rates_from_pos(ctx.deps.pair, ctx.deps.timeframe, 0, 100)
    if pair_info is None:
        return {"error": "Failed to get pair information"}
    
    structured_pair_info = pd.DataFrame(pair_info)
    structured_pair_info['time'] = pd.to_datetime(structured_pair_info['time'], unit='s')
    
    return structured_pair_info