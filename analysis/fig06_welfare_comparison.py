#!/usr/bin/env python3
"""Fig 6: Welfare — individual Gini vs aggregate Gini vs poverty rate.
Source: Campaign 2 + Campaign 3."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS_C2 = os.path.join(BASE, '..', 'simulations', 'results', 'c2_sweep')
FIGDIR = os.path.join(BASE, '..', 'figures')
os.makedirs(FIGDIR, exist_ok=True)

def load_hh_terminal(path, bdp):
    pattern = os.path.join(path, f'c2_bdp{bdp}_hh_terminal.csv')
    files = glob.glob(pattern)
    if not files:
        return None
    return pd.read_csv(files[0], sep=';', decimal=',')

def main():
    bdp_levels = list(range(0, 5250, 250))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    gini_vals = []
    poverty_vals = []
    bdps_found = []

    for bdp in bdp_levels:
        df = load_hh_terminal(RESULTS_C2, bdp)
        if df is None:
            continue
        bdps_found.append(bdp)
        gini_vals.append(df['Gini_Individual'].mean())
        poverty_vals.append(df['PovertyRate_50pct'].mean())

    if bdps_found:
        ax1.plot(bdps_found, gini_vals, 'o-', color='steelblue')
        ax1.set_xlabel('BDP (PLN/month)')
        ax1.set_ylabel('Gini (income)')
        ax1.set_title('Income Gini by BDP')

        ax2.plot(bdps_found, [p * 100 for p in poverty_vals], 's-', color='coral')
        ax2.set_xlabel('BDP (PLN/month)')
        ax2.set_ylabel('Poverty rate (%)')
        ax2.set_title('Poverty Rate (50% median) by BDP')
    else:
        ax1.text(0.5, 0.5, 'No data', transform=ax1.transAxes, ha='center')
        ax2.text(0.5, 0.5, 'No data', transform=ax2.transAxes, ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig06_welfare_comparison.png'), dpi=200)
    plt.close()
    print('Saved fig06_welfare_comparison.png')

if __name__ == '__main__':
    main()
