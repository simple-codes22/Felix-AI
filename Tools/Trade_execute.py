from Agent.FXAgent import fx_agent, RunContext
import MetaTrader5 as mt5



@fx_agent.tool_plain
async def execute_trade(symbol: str, action, lot_size, number_of_orders: int=1):
    """
    Execute a trade
    """
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"{symbol} not found.")
        return
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select {symbol}")
            return
    
    sl_tp = get_tp_sl(symbol, action)

    # Define trade request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).ask if action == "buy" else mt5.symbol_info_tick(symbol).bid,
        "deviation": 10,
        "magic": 9997316,
        "comment": "Cool Trading Signature",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "sl": sl_tp['stop_loss'],
        "tp": sl_tp['take_profit']
    }

    for i in range(number_of_orders):
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order failed. Retcode: {result}")
        else:
            print(f"Order executed. {result}")




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
        symbol_info = mt5.symbol_info(symbol)._asdict()
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
        print(f"Error: {err}")
        return None
