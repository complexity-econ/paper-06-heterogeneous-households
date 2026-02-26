#!/usr/bin/env python3
"""Fig 3: Gini decomposition — within-group vs between-group vs aggregate.
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
    bdp_levels = list(range(0, 5250, 250))
    fig, ax = plt.subplots(figsize=(10, 6))

    gini_income = []
    gini_wealth = []
    bdps_found = []

    for bdp in bdp_levels:
        df = load_hh_terminal(bdp)
        if df is None:
            continue
        bdps_found.append(bdp)
        gini_income.append(df['Gini_Individual'].mean())
        gini_wealth.append(df['Gini_Wealth'].mean())

    if bdps_found:
        ax.plot(bdps_found, gini_income, 'o-', label='Gini (income)', color='steelblue')
        ax.plot(bdps_found, gini_wealth, 's-', label='Gini (wealth)', color='coral')
        ax.set_xlabel('BDP (PLN/month)')
        ax.set_ylabel('Gini coefficient')
        ax.legend()
        ax.set_title('Gini Decomposition: Income vs Wealth Inequality')
        ax.set_ylim(0, 1)
    else:
        ax.text(0.5, 0.5, 'No data available', transform=ax.transAxes, ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig03_gini_decomposition.png'), dpi=200)
    plt.close()
    print('Saved fig03_gini_decomposition.png')

if __name__ == '__main__':
    main()
