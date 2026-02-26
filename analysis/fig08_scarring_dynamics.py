#!/usr/bin/env python3
"""Fig 8: Scarring dynamics — skill + health penalty evolution by unemployment duration.
Source: Campaign 2."""

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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    skills = []
    health = []
    bdps_found = []

    for bdp in bdp_levels:
        df = load_hh_terminal(bdp)
        if df is None:
            continue
        bdps_found.append(bdp)
        skills.append(df['MeanSkill'].mean())
        health.append(df['MeanHealthPenalty'].mean())

    if bdps_found:
        ax1.plot(bdps_found, skills, 'o-', color='steelblue')
        ax1.set_xlabel('BDP (PLN/month)')
        ax1.set_ylabel('Mean skill')
        ax1.set_title('Mean Skill at M120')

        ax2.plot(bdps_found, health, 's-', color='coral')
        ax2.set_xlabel('BDP (PLN/month)')
        ax2.set_ylabel('Mean health penalty')
        ax2.set_title('Mean Health Penalty at M120')

        # Theoretical curves for comparison
        months_unemp = np.arange(0, 90)
        skill_decay = 0.7 * np.where(months_unemp >= 3,
            (1 - 0.02) ** (months_unemp - 3), 1.0)
        health_acc = np.where(months_unemp >= 3,
            np.minimum(0.50, 0.02 * (months_unemp - 3)), 0.0)

        ax_inset1 = ax1.inset_axes([0.55, 0.15, 0.4, 0.35])
        ax_inset1.plot(months_unemp, skill_decay, '-', color='gray', alpha=0.7)
        ax_inset1.set_xlabel('Months', fontsize=7)
        ax_inset1.set_ylabel('Skill', fontsize=7)
        ax_inset1.set_title('Theoretical decay', fontsize=7)
        ax_inset1.tick_params(labelsize=6)

        ax_inset2 = ax2.inset_axes([0.1, 0.55, 0.4, 0.35])
        ax_inset2.plot(months_unemp, health_acc, '-', color='gray', alpha=0.7)
        ax_inset2.set_xlabel('Months', fontsize=7)
        ax_inset2.set_ylabel('Penalty', fontsize=7)
        ax_inset2.set_title('Theoretical scarring', fontsize=7)
        ax_inset2.tick_params(labelsize=6)
    else:
        ax1.text(0.5, 0.5, 'No data', transform=ax1.transAxes, ha='center')
        ax2.text(0.5, 0.5, 'No data', transform=ax2.transAxes, ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'fig08_scarring_dynamics.png'), dpi=200)
    plt.close()
    print('Saved fig08_scarring_dynamics.png')

if __name__ == '__main__':
    main()
