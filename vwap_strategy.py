import pandas as pd

def calculate_vwap(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the Volume Weighted Average Price (VWAP) for a given DataFrame.
    Assumes the DataFrame contains 'high', 'low', 'close', and 'volume' columns.
    """
    
    # Check if data empty
    if df.empty or 'volume' not in df.columns:
        return df

    # 1. Calculate the Typical Price
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    
    # 2. Calculate VWAP cumultatively
    df['cv'] = df['typical_price'] * df['volume']
    df['cumulative_cv'] = df['cv'].cumsum()
    df['cumulative_volume'] = df['volume'].cumsum()
    
    # 3. Final VWAP value
    df['vwap'] = df['cumulative_cv'] / df['cumulative_volume']
    
    return df

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates simple trading signals based on Close price crossing the VWAP.
    Returns 1 for BUY, -1 for SELL, or 0 for NEUTRAL.
    """
    if 'vwap' not in df.columns:
        return df
        
    df['signal'] = 0
    # If the close price of the current bar/tick is strictly higher than VWAP -> BUY
    df.loc[df['close'] > df['vwap'], 'signal'] = 1
    # If the close price is strictly lower than VWAP -> SELL
    df.loc[df['close'] < df['vwap'], 'signal'] = -1
    
    return df