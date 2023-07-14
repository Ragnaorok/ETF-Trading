import matplotlib.pyplot as plt
import pandas as pd

# Read the specific columns from the CSV file into a pandas DataFrame
fngd_columns = ['Adj Close', 'Date']
fngd = pd.read_csv('FNGD.csv', usecols=fngd_columns)

# Plot the selected columns
plt.plot(fngd['Date'], fngd['Adj Close'])

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Adj Close')
plt.title('FNGD Stock')

# Show the plot
plt.show()