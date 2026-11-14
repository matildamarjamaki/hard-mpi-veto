from pathlib import Path

BASE = Path("/eos/user/m/mmarjama/nanogen_study")

OFF = BASE / "powheg_herwig_mpi_on_veto_off_1M/logs"
ON = BASE / "powheg_herwig_mpi_on_veto_on_1M/logs"


def read_events(path):
    events = {}
    current = None

    with path.open(errors="replace") as f:
        for line in f:
            fields = line.split()

            if not fields:
                continue

            if fields[0] == "RNG_EVENT_SEED":
                current = int(fields[1])
                events[current] = {
                    "seed": fields[2],
                    "vetoes": 0,
                    "attempts": [],
                }

            elif current is not None:
                if fields[0] == "HARD_MPI_VETO":
                    events[current]["vetoes"] += 1

                elif fields[0] == "RNG_MPI_ATTEMPT_KIN":
                    # Compare the full attempted MPI kinematics.
                    events[current]["attempts"].append(
                        tuple(fields[4:])
                    )

    return events


for index in range(10):
    off_path = OFF / f"mpi_on_veto_off_{index:03d}.log"
    on_path = ON / f"mpi_on_veto_on_{index:03d}.log"

    off = read_events(off_path)
    on = read_events(on_path)

    first_veto = None
    first_difference = None

    for event_id in sorted(off.keys() & on.keys()):
        a = off[event_id]
        b = on[event_id]

        if a["seed"] != b["seed"]:
            print("SEED MISMATCH:", index, event_id)
            break

        if b["vetoes"] > 0 and first_veto is None:
            first_veto = event_id

        if a["attempts"] != b["attempts"]:
            first_difference = event_id
            break

    print(
        f"file={index:03d}",
        f"first_veto={first_veto}",
        f"first_MPI_difference={first_difference}",
    )
