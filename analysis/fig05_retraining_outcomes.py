#!/usr/bin/env python3
"""Fig 5: Retraining funnel — attempts → completions → re-employment.
Source: Campaign 5 (retraining policy sensitivity)."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, '..', 'simulations', 'results', 'c5_retraining')
FIGDIR = os.path.join(BASE, '..', 'figures')
os.makedirs(FIGDIR, exist_ok=True)

SUBDIR_PREFIX = {'none': 'c5_none', 'baseline': 'c5_base', 'enhanced': 'c5_enh'}

def load_hh_terminal(subdir, bdp):
    prefix = SUBDIR_PREFIX.get(subdir, f'c5_{subdir}')
    pattern = os.path.join(RESULTS, subdir, f'{prefix}_bdp{bdp}_hh_terminal.csv')
    files = glob.glob(pattern)
    if not files:
        return None
    return pd.read_csv(files[0], sep=';', decimal=',')

def main():
    configs = ['none', 'baseline', 'enhanced']
    config_labels = ['No retraining', 'Baseline', 'Enhanced']
    bdp = 2000

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(configs))
    width = 0.35

    attempts = []
    successes = []

    for cfg in configs:
        df = load_hh_terminal(cfg, bdp)
        if df is None:
            attempts.append(0)
            successes.append(0)
            continue
        attempts.append(df['RetrainingAttempts'].mean())
        successes.append(df['RetrainingSuccesses'].mean())

    ax.bar(x - width/2, attempts, width, label='Attempts', color='steelblue')
    ax.bar(x + width/2, successes, width, label='Successes', color='coral')
    ax.set_xticks(x)
    ax.set_xticklabels(config_labels)
    ax.set_ylabel('Count (mean across seeds)')
    ax.set_title(f'Retraining Funnel at BDP={bdp} PLN')
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig05_retraining_outcomes.png'), dpi=200)
    plt.close()
    print('Saved fig05_retraining_outcomes.png')

if __name__ == '__main__':
    main()
