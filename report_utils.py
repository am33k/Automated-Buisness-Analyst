# report_utils.py
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def create_trend_chart_base64(df):
    """Create trend chart and return as base64 string"""
    try:
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 7)
        
        fig, ax1 = plt.subplots(figsize=(14, 7))
        color = 'tab:red'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Stock Price (Close)', color=color)
        ax1.plot(df.index, df['close'], color=color, label='Stock Price', linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Marketing Sales', color=color)
        ax2.plot(df.index, df['sales'], color=color, label='Marketing Sales', linestyle='--')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title('Trend Analysis: Stock Price vs. Marketing Sales Over Time', fontsize=16)
        fig.tight_layout()
        
        # Save to buffer and convert to base64
        from io import BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        
        return image_base64
    except Exception as e:
        print(f"Error creating trend chart: {e}")
        return None

def create_roas_chart_base64(df):
    """Create ROAS chart and return as base64 string"""
    try:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='campaign_id', y='roas')
        plt.title('Return on Ad Spend (ROAS) by Marketing Campaign', fontsize=14)
        plt.xlabel('Campaign ID')
        plt.ylabel('ROAS')
        
        # Save to buffer and convert to base64
        from io import BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        
        return image_base64
    except Exception as e:
        print(f"Error creating ROAS chart: {e}")
        return None

def generate_insights(df):
    """Generate insights from the data"""
    # Trend insight
    correlation = df['sales'].corr(df['close'])
    if correlation > 0.5:
        trend_insight = "Strong positive correlation observed between marketing sales and stock price. Increased sales activity appears to correlate with higher stock valuations."
    elif correlation < -0.5:
        trend_insight = "Interesting inverse relationship detected: higher marketing sales correlate with lower stock prices. This warrants further investigation."
    else:
        trend_insight = "No strong correlation detected between daily marketing sales and stock price movements in this period."
    
    # ROAS insight
    best_campaign = df.groupby('campaign_id')['roas'].mean().idxmax()
    worst_campaign = df.groupby('campaign_id')['roas'].mean().idxmin()
    roas_insight = f"Campaign '{best_campaign}' demonstrates the highest average ROAS, making it our most efficient campaign. Campaign '{worst_campaign}' may require optimization or review."
    
    return trend_insight, roas_insight