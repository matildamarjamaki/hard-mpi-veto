from pathlib import Path
from collections import Counter
import math
import re
import csv

LOGDIR = Path(
    "/eos/user/m/mmarjama/nanogen_study/"
    "powheg_herwig_mpi_on_veto_on_1M/logs"
)

pattern = re.compile(
    r"HARD_MPI_VETO\s+"
    r"primaryScale2=([0-9.eE+-]+)\s+"
    r"mpiScale2=([0-9.eE+-]+)\s+"
    r"mpiIndex=(\d+)"
)

total = 0
violations = 0
files_with_veto = 0
indices = Counter()
ratios = []
primary_scales = []
mpi_scales = []
examples = []

logs = sorted(LOGDIR.glob("*.log"))

for number, path in enumerate(logs, 1):
    file_vetos = 0

    with path.open(errors="replace") as f:
        for line in f:
            if not line.startswith("HARD_MPI_VETO "):
                continue

            match = pattern.search(line)

            if not match:
                raise ValueError(
                    f"Unrecognized veto line in {path}: {line}"
                )

            primary2 = float(match.group(1))
            mpi2 = float(match.group(2))
            index = int(match.group(3))

            total += 1
            file_vetos += 1
            indices[index] += 1

            if not mpi2 > primary2:
                violations += 1
                if len(examples) < 10:
                    examples.append((path.name, line.strip()))

            if primary2 > 0 and mpi2 >= 0:
                ratios.append(math.sqrt(mpi2 / primary2))

            if primary2 >= 0 and mpi2 >= 0:
                primary_scales.append(math.sqrt(primary2))
                mpi_scales.append(math.sqrt(mpi2))

    if file_vetos:
        files_with_veto += 1

    if number % 100 == 0:
        print(f"Processed {number}/{len(logs)} logs", flush=True)


def percentile(values, fraction):
    if not values:
        return None
    values = sorted(values)
    index = round((len(values) - 1) * fraction)
    return values[index]


print("\n===== HARD MPI VETO VALIDATION =====")
print("Log files:", len(logs))
print("Total vetoes:", total)
print("Files containing vetoes:", files_with_veto)
print("Scale-condition violations:", violations)

print("\n===== VETOED MPI SCALE (GeV) =====")
print("Minimum:", min(mpi_scales, default=None))
print("Median:", percentile(mpi_scales, 0.5))
print("90th percentile:", percentile(mpi_scales, 0.9))
print("99th percentile:", percentile(mpi_scales, 0.99))
print("Maximum:", max(mpi_scales, default=None))

print("\n===== MPI / PRIMARY SCALE RATIO =====")
print("Minimum:", min(ratios, default=None))
print("Median:", percentile(ratios, 0.5))
print("90th percentile:", percentile(ratios, 0.9))
print("Maximum:", max(ratios, default=None))

print("\n===== VETOES BY MPI INDEX =====")
for index, count in sorted(indices.items()):
    print(f"mpiIndex={index}: {count}")

print("\n===== CONDITION VIOLATION EXAMPLES =====")
for example in examples:
    print(*example)

with open("hard_mpi_veto_scales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["primary_scale_GeV",
                     "mpi_scale_GeV",
                     "mpi_over_primary"])
    writer.writerows(zip(primary_scales, mpi_scales, ratios))

print("\nSaved: hard_mpi_veto_scales.csv")
