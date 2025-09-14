# Automated Business Analytics Dashboard

An end-to-end data analytics solution that automatically collects, analyzes, and visualizes business performance data.

## 🚀 Features

- **Real-time Data Pipeline**: Fetches stock data from Alpha Vantage API and marketing data
- **Automated Reporting**: Generates professional PDF reports with insights and visualizations  
- **Interactive Dashboard**: Plotly Dash web app with filterable charts and metrics
- **Business Intelligence**: Calculates ROAS, moving averages, correlations, and trends

## 📊 Demo

### Interactive Dashboard
![Dashboard Screenshot](images/dashboard-screenshot.png) *Add a screenshot later*

### Automated Reports
![Report Example](images/report-screenshot.png) *Add a screenshot later*

## 🛠️ Tech Stack

- **Python**: Pandas, NumPy, Matplotlib, Seaborn
- **Dashboard**: Plotly Dash 
- **Reporting**: xhtml2pdf, Jinja2
- **Data**: Alpha Vantage API, Web scraping
- **Visualization**: Plotly, Matplotlib, Seaborn

## 📁 Project Structure

automated-business-analyst/
├── app.py # Interactive dashboard
├── generate_report.py # Automated PDF reporting
├── report_utils.py # Reporting utilities
├── data_acquisition.py # API data fetching
├── data_cleaning.py # Data processing pipeline
├── Analysis.ipynb # Exploratory analysis
├── templates/
│ └── report_template.html # PDF template
├── requirements.txt # Python dependencies
└── README.md # This file