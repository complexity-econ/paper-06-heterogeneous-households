#!/bin/bash
# Campaign 3: MPC heterogeneity sensitivity
# 3 MPC distributions × 3 BDP levels × 30 seeds = 270 sims
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CORE_DIR="$(cd "${SCRIPT_DIR}/../../../core" && pwd)"
RESULTS_DIR="$(cd "${SCRIPT_DIR}/../results" && pwd)"
JAR="${CORE_DIR}/target/scala-3.5.2/sfc-abm.jar"
SEEDS=30

# Low variance: Beta(16, 3.5) → mean ~0.82, tight
# Baseline: Beta(8.2, 1.8) → mean ~0.82, moderate spread
# High variance: Beta(3, 0.7) → mean ~0.81, wide spread

if [[ ! -f "${JAR}" ]]; then
  echo "ERROR: JAR not found at ${JAR}. Run: cd ${CORE_DIR} && sbt assembly"
  exit 1
fi

cd "${CORE_DIR}"

for BDP in 0 500 2000; do
  prefix="c3_low_bdp${BDP}"
  echo "=== C3 MPC low-var: BDP=${BDP} ==="
  HH_MODE=individual HH_MPC_ALPHA=16 HH_MPC_BETA=3.5 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c3_mpc/low_var/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c3_mpc/low_var/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c3_mpc/low_var/" 2>/dev/null || true

  prefix="c3_base_bdp${BDP}"
  echo "=== C3 MPC baseline: BDP=${BDP} ==="
  HH_MODE=individual HH_MPC_ALPHA=8.2 HH_MPC_BETA=1.8 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c3_mpc/baseline/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c3_mpc/baseline/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c3_mpc/baseline/" 2>/dev/null || true

  prefix="c3_high_bdp${BDP}"
  echo "=== C3 MPC high-var: BDP=${BDP} ==="
  HH_MODE=individual HH_MPC_ALPHA=3 HH_MPC_BETA=0.7 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c3_mpc/high_var/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c3_mpc/high_var/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c3_mpc/high_var/" 2>/dev/null || true
done

echo "Campaign 3 complete."
