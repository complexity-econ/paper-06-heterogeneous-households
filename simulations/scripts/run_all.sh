#!/bin/bash
# Paper 06: Run all 5 campaigns (~1,740 sims, ~8-9 hours at 100K HH)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=========================================="
echo "  Paper 06: Heterogeneous Households"
echo "  5 campaigns, ~1,740 total simulations"
echo "=========================================="

bash "${SCRIPT_DIR}/run_c1_validation.sh"
bash "${SCRIPT_DIR}/run_c2_sweep.sh"
bash "${SCRIPT_DIR}/run_c3_mpc.sh"
bash "${SCRIPT_DIR}/run_c4_wealth.sh"
bash "${SCRIPT_DIR}/run_c5_retraining.sh"

echo ""
echo "All Paper 06 campaigns complete."
