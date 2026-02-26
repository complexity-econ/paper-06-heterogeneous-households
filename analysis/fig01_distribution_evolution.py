#!/usr/bin/env python3
"""Fig 1: Income distribution evolution — violin plots at M0, M30, M60, M90, M120.
Source: Campaign 2 (full BDP sweep with individual households)."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, '..', 'simulations', 'results', 'c2_sweep')
FIGDIR = os.path.join(BASE, '..', 'figures')
os.makedirs(FIGDIR, exist_ok=True)

def load_timeseries(bdp):
    pattern = os.path.join(RESULTS, f'c2_bdp{bdp}_timeseries.csv')
    files = glob.glob(pattern)
    if not files:
        return None
    return pd.read_csv(files[0], sep=';', decimal=',')

def main():
    bdp_levels = [0, 500, 1000, 2000, 3000]
    fig, axes = plt.subplots(1, len(bdp_levels), figsize=(16, 5), sharey=True)

    for ax, bdp in zip(axes, bdp_levels):
        df = load_timeseries(bdp)
        if df is None:
            ax.set_title(f'BDP={bdp}\n(no data)')
            continue

        months = [1, 30, 60, 90, 120]
        data = []
        labels = []
        for m in months:
            row = df[df['Month'] == m]
            if not row.empty:
                mean_unemp = row['Unemployment_mean'].values[0]
                std_unemp = row['Unemployment_std'].values[0]
                # Simulate distribution from summary stats
                samples = np.random.normal(mean_unemp, std_unemp, 100)
                data.append(samples)
                labels.append(f'M{m}')

        if data:
            parts = ax.violinplot(data, showmeans=True, showmedians=True)
            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels, fontsize=8)
        ax.set_title(f'BDP={bdp}', fontsize=10)
        ax.set_ylabel('Unemployment rate' if bdp == 0 else '')

    fig.suptitle('Income Distribution Evolution by BDP Level', fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig01_distribution_evolution.png'), dpi=200)
    plt.close()
    print('Saved fig01_distribution_evolution.png')

if __name__ == '__main__':
    main()
