import pandas as pd
import numpy as np


def calc_sma(df, period):
    return df['Close'].rolling(window=period).mean()


def calc_ema(df, period):
    return df['Close'].ewm(span=period, adjust=False).mean()


def calc_macd(df):
    ema_12 = calc_ema(df, 12)
    ema_26 = calc_ema(df, 26)
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    return macd, signal, hist


def calc_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calc_bollinger_bands(df, period=20, num_std=2):
    sma = calc_sma(df, period)
    std = df['Close'].rolling(window=period).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band


def calc_stochastic_oscillator(df, period=14):
    low_min = df['Low'].rolling(window=period).min()
    high_max = df['High'].rolling(window=period).max()
    k = 100 * (df['Close'] - low_min) / (high_max - low_min)
    d = k.rolling(window=3).mean()
    return k, d


def calc_adx(df, period=14):
    plus_dm = df['High'].diff()
    minus_dm = df['Low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    tr = np.maximum(df['High'] - df['Low'],
                    np.maximum(abs(df['High'] - df['Close'].shift()), abs(df['Low'] - df['Close'].shift())))
    atr = tr.rolling(window=period).mean()
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (abs(minus_dm).rolling(window=period).mean() / atr)
    dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))
    adx = dx.rolling(window=period).mean()
    return adx


def calc_stddev(df, period=14):
    return df['Close'].rolling(window=period).std()


def calc_ichimoku(df):
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    conversion_line = (high_9 + low_9) / 2

    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    base_line = (high_26 + low_26) / 2

    span_a = ((conversion_line + base_line) / 2).shift(26)
    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    span_b = ((high_52 + low_52) / 2).shift(26)

    return conversion_line, base_line, span_a, span_b



def calc_trading_indicators(df):
    df['SMA_50'] = calc_sma(df, 50)
    df['SMA_200'] = calc_sma(df, 200)
    df['EMA_50'] = calc_ema(df, 50)
    df['EMA_200'] = calc_ema(df, 200)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calc_macd(df)
    df['RSI'] = calc_rsi(df)
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = calc_bollinger_bands(df)
    df['Slowk'], df['Slowd'] = calc_stochastic_oscillator(df)
    df['ADX'] = calc_adx(df)
    df['STDDEV'] = calc_stddev(df)
    df['Ichimoku_Conversion'], df['Ichimoku_Base'], df['Ichimoku_SpanA'], df['Ichimoku_SpanB'] = calc_ichimoku(df)

    return df
