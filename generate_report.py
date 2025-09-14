# generate_report.py
import pandas as pd
from datetime import datetime
import os
import jinja2
from xhtml2pdf import pisa
from data_cleaning import get_clean_data
from report_utils import create_trend_chart_base64, create_roas_chart_base64, generate_insights

def convert_html_to_pdf(source_html, output_filename):
    """Convert HTML to PDF using xhtml2pdf"""
    try:
        with open(output_filename, "w+b") as output_file:
            pisa_status = pisa.CreatePDF(source_html, dest=output_file)
        return not pisa_status.err
    except Exception as e:
        print(f"Error converting HTML to PDF: {str(e)}")
        return False

def generate_pdf_report():
    """Main function to generate the PDF report."""
    try:
        print("Starting report generation...")
        
        # Get the data
        df = get_clean_data()
        if df.empty:
            print("Error: No data available for report generation.")
            return False
        
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Create visualizations as base64
        print("Creating visualizations...")
        trend_chart_base64 = create_trend_chart_base64(df)
        roas_chart_base64 = create_roas_chart_base64(df)
        
        if not trend_chart_base64 or not roas_chart_base64:
            print("Failed to create visualizations")
            return False
        
        print("Visualizations created successfully")
        
        # Generate insights
        trend_insight, roas_insight = generate_insights(df)
        
        # Calculate KPIs for the report
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = df.index.min().strftime("%Y-%m-%d")
        end_date = df.index.max().strftime("%Y-%m-%d")
        avg_sales = df['sales'].mean()
        avg_roas = df['roas'].mean()
        final_stock_price = df['close'].iloc[-1]
        total_observations = len(df)
        
        print("KPIs calculated")
        
        # Set up Jinja2 template
        template_loader = jinja2.FileSystemLoader(searchpath='./templates')
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template('report_template.html')
        
        print("Template loaded")
        
        # Render HTML with all variables
        html_content = template.render(
            report_date=report_date,
            start_date=start_date,
            end_date=end_date,
            avg_sales=avg_sales,
            avg_roas=avg_roas,
            final_stock_price=final_stock_price,
            total_observations=total_observations,
            trend_chart_base64=trend_chart_base64,
            roas_chart_base64=roas_chart_base64,
            trend_insight=trend_insight,
            roas_insight=roas_insight
        )
        
        print("HTML content rendered")
        
        # Write HTML to file (for debugging)
        os.makedirs('output', exist_ok=True)
        html_path = os.path.join('output', 'report.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("HTML file written")
        
        # Generate PDF from HTML
        pdf_path = os.path.join('output', f'business_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        success = convert_html_to_pdf(html_content, pdf_path)
        
        if success:
            print(f"PDF report successfully generated: {pdf_path}")
            
            # Also test opening the HTML in browser
            import webbrowser
            webbrowser.open(html_path)
            
            return True
        else:
            print("Failed to generate PDF")
            return False
        
    except Exception as e:
        print(f"Error in generate_pdf_report: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = generate_pdf_report()
    
    if success:
        print("Report generation completed successfully!")
    else:
        print("Report generation failed. Check the error messages above.")