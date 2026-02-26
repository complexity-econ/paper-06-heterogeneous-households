#!/bin/bash
# Campaign 5: Retraining policy sensitivity
# 3 retraining configs × 3 BDP levels × 30 seeds = 270 sims
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CORE_DIR="$(cd "${SCRIPT_DIR}/../../../core" && pwd)"
RESULTS_DIR="$(cd "${SCRIPT_DIR}/../results" && pwd)"
JAR="${CORE_DIR}/target/scala-3.5.2/sfc-abm.jar"
SEEDS=30

# No retraining: disabled
# Baseline: prob=0.15, cost=5000, duration=6
# Enhanced: prob=0.30, cost=2500, duration=3

if [[ ! -f "${JAR}" ]]; then
  echo "ERROR: JAR not found at ${JAR}. Run: cd ${CORE_DIR} && sbt assembly"
  exit 1
fi

cd "${CORE_DIR}"

for BDP in 0 500 2000; do
  prefix="c5_none_bdp${BDP}"
  echo "=== C5 Retraining none: BDP=${BDP} ==="
  HH_MODE=individual HH_RETRAIN_ENABLED=false \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c5_retraining/none/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c5_retraining/none/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c5_retraining/none/" 2>/dev/null || true

  prefix="c5_base_bdp${BDP}"
  echo "=== C5 Retraining baseline: BDP=${BDP} ==="
  HH_MODE=individual HH_RETRAIN_PROB=0.15 HH_RETRAIN_COST=5000 HH_RETRAIN_DUR=6 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c5_retraining/baseline/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c5_retraining/baseline/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c5_retraining/baseline/" 2>/dev/null || true

  prefix="c5_enh_bdp${BDP}"
  echo "=== C5 Retraining enhanced: BDP=${BDP} ==="
  HH_MODE=individual HH_RETRAIN_PROB=0.30 HH_RETRAIN_COST=2500 HH_RETRAIN_DUR=3 \
    java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c5_retraining/enhanced/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c5_retraining/enhanced/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c5_retraining/enhanced/" 2>/dev/null || true
done

echo "Campaign 5 complete."
