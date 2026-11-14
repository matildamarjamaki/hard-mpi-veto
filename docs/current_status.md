# Current research status

Updated: 2026-11-14

## Completed or available

- Hard-MPI veto implementation investigated in Herwig.
- Earlier Herwig source modifications retained in the archive.
- ON/OFF source snapshots saved locally.
- Common base commit identified for the saved variants.
- Source differences between ON/OFF variants inspected.
- ACDC source files verified identical between variants.
- Existing jet comparison plots collected locally.

## Important observations

The ON variant contains the hard-MPI veto condition:

    mpiMEScale > primaryMEScale

The OFF variant disables this veto.

Other differences identified in the saved modified sources
are whitespace changes.

## Outstanding validation

- Verify correspondence between snapshots and active lxplus builds.
- Identify the exact configurations used for ON/OFF generation.
- Verify RNG alignment and event-by-event comparability.
- Document the interpretation of existing jet comparisons.
- Establish the next production and analysis steps with supervisors.

## Repository preparation

- Local directory structure established.
- Older Herwig update folders archived.
- Git repository initialized.
- GitHub repository initialized and synchronized with origin/main.
