# Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

def load_data():
    # Load and preprocess the financial data
    df = pd.read_csv('assets/financial_data.csv')
    df['Stock Price'] = pd.to_numeric(df['Stock Price'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'])
    df['YearMonth'] = df['Date'].dt.to_period('M')  # Aggregating by month
    return df

df = load_data()

# Calculate summary statistics
num_records = len(df)
avg_stock_price = df['Stock Price'].mean()

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/styles.css'])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Financial Data Dashboard"), width=12, className="text-center my-4")
    ]),

    # Summary Statistics
    dbc.Row([
        dbc.Col(html.Div(f"Total Records: {num_records}", className='text-center my-2 top-text'), width=5),
        dbc.Col(html.Div(f"Average Stock Price: ${avg_stock_price:,.2f}", className='text-center my-2 top-text'), width=5),
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Stock Price Distribution", className="card-title"),
                    dcc.Dropdown(
                        id="sector-filter",
                        options=[{"label": sector, "value": sector} for sector in df['Sector'].unique()],
                        value=None,
                        placeholder="Select Sector"
                    ),
                    dcc.Graph(id="price-distribution")
                ])
            ])
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Stock Performance Comparison", className="card-title"),
                    dcc.Graph(id="performance-comparison")
                ])
            ])
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Portfolio Value Distribution", className="card-title"),
                    dcc.Slider(
                        id='value-slider',
                        min=df['Portfolio Value'].min(),
                        max=df['Portfolio Value'].max(),
                        value=df['Portfolio Value'].max(),
                        marks={int(value): f'${int(value):,}' for value in df['Portfolio Value'].quantile([0, 0.25, 0.5, 0.75, 1]).values},
                        step=1000
                    ),
                    dcc.Graph(id="value-distribution")
                ])
            ])
        ], width=12),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Market Trends", className="card-title"),
                    dcc.RadioItems(
                        id='chart-type',
                        options=[{'label': 'Line Chart', 'value': 'line'}, {'label': 'Bar Chart', 'value': 'bar'}],
                        value='line',
                        inline=True,
                        className='mb-3'
                    ),
                    dcc.Dropdown(
                        id="sector-trend-filter",
                        options=[{"label": sector, "value": sector} for sector in df['Sector'].unique()],
                        value=None,
                        placeholder="Select Sector"
                    ),
                    dcc.Graph(id="market-trends")
                ])
            ])
        ], width=12),
    ]),
], fluid=True)


# Callbacks for interactivity

@app.callback(
    Output('price-distribution', 'figure'),
    Input('sector-filter', 'value')
)
def update_price_distribution(selected_sector):
    # Filter the dataframe based on the selected sector
    if selected_sector:
        filtered_df = df[df['Sector'] == selected_sector]
    else:
        filtered_df = df

    # Check if the filtered dataframe is not empty
    if filtered_df.empty:
        return {}

    # Create the histogram
    fig = px.histogram(
        filtered_df, 
        x="Stock Price", 
        nbins=10, 
        color="Sector", 
        title="Stock Price Distribution by Sector",
        color_discrete_sequence=["#636EFA", "#EF553B"]
    )

    return fig


@app.callback(
    Output('performance-comparison', 'figure'),
    Input('sector-filter', 'value')
)
def update_performance_comparison(selected_sector):
    filtered_df = df[df['Sector'] == selected_sector] if selected_sector else df
    fig = px.bar(filtered_df, x="Company", y="Stock Price", color="Sector", barmode="group",
                 title="Stock Performance Comparison",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    return fig


@app.callback(
    Output('market-trends', 'figure'),
    [Input('chart-type', 'value'),
     Input('sector-trend-filter', 'value')]
)
def update_market_trends(chart_type, selected_sector):
    filtered_df = df[df['Sector'] == selected_sector] if selected_sector else df
    
    # Group by YearMonth and convert to string
    trend_df = filtered_df.groupby('YearMonth').size().reset_index(name='Count')
    trend_df['YearMonth'] = trend_df['YearMonth'].astype(str)  # Convert to string

    if chart_type == 'line':
        fig = px.line(trend_df, x='YearMonth', y='Count', title="Market Trends Over Time")
    else:
        fig = px.bar(trend_df, x='YearMonth', y='Count', title="Market Trends Over Time")
    
    return fig


@app.callback(
    Output('value-distribution', 'figure'),
    Input('value-slider', 'value')
)
def update_value_distribution(slider_value):
    filtered_df = df[df['Portfolio Value'] <= slider_value]
    fig = px.histogram(filtered_df, x="Portfolio Value", nbins=10, title="Portfolio Value Distribution")
    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
