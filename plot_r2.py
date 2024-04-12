import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib

# Data
data = pd.read_csv('results/vol_calc.csv')
x = data['GT_sub_fat_vol']
y = data['TS_sub_fat_vol']

# Calculate line of best fit
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# Predicted values
y_pred = intercept + slope * x

# Set global text size
matplotlib.rcParams.update({'font.size': 14})  # Adjust the 14 to your desired text size

# Creating the figure with a square plot area
plt.figure(figsize=(5, 5), tight_layout=True)  # Adjust figure size as needed to make it visually square

# Plot scatter graph
plt.scatter(x, y, s=4, color='dimgrey')

# Line equation label
line_eq_label = f'y = {slope:.2f}x + {intercept:.2f}'

# Plot line of best fit with its equation as label
plt.plot(x, y_pred, color='darkblue', label=line_eq_label)

# Confidence interval calculations
# Adjusted to account for distribution of x values
# ci = 1.96 * std_err * np.sqrt(1/len(x) + (x - np.mean(x))**2 / np.sum((x - np.mean(x))**2))
# plt.fill_between(x, y_pred - ci, y_pred + ci, color='blue', alpha=0.2, label='95% CI')

# Calculate and add R^2 value to the legend
# It's added after the CI for desired legend order
r_squared = r_value ** 2
plt.plot([], [], ' ', label=f'$R^2 = {r_squared:.3f}$')  # Placeholder for R^2 in legend

plt.title('TotalSegmentator \nSubcutaneous Fat Volume')
plt.xlabel('Ground Truth Volume (cm$^3$)')
plt.ylabel('Measured Volume (cm$^3$)')
plt.legend(framealpha=0.5)
plt.grid()
plt.savefig('R2_TS_sub_fat_vol.pdf')
plt.show()
