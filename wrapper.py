import pandas as pd
import plotly.graph_objects as go
import webbrowser

from Data_Retriever import DataRetrieverAdapter

def add_title(title):
    def decorator_generate_combined_html(generate_combined_html_func):
        def wrapper():
            # Create an instance of the DataRetrieverAdapter
            adapter = DataRetrieverAdapter()

            # Call the retrieve_data method
            adapter.retrieve_data()

            # Read the JSON files into pandas DataFrames
            fngd = pd.read_json('FNGD.json')
            fngu = pd.read_json('FNGU.json')

            # Ask the user for their selection
            user_input = input("Please enter your selection (FNGU / FNGD): ")

            # Check user input and generate the combined HTML accordingly
            with open('combined.html', 'w', encoding='utf-8') as combined_file:
                combined_file.write(f'<h1>{title}</h1>')

                if user_input.lower() == 'fngu':
                    # Ask the user for the start and end dates
                    start_date = input("Please enter the start date (YYYY-MM-DD): ")
                    end_date = input("Please enter the end date (YYYY-MM-DD): ")

                    # Filter FNGU data based on the start and end dates
                    filtered_fngu = fngu[(fngu['Date'] >= start_date) & (fngu['Date'] <= end_date)]

                    # Generate the FNGU plot using Plotly
                    FNGU_fig = go.Figure()
                    FNGU_fig.add_trace(go.Scatter(x=filtered_fngu['Date'], y=filtered_fngu['Adj Close'], name='Original Data'))
                    FNGU_fig.update_layout(xaxis_title='Date', yaxis_title='Adj Close', title='FNGU Plot')
                    FNGU_fig.write_html('FNGU_plot.html')

                    # Create a table using Plotly for FNGU data
                    table_FNGU_fig = go.Figure(data=[go.Table(header=dict(values=filtered_fngu.columns),
                                                               cells=dict(values=[filtered_fngu[col] for col in filtered_fngu.columns]))])
                    table_FNGU_fig.write_html('FNGU_table.html')

                    # Append the FNGU plot and table to the combined HTML
                    with open('FNGU_plot.html', 'r', encoding='utf-8') as plot_file:
                        combined_file.write('<h2>FNGU Plot</h2>')
                        combined_file.write(plot_file.read())
                    with open('FNGU_table.html', 'r', encoding='utf-8') as table_file:
                        combined_file.write('<h2>FNGU Table</h2>')
                        combined_file.write(table_file.read())

                elif user_input.lower() == 'fngd':
                    # Ask the user for the start and end dates
                    start_date = input("Please enter the start date (YYYY-MM-DD): ")
                    end_date = input("Please enter the end date (YYYY-MM-DD): ")

                    # Filter the FNGD data based on the start and end dates
                    filtered_fngd = fngd[(fngd['Date'] >= start_date) & (fngd['Date'] <= end_date)]

                    # Generate the FNGD plot using Plotly
                    FNGD_fig = go.Figure()
                    FNGD_fig.add_trace(go.Scatter(x=filtered_fngd['Date'], y=filtered_fngd['Adj Close'], name='Original Data'))
                    FNGD_fig.update_layout(xaxis_title='Date', yaxis_title='Adj Close', title='FNGD Plot')
                    FNGD_fig.write_html('FNGD_plot.html')

                    # Create a table using Plotly for FNGD data
                    table_FNGD_fig = go.Figure(data=[go.Table(header=dict(values=filtered_fngd.columns),
                                                               cells=dict(values=[filtered_fngd[col] for col in filtered_fngd.columns]))])
                    table_FNGD_fig.write_html('FNGD_table.html')

                    # Append the FNGD plot and table to the combined HTML
                    with open('FNGD_plot.html', 'r', encoding='utf-8') as plot_file:
                        combined_file.write('<h2>FNGD Plot</h2>')
                        combined_file.write(plot_file.read())
                    with open('FNGD_table.html', 'r', encoding='utf-8') as table_file:
                        combined_file.write('<h2>FNGD Table</h2>')
                        combined_file.write(table_file.read())

            # Open the combined HTML automatically
            webbrowser.open('combined.html')

        return wrapper  



    return decorator_generate_combined_html


