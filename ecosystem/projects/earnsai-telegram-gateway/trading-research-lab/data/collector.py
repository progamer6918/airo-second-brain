import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collect_btc_data(years: int = 2):
    """
    Fetches daily BTC-USD data for the last 'years' and saves it as a CSV.
    Prints a summary of the collected data.
    """
    ticker_symbol = "BTC-USD"
    data_dir = "trading-research-lab/data"
    output_filename = os.path.join(data_dir, f"{ticker_symbol}_daily.csv")

    logging.info(f"Starting data collection for {ticker_symbol} for the last {years} years.")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365) # Approximate 2 years

    try:
        # Fetch data using yfinance
        df = yf.download(ticker_symbol, start=start_date, end=end_date, interval="1d")

        if df.empty:
            logging.warning(f"No data fetched for {ticker_symbol} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.")
            return

        # Ensure the data directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Save to CSV
        df.to_csv(output_filename)
        logging.info(f"Data saved successfully to {output_filename}")

        # Print summary
        file_size_bytes = os.path.getsize(output_filename)
        file_size_kb = file_size_bytes / 1024
        
        logging.info("\n--- Data Collection Summary ---")
        logging.info(f"Ticker: {ticker_symbol}")
        logging.info(f"Number of rows: {len(df)}")
        logging.info(f"Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
        logging.info(f"File size: {file_size_kb:.2f} KB")
        logging.info("-----------------------------\n")

    except Exception as e:
        logging.error(f"An error occurred during data collection: {e}", exc_info=True)

if __name__ == "__main__":
    collect_btc_data(years=2)
