Financial Data Dashboard
A Python-based interactive financial dashboard built using Dash and Plotly. This dashboard visualizes financial data, including stock prices, portfolio values, and sector-based company metrics.

Features:
Display of summary statistics, such as total records and average portfolio value.
Interactive charts and graphs that allow filtering by sector, company, and stock price ranges.
Real-time updates to data visualizations based on user input.
Multiple chart types, including bar, line, and pie charts for detailed analysis.

Demo:
![image](https://github.com/user-attachments/assets/ba72b6e0-bf83-4d37-aa17-de9db82aec3e)

Installation
Prerequisites:
Ensure that you have Python 3.x installed on your machine along with pip.

Clone the Repository:
git clone https://github.com/yourusername/financial-dashboard.git
cd financial-dashboard

Install Dependencies
Install the required Python libraries using pip:
pip install -r requirements.txt

The main dependencies include:

dash: For building web applications.
dash-bootstrap-components: To style the dashboard with Bootstrap themes.
plotly: For generating interactive plots.
pandas: For handling and processing the dataset.
Dataset
The app uses a synthetic financial dataset (assets/financial_data.csv). You can modify or replace this dataset to include real financial data.

Usage:
Running the Application
Ensure you have the dataset file assets/financial_data.csv in place.

Start the app by running the following command:
python app.py
Open your web browser and navigate to localhost to view the dashboard.
