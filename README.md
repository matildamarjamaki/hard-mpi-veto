# Hard-MPI veto study

Study of hard multiple-parton interactions (MPI) in Herwig,
with emphasis on the effect of vetoing secondary interactions
whose matrix-element scale exceeds that of the primary hard process.

## Research objectives

- Investigate the hard-MPI veto implementation in Herwig.
- Compare event generation with the veto enabled and disabled.
- Study random-number-generator (RNG) control and event-level
  comparability.
- Evaluate effects on jet observables and nonperturbative corrections.

## Repository structure

- `code/analysis/`: analysis and plotting scripts.
- `code/herwig_snapshots/`: saved Herwig source modifications.
- `configs/`: event-generation and analysis configurations.
- `docs/`: methodology, progress and reproducibility notes.
- `plots/`: locally retained analysis figures.
- `results/`: small numerical results and summaries.
- `archive/`: earlier implementations and supporting material.

## Saved Herwig versions

Snapshot: `code/herwig_snapshots/hard_mpi_veto_20261114/`

Base commit:

`6ae1bc21651e451bd4b2ef8a13446d4fe8ccac5c`

The snapshot contains ON and OFF variants with saved source
files, patches, Git metadata and SHA256 manifests.

The observed functional source difference between the variants
is the hard-MPI veto condition in `ShowerHandler.cc`.
Additional differences in three other source files are whitespace only.

## Validation status

The saved source variants have been compared locally.

Event-by-event reproducibility, RNG-state alignment and
correspondence with the active lxplus builds remain to be verified.

## Data policy

Large event samples and ROOT files are not stored in Git.
They remain in the appropriate CERN storage locations.
