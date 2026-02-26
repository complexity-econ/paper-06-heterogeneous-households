#!/bin/bash
# Campaign 4: Savings/debt sensitivity
# 3 wealth distributions × 3 BDP levels × 30 seeds = 270 sims
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CORE_DIR="$(cd "${SCRIPT_DIR}/../../../core" && pwd)"
RESULTS_DIR="$(cd "${SCRIPT_DIR}/../results" && pwd)"
JAR="${CORE_DIR}/target/scala-3.5.2/sfc-abm.jar"
SEEDS=30

# Poor: LogNormal(8.5, 1.2) → median ~5K PLN
# Baseline: LogNormal(9.6, 1.2) → median ~15K PLN
# Rich: LogNormal(10.5, 1.2) → median ~36K PLN

if [[ ! -f "${JAR}" ]]; then
  echo "ERROR: JAR not found at ${JAR}. Run: cd ${CORE_DIR} && sbt assembly"
  exit 1
fi

cd "${CORE_DIR}"

for BDP in 0 500 2000; do
  prefix="c4_poor_bdp${BDP}"
  echo "=== C4 Wealth poor: BDP=${BDP} ==="
  HH_MODE=individual HH_SAVINGS_MU=8.5 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c4_wealth/poor/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c4_wealth/poor/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c4_wealth/poor/" 2>/dev/null || true

  prefix="c4_base_bdp${BDP}"
  echo "=== C4 Wealth baseline: BDP=${BDP} ==="
  HH_MODE=individual HH_SAVINGS_MU=9.6 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c4_wealth/baseline/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c4_wealth/baseline/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c4_wealth/baseline/" 2>/dev/null || true

  prefix="c4_rich_bdp${BDP}"
  echo "=== C4 Wealth rich: BDP=${BDP} ==="
  HH_MODE=individual HH_SAVINGS_MU=10.5 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c4_wealth/rich/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c4_wealth/rich/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c4_wealth/rich/" 2>/dev/null || true
done

echo "Campaign 4 complete."
