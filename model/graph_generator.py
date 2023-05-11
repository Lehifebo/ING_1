import pandas as pd
import matplotlib.pyplot as plt


class GraphGenerator:
    def __init__(self, maybe_path):
        self.maybe_path = maybe_path

    def team_graph(self):
        # pathing needs to be fixed
        data = pd.read_csv("../historical_data/Config0001_data.csv")

        # Convert the 'Date' column to a datetime object
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.strftime('%m-%d')
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

    def get_data_tuples(self):
        datasets = []
        for x in range(1, 11):
            config_name = "Config{:04d}".format(x)
            historical_data = pd.read_csv("../historical_data/" + config_name + "_data.csv")
            historical_data['Date'] = pd.to_datetime(historical_data['Date'])
            historical_data.set_index('Date', inplace=True)
            datasets.append((config_name, historical_data))
        return datasets

    def issue_graph(self):
        datasets = self.get_data_tuples()
        for config, data in datasets:
            # plot the 'y' column from both dataframes on the same graph
            plt.plot(data['Date'], data['Vulnerability ID'], label=config)

        # add labels and legend
        plt.xlabel('Date')
        plt.ylabel('Overdue Vulnerabilities')
        plt.legend()

        # show the graph
        plt.show()

#if __name__ == "__main__":
#    issue_graph()
