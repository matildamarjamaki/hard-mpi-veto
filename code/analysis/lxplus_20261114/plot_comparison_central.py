import ROOT
import math

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

f = ROOT.TFile.Open("leading_ak4_central_histograms.root")
if not f or f.IsZombie():
    raise RuntimeError("Cannot open histogram file")

names = ["MPI_OFF", "VETO_OFF", "VETO_ON"]

sumw = {}
for name in names:
    parameter = f.Get(f"sumw_{name}")
    if not parameter:
        raise RuntimeError(f"Missing sumw for {name}")
    sumw[name] = float(parameter.GetVal())

h = {}
for name in names:
    source = f.Get(f"h_{name}")
    if not source:
        raise RuntimeError(f"Missing histogram: {name}")

    h[name] = source.Clone(f"normalized_{name}")
    h[name].SetDirectory(0)
    h[name].Scale(1.0 / sumw[name], "width")

f.Close()

colors = {
    "MPI_OFF": ROOT.kBlack,
    "VETO_OFF": ROOT.kBlue + 1,
    "VETO_ON": ROOT.kRed + 1,
}

labels = {
    "MPI_OFF": "MPI OFF",
    "VETO_OFF": "MPI ON, veto OFF",
    "VETO_ON": "MPI ON, veto ON",
}

canvas = ROOT.TCanvas("canvas", "", 900, 850)

top = ROOT.TPad("top", "", 0, 0.30, 1, 1)
bottom = ROOT.TPad("bottom", "", 0, 0, 1, 0.30)

top.SetBottomMargin(0.03)
top.SetLeftMargin(0.13)
top.SetRightMargin(0.05)
top.SetLogy()

bottom.SetTopMargin(0.03)
bottom.SetBottomMargin(0.35)
bottom.SetLeftMargin(0.13)
bottom.SetRightMargin(0.05)

top.Draw()
bottom.Draw()

top.cd()

legend = ROOT.TLegend(0.56, 0.70, 0.92, 0.88)
legend.SetBorderSize(0)

for i, name in enumerate(names):
    hist = h[name]
    hist.SetLineColor(colors[name])
    hist.SetMarkerColor(colors[name])
    hist.SetLineWidth(2)
    hist.SetTitle("")

    hist.GetYaxis().SetTitle(
        "Weighted fraction / GeV"
    )
    hist.GetYaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetLabelSize(0.045)
    hist.GetYaxis().SetTitleOffset(1.05)
    hist.GetXaxis().SetLabelSize(0)

    hist.Draw("HIST" if i == 0 else "HIST SAME")
    legend.AddEntry(hist, labels[name], "l")

legend.Draw()

bottom.cd()

reference = h["VETO_OFF"]

ratios = {}
for name in ("MPI_OFF", "VETO_ON"):
    ratio = h[name].Clone(f"ratio_{name}")
    ratio.Divide(reference)
    ratio.SetLineColor(colors[name])
    ratio.SetMarkerColor(colors[name])
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.55)
    ratios[name] = ratio

first = ratios["MPI_OFF"]
first.SetTitle("")
first.GetYaxis().SetTitle("Ratio to veto OFF")
first.GetXaxis().SetTitle(
    "Leading central AK4 GenJet p_{T} [GeV]"
)
first.GetYaxis().SetRangeUser(0.0, 1.5)
first.GetYaxis().SetNdivisions(505)
first.GetYaxis().SetTitleSize(0.11)
first.GetYaxis().SetLabelSize(0.09)
first.GetYaxis().SetTitleOffset(0.47)
first.GetXaxis().SetTitleSize(0.12)
first.GetXaxis().SetLabelSize(0.10)
first.GetXaxis().SetTitleOffset(1.1)

first.Draw("E1")
ratios["VETO_ON"].Draw("E1 SAME")

line = ROOT.TLine(30, 1, 400, 1)
line.SetLineStyle(2)
line.Draw()

canvas.SaveAs("leading_ak4_central_comparison.png")
canvas.SaveAs("leading_ak4_central_comparison.pdf")

print("Saved leading_ak4_central_comparison.png")
print("Saved leading_ak4_central_comparison.pdf")
