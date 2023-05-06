import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Create a DataFrame from the given dataset
    data = pd.DataFrame({
        'CI Config Admin Group': ['Config0002', 'Config0002', 'Config0002', 'Config0002'],
        'Compliance result ID': [5.0, 10.0, 2.0, 3.0],
        'Vulnerability ID': [64.0, 64.0, 64.0, 64.0],
        'Total Vulnerability ID': [9.0, 8.0, 12.0, 13.0],
        'Date': ['2023-05-06', '2023-05-07', '2023-05-08', '2023-05-09']
    })

    # Convert the 'Date' column to a datetime object
    data['Date'] = pd.to_datetime(data['Date'])

    # Set the 'Date' column as the index
    data.set_index('Date', inplace=True)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot each column separately as a line plot
    data['Compliance result ID'].plot(ax=ax, label='Compliance result ID')
    data['Vulnerability ID'].plot(ax=ax, label='Vulnerability ID')
    data['Total Vulnerability ID'].plot(ax=ax, label='Total Vulnerability ID')

    # Set the title, legend, and axis labels
    ax.set_title('Compliance and Vulnerability')
    ax.legend()
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')

    # Show the plot
    plt.show()
