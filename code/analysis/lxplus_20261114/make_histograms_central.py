import ROOT
from pathlib import Path
from array import array
from DataFormats.FWLite import Events, Handle

ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libFWCoreFWLite")
ROOT.FWLiteEnabler.enable()
ROOT.TH1.SetDefaultSumw2(True)

BASE = Path("/eos/user/m/mmarjama/nanogen_study")
NFILES = 1000

samples = {
    "MPI_OFF": (
        BASE / "powheg_herwig_mpi_off_1M/root",
        "mpi_off",
    ),
    "VETO_OFF": (
        BASE / "powheg_herwig_mpi_on_veto_off_1M/root",
        "mpi_on_veto_off",
    ),
    "VETO_ON": (
        BASE / "powheg_herwig_mpi_on_veto_on_1M/root",
        "mpi_on_veto_on",
    ),
}

output = ROOT.TFile(
    "leading_ak4_central_histograms.root", "RECREATE"
)

bins = array("d", [
    30, 35, 40, 45, 50, 60, 70, 80, 90,
    100, 120, 140, 170, 200, 220, 250,
    300, 350, 400
])

for name, (directory, prefix) in samples.items():
    hist = ROOT.TH1D(
        f"h_{name}",
        f"{name};Leading central AK4 GenJet p_{{T}} [GeV];Weighted events",
        len(bins) - 1, bins,
    )

    n_events = 0
    n_selected = 0
    sumw = 0.0
    sumw2 = 0.0
    n_negative = 0

    for index in range(NFILES):
        path = directory / f"{prefix}_{index:03d}.root"

        if not path.is_file():
            raise FileNotFoundError(path)

        events = Events(str(path))
        jets = Handle("std::vector<reco::GenJet>")
        gen = Handle("GenEventInfoProduct")

        for event in events:
            event.getByLabel(("ak4GenJets", "", "GEN"), jets)
            event.getByLabel(("generator", "", "GEN"), gen)

            if not jets.isValid() or not gen.isValid():
                raise RuntimeError(f"Missing products in {path}")

            weight = float(gen.product().weight())

            n_events += 1
            sumw += weight
            sumw2 += weight * weight

            if weight < 0:
                n_negative += 1

            selected_pts = [
                jet.pt()
                for jet in jets.product()
                if abs(jet.eta()) < 0.5
            ]

            if selected_pts:
                leading_pt = max(selected_pts)
                hist.Fill(leading_pt, weight)

                if 30 <= leading_pt < 400:
                    n_selected += 1

        if (index + 1) % 100 == 0:
            print(
                f"{name}: {index + 1}/{NFILES} files, "
                f"{n_events} events",
                flush=True,
            )

    output.cd()
    hist.Write()

    ROOT.TParameter("double")(
        f"sumw_{name}", sumw
    ).Write()

    ROOT.TParameter("double")(
        f"sumw2_{name}", sumw2
    ).Write()

    print(f"\n===== {name} =====")
    print(f"Events: {n_events}")
    print(f"Selected: {n_selected}")
    print(f"Sum weights: {sumw:.12g}")
    print(f"Sum weights squared: {sumw2:.12g}")
    print(f"Negative weights: {n_negative}", flush=True)

output.Close()
print("\nSaved leading_ak4_central_histograms.root")
