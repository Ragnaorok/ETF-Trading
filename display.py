import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file into a pandas DataFrame
fngd = pd.read_csv('FNGD.csv')

# Select specific columns
fngd_columns = ['Adj Close', 'Date']
toGraph = fngd[fngd_columns]

# Plot the selected columns
plt.plot(toGraph['Date'], toGraph['Adj Close'])

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Adj Close')
plt.title('FNGD Stock')

# Show the plot
plt.show()