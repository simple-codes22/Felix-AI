import MetaTrader5 as mt5

def get_tp_sl(symbol, trade_type, stop_loss_pct=0.0075, take_profit_pct=0.015, pip_value=None) -> dict:
    """
    Calculate stop-loss (SL) and take-profit (TP) levels for a trade.

    Args:
    - entry_price (float): The entry price of the trade.
    - trade_type (str): "long" or "short".
    - stop_loss_pct (float): Stop-loss percentage (e.g., 0.01 for 1%).
    - take_profit_pct (float): Take-profit percentage (e.g., 0.02 for 2%).
    - pip_value (float, optional): The pip value for the instrument (e.g., 0.0001 for EURUSD, 0.01 for USDJPY). If None, the calculations are based on the raw percentages.

    Returns:
    - dict: A dictionary with calculated stop_loss and take_profit levels.
    """
    if pip_value is None:
        pip_value = 0.01  # Default to raw percentage calculations if pip_value is not provided
    
    try:
        # Get symbol information from MetaTrader 5
        symbol_info = mt5.symbol_info(symbol)._asdict()
        
        # Determine entry price and calculate stop-loss and take-profit levels based on trade type
        if trade_type.lower() == "buy":
            entry_price = symbol_info['ask']
            stop_loss = entry_price - (entry_price * stop_loss_pct)
            take_profit = entry_price + (entry_price * take_profit_pct)
        elif trade_type.lower() == "sell":
            entry_price = symbol_info['bid']
            stop_loss = entry_price + (entry_price * stop_loss_pct)
            take_profit = entry_price - (entry_price * take_profit_pct)
        else:
            raise ValueError("Invalid trade type. Use 'buy' or 'sell'.")

        # Adjust levels based on pip value for instruments with different decimal places
        stop_loss = round(stop_loss / pip_value) * pip_value
        take_profit = round(take_profit / pip_value) * pip_value

        return {
            "stop_loss": round(stop_loss, 5),
            "take_profit": round(take_profit, 5)
        }
    except Exception as err:
        # Print error message if any exception occurs
        print(f"Error: {err}")
        return None
