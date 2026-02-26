#!/bin/bash
# Campaign 2: Full BDP sweep with individual households
# 21 BDP levels × 30 seeds = 630 sims
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

for BDP in 0 250 500 750 1000 1250 1500 1750 2000 2250 2500 2750 3000 3250 3500 3750 4000 4250 4500 4750 5000; do
  prefix="c2_bdp${BDP}"
  echo "=== C2 Sweep: BDP=${BDP} ==="
  HH_MODE=individual java -jar "$JAR" "$BDP" "$SEEDS" "$prefix" pln > /dev/null 2>&1
  mv "mc/${prefix}_terminal.csv" "${RESULTS_DIR}/c2_sweep/"
  mv "mc/${prefix}_timeseries.csv" "${RESULTS_DIR}/c2_sweep/"
  mv "mc/${prefix}_hh_terminal.csv" "${RESULTS_DIR}/c2_sweep/" 2>/dev/null || true
done

echo "Campaign 2 complete."
