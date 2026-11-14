# Hard-MPI Veto — Project Status

Updated: 2026-11-14

## Research question

Investigate the effect of secondary hard multiple-parton
interactions in Herwig and the consequences of vetoing MPI
whose matrix-element scale exceeds the primary hard process.

The veto condition studied is:

    mpiMEScale > primaryMEScale

## Completed or available

- Herwig hard-MPI veto implementation investigated.
- ON and OFF source snapshots preserved.
- Common source base commit identified.
- ON/OFF source differences inspected.
- Existing jet comparison plots collected locally.
- POWHEG + Herwig production scripts saved for three samples:
  MPI OFF, MPI ON with veto OFF, and MPI ON with veto ON.
- Local Git repository synchronized with GitHub.

## Important files

- `README.md`
- `docs/current_status.md`
- `production/powheg_herwig_1M/README.md`
- `code/herwig_snapshots/hard_mpi_veto_20261114/`
- `code/analysis/`
- `configs/`

Historical source versions and MPI parameter scans are retained
locally in `archive/`, which is excluded from Git in this clone.

## Current limitations

- Correspondence between saved sources and active CERN builds
  has not been fully established.
- Identical input LHE events and seeds do not guarantee
  event-by-event RNG synchronization.
- Existing jet plots still need a consolidated interpretation.
- The saved scripts depend on CERN software and data paths.

## Next research steps

1. Identify the exact Herwig installations and configurations
   used for each production sample.
2. Validate event correspondence and RNG behavior.
3. Compare jet observables between the three POWHEG+Herwig
   production variants.
4. Summarize statistical and systematic limitations.
5. Agree on the final analysis and publication scope
   with supervisors.

## GitHub

Repository:
https://github.com/matildamarjamaki/hard-mpi-veto

Branch: `main`
Saved commit: `36cb88b`

The source-code archive is not a fully validated standalone
Herwig build.
