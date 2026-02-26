#!/usr/bin/env python3
"""Fig 2: Savings trajectories by quintile (spaghetti + median band).
Source: Campaign 2 (_hh_terminal.csv)."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, '..', 'simulations', 'results', 'c2_sweep')
FIGDIR = os.path.join(BASE, '..', 'figures')
os.makedirs(FIGDIR, exist_ok=True)

def load_hh_terminal(bdp):
    pattern = os.path.join(RESULTS, f'c2_bdp{bdp}_hh_terminal.csv')
    files = glob.glob(pattern)
    if not files:
        return None
    return pd.read_csv(files[0], sep=';', decimal=',')

def main():
    bdp_levels = [0, 500, 1000, 2000, 3000, 5000]
    fig, ax = plt.subplots(figsize=(10, 6))

    mean_savings = []
    median_savings = []
    bdps_found = []

    for bdp in bdp_levels:
        df = load_hh_terminal(bdp)
        if df is None:
            continue
        bdps_found.append(bdp)
        mean_savings.append(df['MeanSavings'].mean())
        median_savings.append(df['MedianSavings'].mean())

    if bdps_found:
        ax.plot(bdps_found, mean_savings, 'o-', label='Mean savings', color='steelblue')
        ax.plot(bdps_found, median_savings, 's--', label='Median savings', color='coral')
        ax.fill_between(bdps_found, median_savings, mean_savings, alpha=0.15, color='gray')
        ax.set_xlabel('BDP (PLN/month)')
        ax.set_ylabel('Terminal savings (PLN)')
        ax.legend()
        ax.set_title('Terminal Household Savings by BDP Level')
    else:
        ax.text(0.5, 0.5, 'No data available', transform=ax.transAxes, ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig02_savings_trajectories.png'), dpi=200)
    plt.close()
    print('Saved fig02_savings_trajectories.png')

if __name__ == '__main__':
    main()
