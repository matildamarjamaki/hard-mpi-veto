#!/bin/bash
set -euo pipefail

INDEX="$1"
INDEX3=$(printf "%03d" "$INDEX")

export SCRAM_ARCH=el9_amd64_gcc12
source /cvmfs/cms.cern.ch/cmsset_default.sh

PLAIN="$HOME/herwig_plain_production/CMSSW_15_0_15_patch4/src"
BATCH="$HOME/condor_powheg_herwig_mpi_on_1M"

PROD="/eos/user/m/mmarjama/nanogen_study/herwig_modified/powheg_herwig_1M_1000x1000_20261026"
EOSOUT="/eos/user/m/mmarjama/nanogen_study/powheg_herwig_mpi_on_veto_on_1M"

cd "$PLAIN"
eval "$(scram runtime -sh)"

export HERWIGPP_BASE="/eos/user/m/mmarjama/nanogen_study/herwig_modified/powheg_herwig_1M_runtime/ON"
export HERWIGPATH="$HERWIGPP_BASE/share/Herwig"
export LD_LIBRARY_PATH="$HERWIGPP_BASE/lib/Herwig:$HERWIGPP_BASE/lib:${LD_LIBRARY_PATH:-}"


JOBDIR="${_CONDOR_SCRATCH_DIR:?Missing Condor scratch directory}"
cd "$JOBDIR"

INPUT="$PROD/lhe/powheg_dijet_${INDEX3}.lhe"
OUTPUT="mpi_on_veto_on_${INDEX3}.root"
NUMBERED="powheg_numbered_${INDEX3}.lhe"
CFG="mpi_on_veto_on_${INDEX3}_cfg.py"

echo "===== JOB ====="
echo "Index: $INDEX"
echo "Host: $(hostname)"
echo "Scratch: $JOBDIR"
echo "Input: $INPUT"

# Stage input locally.
cp "$INPUT" original.lhe

# Number events with globally unique IDs.
python3 "$BATCH/scripts/number_lhe.py" \
    --input original.lhe \
    --output "$NUMBERED" \
    --index "$INDEX" \
    --script "$PLAIN/GeneratorInterface/LHEInterface/scripts/addLHEnumbers.py"

# Generate job-specific CMSSW configuration.
python3 - "$BATCH/configs/mpi_on_veto_on_template_cfg.py" \
    "$CFG" "$NUMBERED" "$OUTPUT" "$INDEX" <<'PY'
import sys
from pathlib import Path

template, destination, lhe, output, index = sys.argv[1:]
text = Path(template).read_text()

assert text.count("__NUMBERED_LHE__") == 2
assert text.count("__OUTPUT_ROOT__") == 1
assert text.count("seed = cms.untracked.int32(12345)") == 1

text = text.replace("__NUMBERED_LHE__", str(Path(lhe).resolve()))
text = text.replace("__OUTPUT_ROOT__", output)

seed = 12345 + int(index)
text = text.replace(
    "seed = cms.untracked.int32(12345)",
    f"seed = cms.untracked.int32({seed})"
)

Path(destination).write_text(text)
print(f"Herwig seed: {seed}")
PY

python3 -m py_compile "$CFG"

# Save diagnostics if the job fails.
save_failure_log() {
    status=$?
    trap - EXIT
    if [ "$status" -ne 0 ]; then
        echo "Job $INDEX failed with exit code $status"
        if [ -f cmsrun.log ]; then
            mkdir -p "$EOSOUT/logs/failed"
            cp cmsrun.log                 "$EOSOUT/logs/failed/mpi_on_veto_on_${INDEX3}_cmsrun.log"                 || true
        fi
    fi
    exit "$status"
}
trap save_failure_log EXIT

echo "===== START CMSRUN ====="
cmsRun "$CFG" > cmsrun.log 2>&1

echo "===== VALIDATE OUTPUT ====="
test -s "$OUTPUT"

python3 - "$OUTPUT" "$INDEX" cmsrun.log <<'PY'
import re
import subprocess
import sys
from pathlib import Path

root_file = sys.argv[1]
index = int(sys.argv[2])
log_file = Path(sys.argv[3])

output = subprocess.check_output(
    ["edmFileUtil", "-e", root_file],
    text=True
)

match = re.search(r"\b(\d+)\s+events\b", output)
if not match:
    raise RuntimeError("Cannot determine ROOT event count")

count = int(match.group(1))

if count == 1000:
    print("Validated 1000 events")
elif count == 999:
    log = log_file.read_text(errors="replace")
    skipped = set(map(int, re.findall(
        r"Event\s+(\d+)\s+not generated", log
    )))

    expected_start = index * 1000 + 1
    expected_end = (index + 1) * 1000

    if len(skipped) != 1 or not all(
        expected_start <= event <= expected_end
        for event in skipped
    ):
        raise RuntimeError(
            f"999 events but unexpected skipped IDs: {skipped}"
        )

    print(f"Validated 999 events; skipped LHE event: {next(iter(skipped))}")
else:
    raise RuntimeError(f"Unexpected event count: {count}")
PY

DEST="$EOSOUT/root/$OUTPUT"

if [ -e "$DEST" ]; then
    echo "ERROR: Destination already exists: $DEST"
    exit 1
fi

echo "===== COPY OUTPUT TO EOS ====="
cp "$OUTPUT" "$DEST"

test -s "$DEST"

LOGDEST="$EOSOUT/logs/mpi_on_veto_on_${INDEX3}.log"

if [ -e "$LOGDEST" ]; then
    echo "ERROR: Log already exists: $LOGDEST"
    exit 1
fi

cp cmsrun.log "$LOGDEST"
test -s "$LOGDEST"

echo "===== COMPLETED ====="
echo "$DEST"
