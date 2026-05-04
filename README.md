# IB-VWAP Quantitative Execution Engine 🚀

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

## 1. Overview
A high-performance, low-latency market data ingestion and signal execution pipeline. This system connects to Interactive Brokers (IB) API, calculates real-time quantitative metrics (e.g., VWAP), and streams actionable signals to downstream execution platforms via ZeroMQ (IPC/TCP).

## 2. System Architecture
This engine is built on a decoupled, microservices-oriented architecture:
* **Ingestion Layer (Python):** Handles network resilience and asynchronous data fetching via `ib_insync`.
* **Calculation Engine (C++23):** *[To be unlocked in full version]* Manages deterministic, low-latency state and advanced mathematical models.
* **Transport Layer (ZMQ):** Ensures sub-millisecond signal delivery between the ingestion layer and execution platforms.

## 3. Key Features
* **Real-time Data Streaming:** Event-driven architecture for tick-level and minute-level data.
* **Abstract Exporter Interfaces:** Seamlessly swap between CSV logging (for PoC/Debugging) and ZeroMQ publishing (for Production).
* **Robust Reconnection:** Automatic connection retries for IB Gateway / TWS network drops.
* **Memory-Safe Computations:** Optimized `pandas` and `numpy` operations for initial stages, with C++ structures for advanced states.

## 4. Prerequisites
Ensure the following dependencies are installed before deploying the node:
* Python 3.9+
* Interactive Brokers TWS or IB Gateway (API port enabled)
* `requirements.txt` packages (`ib_insync`, `pandas`, `pyzmq`)

## 5. Installation & Deployment
```bash
# Clone the repository
git clone https://github.com/diwiw/ib-vwap-signals.git
cd ib-vwap-signals

# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install core and commercial dependencies
pip install -r requirements.txt
```

## 6. Configuration
Configure the node via the .env file or command-line arguments:
* `IB_HOST`: IP address of the IB Gateway (Default: `127.0.0.1`)
* `IB_PORT`: API port (Default: `7497` for Paper, `7496` for Live)
* `ZMQ_PORT`: IPC port for the C++ Engine communication (Default: `5555`)

## 7. Quick Start (Standalone Mode)
To run the ingestion node independently for signal validation:
```
python main.py --symbol AAPL --mode debug
```

## 8. License & Usage Terms
### PROPRIETARY SOFTWARE - ALL RIGHTS RESERVED
This software is developed, maintained, and exclusively owned by Dawid Skrobol. 
Unauthorized copying, modification, distribution, or commercial execution (including live market trading or integration into proprietary platforms) without an explicit, active commercial agreement is strictly prohibited.