# Forex Trading AI Agent (FELIX)

## Overview
FELIX is a simple AI-powered Forex trading agent that uses technical indicators and news analysis to make trading decisions. It leverages the OpenAI GPT-4o model to predict price movements and decide whether to buy, sell, or hold a currency pair.

## Features
- Login to MetaTrader 5 account
- Retrieve currency pair information
- Analyze technical indicators (Bollinger Bands, Moving Average Crossover, RSI)
- Execute trades on MetaTrader 5
- Fetch and filter news for specific currencies
- Get current UTC time

## Setup

### Prerequisites
- Python 3.8+
- MetaTrader 5
- OpenAI API Key
- News API URL

### Installation
1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your OpenAI API key, News API URL, and MetaTrader 5 credentials:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    NEWS_API_URL=your_news_api_url
    LOGIN=your_mt5_login
    PASSWORD=your_mt5_password
    SERVER=your_mt5_server
    ```

## Usage

### Running the Agent
To run the agent, execute the following command:
```sh
python main.py
```

### Agent Tools
- **login_to_account**: Logs into the MetaTrader 5 account using provided credentials.
- **get_pair_info**: Retrieves information for a specified currency pair and timeframe.
- **use_indicators**: Analyzes the currency pair using Bollinger Bands, Moving Average Crossover, and RSI.
- **execute_trade**: Executes a trade on MetaTrader 5.
- **get_news**: Fetches and filters news for specific currencies.
- **get_utc_time**: Returns the current UTC time.


## Roadmap
- Implement more technical indicators
- Add support for more trading platforms
- Improve news analysis and sentiment analysis
- Optimize AI model for better predictions
- Implement a web interface for the agent
- Add support for more currency pairs
- Implement a reward system for the agent
- Add support for multiple agents
- Implement a portfolio management system
- Add support for backtesting
- Implement a risk management system

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.
