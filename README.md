# Project Title

**Trading System -- Multi-Strategy Indian Stock Market Scanner**

## Table of Contents

-   About The Project
-   Built With
-   Key Features
-   Getting Started
-   Technologies Used (Prerequisites)
-   Installation
-   Usage
-   Project Structure
-   How It Works
-   Main Python Functions
-   Version History
-   Future Roadmap
-   License Description
-   Disclaimer

## About The Project

Built on - May 2024

Trading System is a modular Python-based market analysis platform for
Indian equities that evolved through multiple versions (v1--v8). It
combines live NSE market data, Yahoo Finance historical data,
multiprocessing, scheduled execution, technical indicator calculations,
price and volume breakout detection, ORB analysis, and Flask dashboard
integration. The project is designed as a foundation for intraday and
swing trading research.

### Built With

-   Python 3
-   pandas
-   yfinance
-   nselib
-   jugaad-data
-   multiprocessing
-   Flask
-   datetime
-   re

### Key Features

-   Live NSE quote retrieval
-   Historical market data download
-   Parallel processing across CPU cores
-   RSI calculations
-   Price breakout detection
-   Volume breakout detection
-   ORB (Opening Range Breakout) analysis
-   Common stock filtering
-   Scheduled market scanning
-   Flask web dashboard (v8)
-   Modular architecture
-   Automatic retry logic

## Getting Started

### Technologies Used (Prerequisites)

-   Python 3.10+
-   pip
-   Internet connection
-   NSE market access

``` bash
pip install pandas yfinance nselib jugaad-data flask
```

### Installation

``` bash
git clone https://github.com/pandiyan07/Multi-Strategy-Indian-Stock-Market-Scanner.git
cd Multi-Strategy-Indian-Stock-Market-Scanner
pip install -r requirements.txt
python Trading_system_v5.py
```

## Usage

Execute any version (v1--v8) depending on the required functionality.
The system downloads market data, performs technical analysis, detects
trading opportunities, and prints or serves the results.

## Project Structure

``` text
Trading system v1.py      # Initial single-process scanner
Trading system v2.py      # Multiprocessing implementation
Trading system v3.py      # Scheduled periodic scanner
Trading system v4.py      # Batch data downloader
Trading_system_v5.py      # Modular breakout engine
Trading_system_v8.py      # Flask dashboard integration
```

## How It Works

1.  Initialize market configuration.
2.  Create stock watchlist.
3.  Connect to NSE and Yahoo Finance.
4.  Download live and historical market data.
5.  Schedule market scans.
6.  Calculate technical indicators.
7.  Detect price breakout opportunities.
8.  Detect abnormal volume breakouts.
9.  Calculate ORB values.
10. Filter common qualifying stocks.
11. Aggregate multiprocessing results.
12. Display terminal tables or Flask dashboard.

## Main Python Functions

  ---------------------------------------------------------------------------
  Function                           Description
  ---------------------------------- ----------------------------------------
  `THE_MAIN()`                       Main orchestration workflow.

  `DATA_FETCHER()`                   Downloads live and historical market
                                     data.

  `RSI_14_CALCULATOR()`              Calculates 14-period RSI.

  `THREE_CANDLE_PRICE_BREAKOUT()`    Detects three-candle price breakout
                                     patterns.

  `THREE_CANDLE_VOLUME_BREAKOUT()`   Detects three-candle volume breakouts.

  `APPENDER()`                       Stores processed analysis results.

  `SCHEDULE_TASK()`                  Executes scans at configured intervals.

  `COMMON_STOCKS()`                  Identifies stocks satisfying multiple
                                     conditions.

  `OUTPUT_PRINTER()`                 Formats and prints final output tables.
  ---------------------------------------------------------------------------

## Version History

-   v1 -- Single-process implementation
-   v2 -- Multiprocessing
-   v3 -- Scheduled periodic scanning
-   v4 -- Batch market-data downloads
-   v5 -- Modular breakout engine
-   v8 -- Flask dashboard integration

## Future Roadmap

-   Automated order placement
-   Swing trading module
-   AI-assisted ranking
-   Portfolio tracking
-   Performance analytics
-   REST API

## License Description

Recommended License: MIT License.

## Disclaimer

This project is intended for educational, research, and
strategy-development purposes only. It does not provide financial advice
or guarantee profitable trading outcomes.
