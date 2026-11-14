# MSc Thesis — Research Overview

Updated: 2026-11-14

## Research context

MSc research in experimental high-energy physics, connected to
the CMS experiment at CERN.

Three research workstreams are currently maintained:

1. Hard-MPI veto in Herwig.
2. Matrix-based non-perturbative corrections.
3. Low-pileup particle-flow candidate response.

The final MSc thesis scope and the relationship between these
workstreams remain to be agreed with supervisors.

## Project locations

### 1. Hard-MPI veto

Local:
`~/MSc_Thesis/01_Hard_MPI_Veto`

GitHub:
https://github.com/matildamarjamaki/hard-mpi-veto

Branch: `main`
Saved commit: `207c702`

Study: vetoing secondary MPI when its matrix-element scale
exceeds the primary hard-process scale.

### 2. Matrix-based NP corrections

Local:
`~/MSc_Thesis/02_Matrix_NP_Corrections`

GitHub:
https://github.com/matildamarjamaki/matrix-np-corrections

Branch: `main`
Saved commit: `dd4c7e9`

Study: event-correlated NP ON/OFF simulations and migration
matrices for jet observables.

### 3. Low-PU PF candidate study

Local:
`~/MSc_Thesis/03_LowPU_PF`

GitHub:
https://github.com/matildamarjamaki/SPRLowPU

Snapshot branch: `thesis/lowpu-snapshot-2026`
Saved commit: `76bffe6`

Study: charged-hadron response, PFBlock/HCAL associations,
and V0-tagged particle-flow response in low-pileup CMS data.

## Research status

The three selected source-code collections are saved in GitHub.

This does not establish full reproducibility:
large event samples, ROOT results, CERN software environments,
and some dataset inventories remain outside Git.

Each project contains a PROJECT_STATUS.md file documenting
the current state and the next research steps.

## General next steps

1. Confirm the final thesis topic and scope with supervisors.
2. Complete reproducibility and validation checks for the
   selected analysis.
3. Document the physics interpretation of existing results.
4. Preserve important numerical results and dataset locations.
5. Develop the thesis outline and LaTeX writing environment.

## Recovery

If earlier conversations are unavailable:

1. Open this file.
2. Read the relevant project's README.md.
3. Read its PROJECT_STATUS.md.
4. Check the saved GitHub branch and latest commit.
5. Verify the CERN software environment and data availability
   before attempting to reproduce an analysis.

Do not assume that a clean Git checkout reproduces the original
CERN working environment without additional dependencies.
