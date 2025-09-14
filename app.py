# app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data_cleaning import get_clean_data

# Load the data
print("Loading data for dashboard...")
df = get_clean_data()
print(f"Data loaded. Shape: {df.shape}")

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # Expose the server for deployment

# Calculate some overall metrics for the dashboard
avg_sales = df['sales'].mean()
avg_roas = df['roas'].mean()
final_stock_price = df['close'].iloc[-1]
best_campaign = df.groupby('campaign_id')['roas'].mean().idxmax()

# Create the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Business Performance Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    ]),
    
    # Key Metrics Cards
    html.Div([
        html.Div([
            html.H3("Avg. Daily Sales", style={'color': '#7f8c8d', 'fontSize': '1.2em'}),
            html.H2(f"${avg_sales:.2f}", style={'color': '#2c3e50', 'fontSize': '2em'})
        ], className='metric-card', style={
            'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'
        }),
        
        html.Div([
            html.H3("Avg. ROAS", style={'color': '#7f8c8d', 'fontSize': '1.2em'}),
            html.H2(f"{avg_roas:.2f}x", style={'color': '#2c3e50', 'fontSize': '2em'})
        ], className='metric-card', style={
            'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'
        }),
        
        html.Div([
            html.H3("Current Stock Price", style={'color': '#7f8c8d', 'fontSize': '1.2em'}),
            html.H2(f"${final_stock_price:.2f}", style={'color': '#2c3e50', 'fontSize': '2em'})
        ], className='metric-card', style={
            'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'
        }),
        
        html.Div([
            html.H3("Best Campaign", style={'color': '#7f8c8d', 'fontSize': '1.2em'}),
            html.H2(f"{best_campaign}", style={'color': '#2c3e50', 'fontSize': '2em'})
        ], className='metric-card', style={
            'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'
        }),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap', 'marginBottom': '30px'}),
    
    # Date Range Selector
    html.Div([
        html.Label("Select Date Range:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df.index.min(),
            end_date=df.index.max(),
            display_format='YYYY-MM-DD'
        )
    ], style={'margin': '20px', 'textAlign': 'center'}),
    
    # Charts Row 1
    html.Div([
        # Stock Price vs Sales Trend
        html.Div([
            html.H3("Stock Price vs Marketing Sales Trend", style={'textAlign': 'center'}),
            dcc.Graph(id='trend-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        # ROAS by Campaign
        html.Div([
            html.H3("ROAS by Marketing Campaign", style={'textAlign': 'center'}),
            dcc.Graph(id='roas-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
    ]),
    
    # Charts Row 2
    html.Div([
        # Correlation Heatmap
        html.Div([
            html.H3("Metrics Correlation Heatmap", style={'textAlign': 'center'}),
            dcc.Graph(id='correlation-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        # Daily Returns Distribution
        html.Div([
            html.H3("Stock Daily Returns Distribution", style={'textAlign': 'center'}),
            dcc.Graph(id='returns-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
    ]),
    
    # Footer
    html.Div([
        html.P("Data automatically updated from Alpha Vantage API and marketing sources", 
              style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '50px'})
    ])
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})

# Callback for updating charts based on date selection
@app.callback(
    [Output('trend-chart', 'figure'),
     Output('roas-chart', 'figure'),
     Output('correlation-chart', 'figure'),
     Output('returns-chart', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_charts(start_date, end_date):
    # Filter data based on selected date range
    filtered_df = df.loc[start_date:end_date]
    
    # 1. Trend Chart (Stock Price vs Sales)
    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(
        go.Scatter(x=filtered_df.index, y=filtered_df['close'], name="Stock Price", line=dict(color='red')),
        secondary_y=False,
    )
    fig_trend.add_trace(
        go.Scatter(x=filtered_df.index, y=filtered_df['sales'], name="Marketing Sales", line=dict(color='blue', dash='dot')),
        secondary_y=True,
    )
    fig_trend.update_layout(title_text="Stock Price vs Marketing Sales Over Time")
    fig_trend.update_xaxes(title_text="Date")
    fig_trend.update_yaxes(title_text="Stock Price ($)", secondary_y=False)
    fig_trend.update_yaxes(title_text="Sales ($)", secondary_y=True)
    
    # 2. ROAS by Campaign
    fig_roas = px.box(filtered_df, x='campaign_id', y='roas', 
                     title="Return on Ad Spend by Campaign")
    fig_roas.update_layout(yaxis_title="ROAS", xaxis_title="Campaign")
    
    # 3. Correlation Heatmap
    numeric_cols = ['sales', 'cost', 'roas', 'daily_visitors', 'close', 'daily_return']
    correlation_matrix = filtered_df[numeric_cols].corr()
    fig_corr = px.imshow(correlation_matrix, 
                        text_auto=True, 
                        aspect="auto",
                        title="Correlation Between Metrics")
    
    # 4. Daily Returns Distribution
    fig_returns = px.histogram(filtered_df, x='daily_return', 
                              nbins=30, 
                              title="Distribution of Daily Stock Returns")
    fig_returns.update_layout(xaxis_title="Daily Return (%)", yaxis_title="Frequency")
    
    return fig_trend, fig_roas, fig_corr, fig_returns

if __name__ == '__main__':
    print("Starting Dash server...")
    app.run(debug=True, host='0.0.0.0', port=8050)