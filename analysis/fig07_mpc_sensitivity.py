#!/usr/bin/env python3
"""Fig 7: MPC sensitivity — consumption distribution under 3 MPC regimes.
Source: Campaign 3."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, '..', 'simulations', 'results', 'c3_mpc')
FIGDIR = os.path.join(BASE, '..', 'figures')
os.makedirs(FIGDIR, exist_ok=True)

SUBDIR_PREFIX = {'low_var': 'c3_low', 'baseline': 'c3_base', 'high_var': 'c3_high'}

def load_hh_terminal(subdir, bdp):
    prefix = SUBDIR_PREFIX.get(subdir, f'c3_{subdir}')
    pattern = os.path.join(RESULTS, subdir, f'{prefix}_bdp{bdp}_hh_terminal.csv')
    files = glob.glob(pattern)
    if not files:
        return None
    return pd.read_csv(files[0], sep=';', decimal=',')

def main():
    configs = ['low_var', 'baseline', 'high_var']
    config_labels = [r'Low var ($\alpha$=16)', r'Baseline ($\alpha$=8.2)', r'High var ($\alpha$=3)']
    bdp = 2000

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for ax, cfg, label in zip(axes, configs, config_labels):
        df = load_hh_terminal(cfg, bdp)
        if df is None:
            ax.set_title(f'{label}\n(no data)')
            continue

        p10 = df['ConsumptionP10'].values
        p50 = df['ConsumptionP50'].values
        p90 = df['ConsumptionP90'].values

        seeds = range(1, len(p10) + 1)
        ax.fill_between(seeds, p10, p90, alpha=0.3, color='steelblue')
        ax.plot(seeds, p50, '-', color='steelblue', label='Median')
        ax.set_xlabel('Seed')
        ax.set_title(label)
        if cfg == 'low_var':
            ax.set_ylabel('Consumption (PLN)')

    fig.suptitle(f'Consumption Distribution by MPC Regime (BDP={bdp})', fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig07_mpc_sensitivity.png'), dpi=200)
    plt.close()
    print('Saved fig07_mpc_sensitivity.png')

if __name__ == '__main__':
    main()
