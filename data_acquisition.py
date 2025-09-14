import pandas as pd
import requests
import os

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_stock_data(symbol="IBM"):
    """Fetches daily time series data for a stock from Alpha Vantage"""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status() #raises an error for bad status codes
        data = response.json()
        # the actual time series is nested in this key
        time_series = data["Time Series (Daily)"]
        # Convert into a dataframe and clean it up

        df = pd.DataFrame.from_dict(time_series, orient='index')
        df = df.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        })

        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df = df.sort_index()
        print(f"Successfully fetched {len(df)} days of data for {symbol}")
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error
    
# Test the function
if __name__=="__main__":
    stock_df = get_stock_data("IBM")
    print(stock_df.head()) 

# data_acquisition.py (update the get_marketing_data function)
def get_marketing_data(stock_dates=None):
    """Fetches mock marketing data from a web URL.
    If stock_dates is provided, generates marketing data for the same period.
    """
    # Using a public dataset URL for reliability
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    try:
        df = pd.read_csv(url)
        print("Successfully fetched marketing data.")

        # Rename columns to make it seem like marketing data for our project
        df = df.rename(columns={
            'sepal_length': 'daily_visitors',
            'sepal_width': 'click_through_rate',
            'petal_length': 'conversion_rate',
            'petal_width': 'avg_order_value',
            'species': 'campaign_id'
        })

        # --- CRITICAL FIX: Align dates with stock data ---
        if stock_dates is not None:
            # Generate dates matching the stock data's date range and length
            num_days = len(stock_dates)
            # If we have more marketing data rows than stock days, trim it.
            df = df.head(num_days)
            # Create a date index starting from the first stock date
            dates = pd.date_range(start=stock_dates.min(), periods=len(df), freq='D')
        else:
            # Fallback: use the old method if no stock_dates are provided
            dates = pd.date_range(start='2023-01-01', periods=len(df), freq='D')

        df['date'] = dates
        df.set_index('date', inplace=True)
        

        return df
    except Exception as e:
        print(f"Error fetching marketing data: {e}")
        return pd.DataFrame()
    
#testing the function

if __name__ =="__main__":
    marketing_df = get_marketing_data()
    print(marketing_df.head())
    