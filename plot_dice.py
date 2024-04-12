import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde


# Function for custom violin-box plot
def violin_plot(ax, data, pos, bp=False, colors=None, labels=None):
    '''
    Create violin plots on an axis with optional box plots.
    https://pyinsci.blogspot.com/2009/09/violin-plot-with-matplotlib.html
    '''
    dist = max(pos)-min(pos)
    w = min(0.4*max(dist, 1.0), 0.5)
    for d, p, color in zip(data, pos, colors):
        k = gaussian_kde(d)  # Calculates the kernel density
        m = k.dataset.min()  # Lower bound of violin
        M = k.dataset.max()  # Upper bound of violin
        x = np.arange(m, M, (M-m)/100.)  # Support for violin
        v = k.evaluate(x)  # Violin profile (density curve)
        v = v/v.max()*w  # Scaling the violin to the available space
        ax.fill_betweenx(x, p, v+p, facecolor=color, alpha=0.3)
        ax.fill_betweenx(x, p, -v+p, facecolor=color, alpha=0.3)
    if bp:
        box = ax.boxplot(data, notch=1, positions=pos, vert=1)
        for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
            plt.setp(box[item], color='black')
    if labels:
        ax.set_xticks(pos)
        ax.set_xticklabels(labels, fontsize=18)
        ax.set_ylabel('Dice', fontsize=18, color='black')
        ax.set_ylim([0, 1])
        ax.tick_params(axis='y', labelsize=18)


# Data
jf_results = pd.read_csv('results/jianfei_dice.csv')
ts_results = pd.read_csv('results/TS_dice.csv')

jf_fat = jf_results['dice_fat']
jf_mus = jf_results['dice_muscle']
ts_fat = ts_results['dice_fat']
ts_mus = ts_results['dice_muscle']

# Create figure
fig = plt.figure(figsize=(6, 6), tight_layout=True)

# First subplot
ax1 = fig.add_subplot(111)
violin_plot(ax1, [jf_fat, ts_fat], [1, 2], bp=True,
            colors=['blue', 'green'],
            labels=['Internal', 'TotalSegmentator'])
ax1.set_title('Comparison of Subcutaneous Fat', fontsize=18, color='black')

fig.text(0.56, 0.4, 'p < 0.001', ha='center', va='center', fontsize=16, color='black')


# plt.grid()
plt.show()
fig.savefig('boxPlot_fat.pdf')
# a=1
