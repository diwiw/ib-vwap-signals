import pandas as pd
from ib_insync import IB, util, Contract, Stock

class IBDataEngine:
    def __init__(self, host='127.0.01', port=7497, client_id=1):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()

    def connect(self) -> bool:
        """Establishes connection to the local TWS or IB Gateway instance."""
        try:
            # timeout=10 helps if TWS is slow to respond
            self.ib.connect(self.host, self.port, clientId=self.client_id, timeout=10)
            print(f"[+] Successfully connected to IB API ({self.host}:{self.port})")
            return True
        except Exception as e:
            print(f"[-] Connection failed. Is TWS/Gateway running? Error: {e}")
            return False
        
    def disconnect(self):
        """Safely disconnect from the API."""
        self.ib_disconnect()
        print("[+] Disconnected from IB API.")

    def fetch_historical_data(self, symbol: str, exchange: str = 'SMART', currency: str = 'USD') -> pd.DataFrame:
        """
        Fetches 1-day of 1-minute bars for the VWAP calculation.
        """
        contract = Stock(symbol, exchange, currency)

        # Qualify contract to get the exact conId (required by IB)
        self.ib.qualifyContracts(contract)

        print(f"[~] Fetching 1-minute historical data for {symbol}...")
        bars = self.ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='1 D',
            barSizeSettings='1 min',
            whatToShow='TRADES',
            useRTH=True         # Regular Trading Hours only
        )

        if not bars:
            print(f"[-] No data received for {symbol}.")
            return pd.DataFrame()
        
        # Convert IB objects directly to a Pandas DataFrame
        df = util.df(bars)
        return df
