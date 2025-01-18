import pandas as pd
# from Agent.FXAgent import fx_agent


def bollinger_bands(rates, period=20, std_multiplier=2):
    if rates is None:
        return {"signal": "hold", "reason": "Not enough data for Bollinger Bands."}

    df = rates

    df['sma'] = df['close'].rolling(window=period).mean()
    df['std'] = df['close'].rolling(window=period).std()
    df['upper_band'] = df['sma'] + std_multiplier * df['std']
    df['lower_band'] = df['sma'] - std_multiplier * df['std']

    response = []
    

    for index, row in df.tail(2).iterrows():
        last_high = row['high']
        last_low = row['low']
        if last_high > row['upper_band']:
            response.append({"index": index, "signal": "sell", "close": last_high, "upper_band": row['upper_band']})
        elif last_low < row['lower_band']:
            response.append({"index": index, "signal": "buy", "close": last_low, "lower_band": row['lower_band']})
        else:
            response.append({"index": index, "signal": "hold", "reason": "Price within Bollinger Bands."})
    return response



def bb_reversal(last_candle, current_candle, signal) -> bool:
    if signal == "buy":
        return (
            current_candle['close'] > last_candle['close']
            and current_candle['close'] > current_candle['lower_band']
            and last_candle['close'] < last_candle['lower_band']
        )
    if signal == "sell":
        return (
            current_candle['close'] < last_candle['close']
            and current_candle['close'] < current_candle['upper_band']
            and last_candle['close'] > last_candle['upper_band']
        )
    return False



def moving_average_crossover(rates, short_period=9, long_period=21) -> dict:
    if rates is None:
        return {"signal": "hold", "reason": "Not enough data for moving averages."}

    df = rates


    # Calculate moving averages
    df['short_ma'] = df['close'].rolling(window=short_period).mean()
    df['long_ma'] = df['close'].rolling(window=long_period).mean()

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


def calculate_rsi(prices, period=14):
    delta = prices.diff()
    up = delta.clip(lower=0)  # Positive gains (up moves)
    down = -delta.clip(upper=0)  # Negative gains (down moves)

    ema_up = up.ewm(span=period, adjust=False).mean()  # Exponential Moving Average for gains
    ema_down = down.ewm(span=period, adjust=False).mean()  # EMA for losses

    rs = ema_up / ema_down  # Relative strength
    rsi = 100 - (100 / (1 + rs))  # RSI formula

    return rsi


def analyse_rsi(data) -> str:
    """
        Analyse the RSI of a given currency pair and timeframe.
        returns the last 2 RSI values and signals based on the RSI values.
    """


    # Load historical data from MetaTrader 5
    # data = mt5.copy_rates_from_pos(pair, timeframe, 0, 10)

    # Check if data is retrieved
    if data is None or len(data) == 0:
        return {"error": "No data retrieved."}

    # Create a DataFrame
    df = data

    # Convert 'time' from timestamp to a readable datetime
    # df['time'] = pd.to_datetime(df['time'], unit='s')

    # Calculate RSI
    df['RSI'] = calculate_rsi(df['close'], period=14)

    # Print the last few rows

    response = []

    for index, row in df.tail(2).iterrows():
        if row["RSI"] > 76.03:
            response.append(row["RSI"])
        elif row["RSI"] < 21.7:
            response.append(row["RSI"])
        else:
            response.append(row["RSI"])
    print(response)
    return f"High RSI Cap: 76.03, Low RSI Cap: 21.7. last 2 RSI values: {response}"
