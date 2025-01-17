from Agent.FXAgent import fx_agent
import MetaTrader5 as mt5
import pandas as pd


@fx_agent.tool
def get_pair_info(pair: str="BTCUSDm", timeframe: int=15) -> dict:
    """
    Get the information of a pair
    """
    if not mt5.initialize():
        return {"error": "Failed to initialize MetaTrader5"}
    pair_info = mt5.copy_rates_from_pos(pair, timeframe, 0, 100)
    if pair_info is None:
        return {"error": "Failed to get pair information"}
    
    structured_pair_info = pd.DataFrame(pair_info)
    structured_pair_info['time'] = pd.to_datetime(structured_pair_info['time'], unit='s')
    
    return structured_pair_info
