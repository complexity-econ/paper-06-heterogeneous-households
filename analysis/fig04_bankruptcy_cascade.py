#!/usr/bin/env python3
"""Fig 4: Bankruptcy cascade — cumulative bankruptcy rate over time by BDP level.
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

    colors = plt.cm.viridis(np.linspace(0, 1, len(bdp_levels)))
    for bdp, color in zip(bdp_levels, colors):
        df = load_hh_terminal(bdp)
        if df is None:
            continue
        mean_rate = df['BankruptcyRate'].mean()
        std_rate = df['BankruptcyRate'].std()
        ax.bar(str(bdp), mean_rate * 100, yerr=std_rate * 100,
               color=color, capsize=5, edgecolor='black', linewidth=0.5)

    ax.set_xlabel('BDP (PLN/month)')
    ax.set_ylabel('Bankruptcy rate at M120 (%)')
    ax.set_title('Household Bankruptcy Rate by BDP Level')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig04_bankruptcy_cascade.png'), dpi=200)
    plt.close()
    print('Saved fig04_bankruptcy_cascade.png')

if __name__ == '__main__':
    main()
