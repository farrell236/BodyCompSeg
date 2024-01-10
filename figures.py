import matplotlib.pyplot as plt
import numpy as np

import pandas as pd


a=1


results1 = pd.read_csv('jianfei_dice.csv')
results2 = pd.read_csv('TS_dice.csv')

# Example data
data1 = results1['dice_fat']
data2 = results1['dice_muscle']
data3 = results2['dice_fat']
data4 = results2['dice_muscle']
data_to_plot = [data1, data2, data3, data4]

# Create a figure instance
plt.figure()

# Create a violin plot
plt.violinplot(data_to_plot)

# Customize the plot
plt.title('Results')
plt.ylabel('Dice')
plt.xlabel('Anatomy')
plt.xticks([1, 2, 3, 4], ['JF_fat', 'JF_muscle', 'TS_fat', 'TS_muscle'])

# Show the plot
plt.show()
