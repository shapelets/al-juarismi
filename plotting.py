import matplotlib.pyplot as plt


# This function plots a dataset.
def plotDataset(dataset):
    plt.plot(dataset['Fare'])
    plt.show()


def executePlot(currentDataset):
    """Show the result graphically of anything"""
    plotDataset(currentDataset)
