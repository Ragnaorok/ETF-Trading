import pandas as pd
import plotly.graph_objects as go

# Read the JSON file into a pandas DataFrame
fngd = pd.read_json('FNGD.json')
fngu = pd.read_json('FNGU.json')
# Select specific columns
columns = ['Date', 'Close','Adj Close', 'Open', 'High','Low','Volume']
fngd_graph = fngd[columns].copy()  # Make a copy to avoid the warning
fngu_graph = fngu[columns].copy()

# Calculate the moving average
window_size = 7  # Set the window size for the moving average
fngd_graph['FNGD Moving Average'] = fngd_graph['Adj Close'].rolling(window_size).mean()
fngu_graph['FNGU Moving Average'] = fngu_graph['Adj Close'].rolling(window_size).mean()

# Create the plot using Plotly
FNGD_fig = go.Figure()
FNGD_fig.add_trace(go.Scatter(x=fngd_graph['Date'], y=fngd_graph['Adj Close'], name='Original Data'))
FNGD_fig.add_trace(go.Scatter(x=fngd_graph['Date'], y=fngd_graph['FNGD Moving Average'], name='FNDG Moving Average'))

FNGU_fig = go.Figure()
FNGU_fig.add_trace(go.Scatter(x=fngu_graph['Date'], y=fngu_graph['Adj Close'], name='Original Data'))
FNGU_fig.add_trace(go.Scatter(x=fngu_graph['Date'], y=fngu_graph['FNGU Moving Average'], name='FNDU Moving Average'))

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
# Save the table as HTML
table_FNGD_fig.write_html('FNGD_table.html')
table_FNGU_fig.write_html('FNGU_table.html')
# Combine the HTML files into a single page
# Combine the HTML files into a single page
with open('combined.html', 'w', encoding='utf-8') as combined_file:
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
