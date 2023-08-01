import pandas as pd
import plotly.graph_objects as go

# Read the JSON file into a pandas DataFrame
fngd = pd.read_json('FNGD.json')
fngu = pd.read_json('FNGU.json')

# Select specific columns
columns = ['Date', 'Adj Close']
fngd_graph = fngd[columns].copy()  # Make a copy to avoid the warning
fngu_graph = fngu[columns].copy()

# Calculate the moving average
window_size = 7  # Set the window size for the moving average
fngd_graph['FNGD Moving Average'] = fngd_graph['Adj Close'].rolling(window_size).mean()
fngu_graph['FNGU Moving Average'] = fngu_graph['Adj Close'].rolling(window_size).mean()

# Create the plot using Plotly
FNGD_fig = go.Figure()
FNGD_fig.add_trace(go.Scatter(
    x=fngd_graph['Date'],
    y=fngd_graph['Adj Close'],
    name='Original Data',
    hovertemplate='%{x}<br>Open: %{text[0]}<br>High: %{text[1]}<br>Low: %{text[2]}<br>Close: %{text[3]}',
    text=fngd[['Open', 'High', 'Low', 'Close']].apply(lambda row: tuple(row), axis=1)
))
FNGD_fig.add_trace(go.Scatter(
    x=fngd_graph['Date'],
    y=fngd_graph['FNGD Moving Average'],
    name='FNGD Moving Average',
    hovertemplate='%{x}<br>Value: %{y:.2f}'
))

FNGU_fig = go.Figure()
FNGU_fig.add_trace(go.Scatter(
    x=fngu_graph['Date'],
    y=fngu_graph['Adj Close'],
    name='Original Data',
    hovertemplate='%{x}<br>Open: %{text[0]}<br>High: %{text[1]}<br>Low: %{text[2]}<br>Close: %{text[3]}',
    text=fngu[['Open', 'High', 'Low', 'Close']].apply(lambda row: tuple(row), axis=1)
))
FNGU_fig.add_trace(go.Scatter(
    x=fngu_graph['Date'],
    y=fngu_graph['FNGU Moving Average'],
    name='FNGU Moving Average',
    hovertemplate='%{x}<br>Value: %{y:.2f}'
))

# Set the axis labels and title of the FNGD_figure
FNGD_fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Adj Close',
    title='FNGD Moving Average Plot'
)
FNGU_fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Adj Close',
    title='FNGU Moving Average Plot'
)

# Save the plot as HTML
FNGD_fig.write_html('FNGD_plot.html')
FNGU_fig.write_html('FNGU_plot.html')

# Create the table using Plotly
table_FNGD_fig = go.Figure(data=[go.Table(header=dict(values=fngd_graph.columns),
                                     cells=dict(values=[fngd_graph[col] for col in fngd_graph.columns]))])

table_FNGU_fig = go.Figure(data=[go.Table(header=dict(values=fngu_graph.columns),
                                     cells=dict(values=[fngu_graph[col] for col in fngu_graph.columns]))])

# Calculation of the standard deviation
fngd_graph['FNGD Standard Deviation'] = fngd_graph['Adj Close'].rolling(window_size).std()
fngu_graph['FNGU Standard Deviation'] = fngu_graph['Adj Close'].rolling(window_size).std()
fngd_graph = fngd_graph.round(2)
fngu_graph = fngu_graph.round(2)

# Convert the date column to a string and remove the time portion
fngd_graph['Date'] = fngd_graph['Date'].astype(str).str.slice(0, 10)
fngu_graph['Date'] = fngu_graph['Date'].astype(str).str.slice(0, 10)

# Update the table to include the new columns with the standard deviation values
table_FNGD_fig = go.Figure(data=[go.Table(header=dict(values=fngd_graph.columns),
                                     cells=dict(values=[fngd_graph[col] for col in fngd_graph.columns]))])
table_FNGU_fig = go.Figure(data=[go.Table(header=dict(values=fngu_graph.columns),
                                     cells=dict(values=[fngu_graph[col] for col in fngu_graph.columns]))])

# Save the table as HTML
table_FNGD_fig.write_html('FNGD_table.html')
table_FNGU_fig.write_html('FNGU_table.html')

# Combine the HTML files into a single page
with open('combined.html', 'w', encoding='utf-8') as combined_file:
    combined_file.write('<style>h1 {text-align: center;}</style>')
    with open('FNGD_plot.html', 'r', encoding='utf-8') as plot_file:
        combined_file.write('<h1>FNGD Plot</h1>')
        combined_file.write(plot_file.read())
    
    with open('FNGD_table.html', 'r', encoding='utf-8') as table_file:
        combined_file.write('<h1>FNGD Table</h1>')
        combined_file.write(table_file.read())
    
    with open('FNGU_plot.html', 'r', encoding='utf-8') as plot_file:
        combined_file.write('<h1>FNGU Plot</h1>')
        combined_file.write(plot_file.read())
    
    with open('FNGU_table.html', 'r', encoding='utf-8') as table_file:
        combined_file.write('<h1>FNGU Table</h1>')
        combined_file.write(table_file.read())

