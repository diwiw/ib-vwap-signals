import argparse
from ib_connector import IBDataEngine
from vwap_strategy import calculate_vwap, generate_signals
from exporters import CSVSignalExporter, ZMQSignalPublisher

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="IB-VWAP Execution Engine PoC")
    parser.add_argument('--symbol', type=str, default='AAPL', help='Ticker symbol to process')
    parser.add_argument('--mode', type=str, default='debug', choices=['debug', 'prod'], help='Execution mode')
    args = parser.parse_args()

    print("==================================================")
    print(" IB API TO VWAP SIGNAL GENERATOR")
    print(f" Target Symbol: {args.symbol} | Mode: {args.mode.upper()}")
    print("==================================================")
    
    # 1. Module configuration (Dependency Injection)
    engine = IBDataEngine()
    
    # 2. Setup the exporter
    # Using CSV for Patrick. Swap to ZMQSignalPublisher() for C++ integration.
    exporter = CSVSignalExporter() 
    
    # 3. Start engine
    if not engine.connect():
        return

    target_symbol = "AAPL" 
    
    # 4. Data Pipeline
    df = engine.fetch_historical_data(symbol=target_symbol)
    
    if not df.empty:
        df = calculate_vwap(df)
        df = generate_signals(df)
        
        # 5. Push signal through the selected channel
        exporter.export(df, target_symbol)

    engine.disconnect()

if __name__ == "__main__":
    main()