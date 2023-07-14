import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

# Read the CSV file into a pandas DataFrame
fngd = pd.read_csv('FNGD.csv')

# Select specific columns
fngd_columns = ['Adj Close', 'Date']
toGraph = fngd[fngd_columns]
toGraph.head()
# Plot the selected columns




# Save the plot as HTML
# Create the plot using Plotly
fig = go.Figure(data=go.Scatter(x=toGraph['Date'], y=toGraph['Adj Close']))

# Save the plot as HTML
fig.write_html('plot.html')