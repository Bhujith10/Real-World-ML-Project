import numpy as np
import pandas as pd
from loguru import logger
from quixstreams import State
from ta import momentum, trend, volume


def compute_technical_indicators(
    candle: dict,
    state: dict,
):
    """
    Computes technical indicators from the candles in the state dictionary.

    Args:
        candles (list): List of candles in the state dictionary

    Returns:
        dict: Dictionary with the computed technical indicators
    """

    # Extract the candles from the state dictionary
    candles = state.get("candles", default=[])

    logger.debug(f"Number of candles in state: {len(candles)}")

    # Convert candles to pandas DataFrame for use with ta library
    df = pd.DataFrame(candles) if candles else pd.DataFrame()

    indicators = {}

    if not df.empty and len(df) > 0:
        # Simple Moving Average (SMA) for different periods
        indicators["sma_7"] = trend.sma_indicator(
            df["close"], window=7, fillna=True
        ).iloc[-1]
        indicators["sma_14"] = trend.sma_indicator(
            df["close"], window=14, fillna=True
        ).iloc[-1]
        indicators["sma_21"] = trend.sma_indicator(
            df["close"], window=21, fillna=True
        ).iloc[-1]
        indicators["sma_60"] = trend.sma_indicator(
            df["close"], window=60, fillna=True
        ).iloc[-1]

        # Exponential Moving Average (EMA) for different periods
        indicators["ema_7"] = trend.ema_indicator(
            df["close"], window=7, fillna=True
        ).iloc[-1]
        indicators["ema_14"] = trend.ema_indicator(
            df["close"], window=14, fillna=True
        ).iloc[-1]
        indicators["ema_21"] = trend.ema_indicator(
            df["close"], window=21, fillna=True
        ).iloc[-1]
        indicators["ema_60"] = trend.ema_indicator(
            df["close"], window=60, fillna=True
        ).iloc[-1]

        # Relative Strength Index (RSI) for different periods
        indicators["rsi_7"] = momentum.rsi(
            df["close"], window=7, fillna=True).iloc[-1]
        indicators["rsi_14"] = momentum.rsi(df["close"], window=14, fillna=True).iloc[
            -1
        ]
        indicators["rsi_21"] = momentum.rsi(df["close"], window=21, fillna=True).iloc[
            -1
        ]
        indicators["rsi_60"] = momentum.rsi(df["close"], window=60, fillna=True).iloc[
            -1
        ]

        # Moving Average Convergence Divergence (MACD) for different periods
        macd = trend.MACD(df["close"], window_fast=7,
                          window_slow=14, window_sign=9)
        indicators["macd_7"] = macd.macd().iloc[-1]
        indicators["macdsignal_7"] = macd.macd_signal().iloc[-1]
        indicators["macdhist_7"] = macd.macd_diff().iloc[-1]

        # On-Balance Volume (OBV)
        indicators["obv"] = volume.on_balance_volume(
            df["close"], df["volume"], fillna=True
        ).iloc[-1]
    else:
        # Initialize with None if no data
        for key in [
            "sma_7",
            "sma_14",
            "sma_21",
            "sma_60",
            "ema_7",
            "ema_14",
            "ema_21",
            "ema_60",
            "rsi_7",
            "rsi_14",
            "rsi_21",
            "rsi_60",
            "macd_7",
            "macdsignal_7",
            "macdhist_7",
            "obv",
        ]:
            indicators[key] = None

    logger.debug(f'Computed indicators: {indicators}')

    # Convert NumPy values to native Python types
    converted_indicators = {}
    for key, value in indicators.items():
        if value is not None:
            try:
                # Convert NumPy values to native Python float
                converted_indicators[key] = float(value)
            except (TypeError, ValueError):
                # If conversion fails, keep the original value
                converted_indicators[key] = value
        else:
            converted_indicators[key] = None

    return {**candle, **converted_indicators}
