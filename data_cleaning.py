import pandas as pd
import numpy as np
from data_acquisition import get_stock_data, get_marketing_data

def clean_and_transform_Stock_data(stock_df):
    """
    Cleans the stock DataFrame and ads calculated financial metrics.
    """
    if stock_df.empty:
        return stock_df
    
    # Make a copy to avoid modifying the original
    df = stock_df.copy()

    # 1. Calculate daily percentage return (a key KPI)
    df['daily_return'] = df['close'].pct_change() * 100

    # 2. Calculate a 7-day moving average of the closing price (to identidy trends)
    df['moving_avg_7d'] = df['close'].rolling(window=7).mean()

    # 3. Drop the first 6 rows which now have NaN due to the moving averasge calculation
    df = df.dropna()

    print("Stock data cleaned and transformed")
    return df

# Test the function
if __name__=="__main__":
    stock_raw = get_stock_data("IBM")
    stock_clean = clean_and_transform_Stock_data(stock_raw)
    print(stock_clean[['close', 'daily_return', 'moving_avg_7d']].head(10)) # Show first 10 to see the moving avg


# data_cleaning.py (fix the warning in clean_and_transform_marketing_data)
def clean_and_transform_marketing_data(marketing_df):
    """
    Cleans the marketing DataFrame and adds calculated marketing metrics.
    Let's pretend our mock data is for an online store.
    """
    if marketing_df.empty:
        return marketing_df

    df = marketing_df.copy()
    
    # 1. Calculate 'sales' based on our pretend metrics: visitors * conversion rate * order value
    df['sales'] = (df['daily_visitors'] * df['conversion_rate'] * df['avg_order_value']).round(2)
    
    # 2. Calculate 'cost' arbitrarily for ROAS calculation.
    np.random.seed(42)
    cost_factors = {'setosa': 0.5, 'versicolor': 0.6, 'virginica': 0.7}
    df['cost_factor'] = df['campaign_id'].map(cost_factors)
    df['cost'] = (df['sales'] * df['cost_factor']).round(2)
    
    # 3. Calculate Return on Ad Spend (ROAS)
    df['roas'] = (df['sales'] / df['cost']).round(2)
    
    # 4. FIXED: Handle potential infinities from division by zero
    # Use .loc to avoid the chained assignment warning
    mask = df['roas'].isin([np.inf, -np.inf])
    df.loc[mask, 'roas'] = np.nan
    
    print("Marketing data cleaned and transformed.")
    return df

# Test the function
if __name__ == "__main__":
    marketing_raw = get_marketing_data()
    marketing_clean = clean_and_transform_marketing_data(marketing_raw)
    print(marketing_clean[['sales', 'cost', 'roas']].head())


def merge_datasets(stock_df, marketing_df):
    """
    Merges the stock and marketing DataFrames on the date index.
    Uses an inner join to only keep dates present in both datasets.
    """
    # Inner join ensures we only have dates where both marketing and stock data exist
    merged_df = pd.merge(marketing_df, stock_df, how='inner', left_index=True, right_index=True)
    
    print(f"Datasets merged successfully. Final shape: {merged_df.shape}")
    return merged_df

def get_clean_data():
    """
    Main function to run the entire data acquisition and cleaning pipeline.
    Returns the merged, cleaned DataFrame.
    """
    print("Acquiring data...")
    stock_raw = get_stock_data("IBM")
    # Get the index from the raw stock data to align dates
    stock_dates = stock_raw.index 
    
    # Pass the stock_dates to the marketing function
    marketing_raw = get_marketing_data(stock_dates=stock_dates)
    
    print("Cleaning and transforming data...")
    stock_clean = clean_and_transform_Stock_data(stock_raw)
    marketing_clean = clean_and_transform_marketing_data(marketing_raw)
    
    print("Merging datasets...")
    master_df = merge_datasets(stock_clean, marketing_clean)
    
    return master_df

# Test the entire pipeline
if __name__ == "__main__":
    final_df = get_clean_data()
    print("\nMaster DataFrame Columns:")
    print(final_df.columns.tolist())
    print("\nMaster DataFrame Head:")
    print(final_df.head())