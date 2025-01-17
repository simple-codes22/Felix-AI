import pandas as pd
from Agent.FXAgent import fx_agent

@fx_agent.tool
def use_indicators(pair: str="BTCUSDm") -> dict:
    """
    Get the indicators of a pair
    """
    return



def bollinger_bands(rates, period=20, std_multiplier=2):
    if rates is None or len(rates) < period:
        return {"signal": "hold", "reason": "Not enough data for Bollinger Bands."}

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # print(df.tail())

    df['sma'] = df['close'].rolling(window=period).mean()
    df['std'] = df['close'].rolling(window=period).std()
    df['upper_band'] = df['sma'] + std_multiplier * df['std']
    df['lower_band'] = df['sma'] - std_multiplier * df['std']

    response = []
    last_candle = df.iloc[-2]
    current_candle = df.iloc[-1]

    # if detect_candle_reversal_from_cons_trends_bollinger_bands(last_candle, current_candle, "buy"):
    #     response.append({"time": current_candle["time"], "signal": "buy", "close": current_candle['close'], "lower_band": current_candle['lower_band']})
    #     return response
    # elif detect_candle_reversal_from_cons_trends_bollinger_bands(last_candle, current_candle, "sell"):
    #     response.append({"time": current_candle["time"], "signal": "sell", "close": current_candle['close'], "upper_band": current_candle['upper_band']})
    #     return response
    # else:
    for index, row in df.tail(18).iterrows():
        last_high = row['high']
        last_low = row['low']
        if last_high > row['upper_band']:
            response.append({"time": row["time"], "signal": "sell", "close": last_high, "upper_band": row['upper_band']})
        elif last_low < row['lower_band']:
            response.append({"time": row["time"], "signal": "buy", "close": last_low, "lower_band": row['lower_band']})
        else:
            response.append({"time": row["time"], "signal": "hold", "reason": "Price within Bollinger Bands."})
    return response




def moving_average_crossover(rates, short_period=9, long_period=21):
    if rates is None or len(rates) < long_period:
        return {"signal": "hold", "reason": "Not enough data for moving averages."}

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # print(df)

    df['short_ma'] = df['close'].rolling(window=short_period).mean()
    df['long_ma'] = df['close'].rolling(window=long_period).mean()
    # Calculate moving averages

    response = {}

    if df['short_ma'].iloc[-1] > df['long_ma'].iloc[-1] and ((df['short_ma'].iloc[-2] < df['long_ma'].iloc[-2]) or (df["short_ma"].iloc[-3] < df["long_ma"].iloc[-3])):
        response = {"signal": "buy", "short_ma": df['short_ma'].iloc[-1],  "long_ma": df['long_ma'].iloc[-1]}
        return response
    elif df['short_ma'].iloc[-1] < df['long_ma'].iloc[-1] and ((df['short_ma'].iloc[-2] > df['long_ma'].iloc[-2]) or (df["short_ma"].iloc[-3] > df["long_ma"].iloc[-3])):
        response = {"signal": "sell", "short_ma": df['short_ma'].iloc[-1], "long_ma": df['long_ma'].iloc[-1]}
        return response
    else:
        response = {"signal": "hold", "reason": "No crossover detected."}
        return response




