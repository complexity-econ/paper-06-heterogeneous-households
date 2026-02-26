#!/bin/bash
# Campaign 1: Baseline comparison — aggregate vs individual mode
# 5 BDP levels × 2 modes × 30 seeds = 300 sims
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CORE_DIR="$(cd "${SCRIPT_DIR}/../../../core" && pwd)"
RESULTS_DIR="$(cd "${SCRIPT_DIR}/../results" && pwd)"
JAR="${CORE_DIR}/target/scala-3.5.2/sfc-abm.jar"
SEEDS=30

if [[ ! -f "${JAR}" ]]; then
  echo "ERROR: JAR not found at ${JAR}. Run: cd ${CORE_DIR} && sbt assembly"
  exit 1
fi

cd "${CORE_DIR}"

for BDP in 0 500 1000 2000 3000; do
  prefix="c1_agg_bdp${BDP}"
  echo "=== C1 Validation: BDP=${BDP}, HH_MODE=aggregate ==="
  HH_MODE=aggregate java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c1_validation/agg/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c1_validation/agg/"

  prefix="c1_ind_bdp${BDP}"
  echo "=== C1 Validation: BDP=${BDP}, HH_MODE=individual ==="
  HH_MODE=individual java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c1_validation/ind/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c1_validation/ind/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c1_validation/ind/" 2>/dev/null || true
done

echo "Campaign 1 complete."
