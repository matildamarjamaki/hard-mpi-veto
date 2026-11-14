# POWHEG + Herwig production (1M-event study)

This directory contains selected production scripts and CMSSW
configuration templates for the three POWHEG + Herwig samples
used in the Hard-MPI veto study.

## Samples

| Sample | MPI | Hard-MPI veto |
|---|---|---|
| `powheg_herwig_mpi_off_1M` | OFF | Not applicable |
| `powheg_herwig_mpi_on_veto_off_1M` | ON | OFF |
| `powheg_herwig_mpi_on_veto_on_1M` | ON | ON |

All three production scripts use LHE input files from the same
POWHEG dijet production and assign job-dependent Herwig seeds:

    seed = 12345 + job_index

Each job requests 1000 input events.

## Configuration differences

The MPI OFF configuration explicitly disables MPI using:

    set /Herwig/Shower/ShowerHandler:MPIHandler NULL

The two MPI ON configuration templates are identical.
Their production scripts select different Herwig installations
through HERWIGPP_BASE:

- `OFF`: Herwig build without the Hard-MPI veto.
- `ON`: Herwig build with the Hard-MPI veto.

The corresponding Herwig source snapshots are stored separately
under `code/herwig_snapshots/`.

## Files

- `configs/`: Original CMSSW configuration templates.
- `scripts/run_job.sh`: MPI OFF production.
- `scripts/run_mpi_on_veto_off.sh`: MPI ON, veto OFF production.
- `scripts/run_mpi_on_veto_on.sh`: MPI ON, veto ON production.
- `scripts/number_lhe.py`: Shared LHE event-numbering helper.

## Reproducibility notes

The files are preserved with their original names and contents.
The production scripts contain CERN-specific paths and depend on
the original CMSSW environment, Herwig installations, POWHEG
LHE inputs, and CMSSW's addLHEnumbers.py helper.

Using the same LHE events and initial random seed does not
guarantee identical random-number consumption across different
Herwig configurations. Event-by-event RNG synchronization
remains a separate subject of investigation.

The large generated ROOT files, LHE inputs, runtime installations,
and batch logs are not included in this repository.
