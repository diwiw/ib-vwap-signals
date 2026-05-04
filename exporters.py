import os
import csv
from abc import ABC, abstractmethod
import pandas as pd

# ---------------------------------------------------------
# BASE INTERFACE
# ---------------------------------------------------------
class SignalExporter(ABC):
    """
    Abstract Base Class for exporting trading signals.
    Allows easy swapping between CSV (for PoC) and ZeroMQ/WebSockets (for Enterprise).
    """
    @abstractmethod
    def export(self, df: pd.DataFrame, symbol:str):
        pass

# ---------------------------------------------------------
# CSV EXPORTER 
# ---------------------------------------------------------
class CSVSignalExporter(SignalExporter):
    def __init__(self, output_dir: str = "signals_output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, df: pd.DataFrame, symbol: str):
        if df.empty or 'signal' not in df.columns:
            return
        
        latest = df.iloc[-1]

        signal_str = "NEUTRAL"
        if latest['signal'] == 1: signal_str = "BUY"
        elif latest['signal'] == -1: signal_str = "SELL"

        output_dict = {
            "timestamp": str(latest['date']),
            "symbol": symbol,
            "close_price": round(latest['close'], 2),
            "vwap_value": round(latest['vwap'], 2),
            "signal": signal_str
        }

        output_file = os.path.join(self.output_dir, f"{symbol}_latest_signal.csv")

        file_exists = os.path.isfile(output_file)
        with open(output_file, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'symbol', 'close_price', 'vwap_value', 'signal']
            writer = csv.DictWriter(csvfile, Fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

        print(f"[+] CSV EXPORT: [{signal_str}] at {latest['date']} > {output_file}")

# ---------------------------------------------------------
# ZMQ PUBLISHER FOR C++ ENGINE (STUB)
# ---------------------------------------------------------

class ZMQSignalPublisher(SignalExporter):
    """
    High-performance IPC/TCP publisher for C++ execution engines.
    Requires 'pyzmq' library. This is a stub for the commercial version.
    """
    def __init__(self, port: int = 5555):
        self.port = port
        print(f"[*] Initializing ZeroMQ Publisher on port {self.port} (Commercial Mode Required)")
        # import zmq
        # self.context = zmq.Context()
        # self.socket = self.context.socket(zmq.PUB)
        # self.socket.bind(f"tcp://*:{self.port}")

    def export(self, df: pd.DataFrame, symbol: str):
        # Commercial implementation hidden behind evaluation license.
        print(f"[!] ZMQ PUBLISH: Signal ready for C++ engine via IPC. (Implementation omitted in PoC)")
        pass