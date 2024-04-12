import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Data
data = pd.read_csv('results/vol_calc.csv')
data1 = data['GT_muscle_vol']
data2 = data['JF_muscle_vol']

# Calculate differences and means
differences = data1 - data2
means = (data1 + data2) / 2

# Calculate mean difference and limits of agreement
mean_difference = np.mean(differences)
std_difference = np.std(differences)
upper_limit = mean_difference + 1.96 * std_difference
lower_limit = mean_difference - 1.96 * std_difference

# Set global text size
matplotlib.rcParams.update({'font.size': 14})  # Adjust the 14 to your desired text size

# Create the Bland-Altman plot
plt.figure(figsize=(5, 5), tight_layout=True)
plt.scatter(means, differences, s=4, color='dimgrey', alpha=0.8)
plt.axhline(mean_difference, color='black', linestyle='--', label='Mean difference')
plt.axhline(upper_limit, color='red', linestyle='--', label='Upper limit of agreement')
plt.axhline(lower_limit, color='red', linestyle='--', label='Lower limit of agreement')

plt.title('Muscle Volume \nGround Truth vs Internal Tool')
plt.xlabel('Volume Averages (cm$^3$)')
plt.ylabel('Volume Differences (cm$^3$)')
# plt.legend()
plt.grid()
plt.savefig('BA_JF_muscle_vol.pdf')
plt.show()
