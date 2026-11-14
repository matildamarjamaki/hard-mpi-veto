#include <TFile.h>
#include <TH1D.h>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include <TLine.h>
#include <TLatex.h>
#include <TLegend.h>
#include <TStyle.h>

#include <cmath>
#include <iostream>
#include <vector>

void plot_modified_plain_clean()
{
    gStyle->SetOptStat(0);

    TFile f("root/herwig_highpt_comparison.root", "READ");

    auto *h =
        dynamic_cast<TH1D*>(f.Get("ratio_modified_over_plain"));

    if (!h) {
        std::cerr
            << "ERROR: ratio_modified_over_plain not found\n";
        return;
    }

    // Nominal bins and bins known to be dominated by anomalous genWeights.
    std::vector<double> x, y, ex, ey;
    std::vector<double> xb, yb, exb, eyb;

    for (int i = 1; i <= h->GetNbinsX(); ++i) {

        const double lo = h->GetXaxis()->GetBinLowEdge(i);
        const double hi = h->GetXaxis()->GetBinUpEdge(i);

        if (lo < 500. || lo >= 3273.)
            continue;

        const double val = h->GetBinContent(i);
        const double err = h->GetBinError(i);

        if (!std::isfinite(val) || val <= 0.)
            continue;

        const double xc = 0.5 * (lo + hi);
        const double xe = 0.5 * (hi - lo);

        const bool pathological =
            (std::abs(lo - 737.) < 0.1) ||
            (std::abs(lo - 3103.) < 0.1);

        if (pathological) {
            xb.push_back(xc);
            yb.push_back(val);
            exb.push_back(xe);
            eyb.push_back(err);
        } else {
            x.push_back(xc);
            y.push_back(val);
            ex.push_back(xe);
            ey.push_back(err);
        }
    }

    TCanvas c("c", "", 900, 650);

    c.SetLogx();
    c.SetLeftMargin(0.13);
    c.SetRightMargin(0.04);
    c.SetBottomMargin(0.13);
    c.SetTopMargin(0.08);

    TH1D frame("frame", "", 100, 500., 3300.);

    frame.SetMinimum(0.45);
    frame.SetMaximum(1.05);

    frame.GetXaxis()->SetTitle(
        "Leading GenJet p_{T} [GeV]"
    );
    frame.GetYaxis()->SetTitle(
        "Modified MPI ON / Plain MPI ON"
    );

    frame.GetXaxis()->SetTitleSize(0.045);
    frame.GetYaxis()->SetTitleSize(0.045);

    frame.GetXaxis()->SetLabelSize(0.040);
    frame.GetYaxis()->SetLabelSize(0.040);

    frame.GetXaxis()->SetTitleOffset(1.15);
    frame.GetYaxis()->SetTitleOffset(1.25);

    frame.Draw();

    // Unity reference.
    TLine unity(500., 1., 3300., 1.);
    unity.SetLineStyle(2);
    unity.SetLineWidth(2);
    unity.Draw();

    // Nominal bins.
    TGraphErrors good(
        x.size(),
        x.data(),
        y.data(),
        ex.data(),
        ey.data()
    );

    good.SetMarkerStyle(20);
    good.SetMarkerSize(1.0);
    good.SetLineWidth(1);
    good.Draw("P SAME");

    // Pathological bins are explicitly distinguished, not removed.
    TGraphErrors bad(
        xb.size(),
        xb.data(),
        yb.data(),
        exb.data(),
        eyb.data()
    );

    bad.SetMarkerStyle(24);
    bad.SetMarkerSize(1.3);
    bad.SetLineWidth(1);
    bad.Draw("P SAME");

    // Compact generator / selection information.
    TLatex text;
    text.SetNDC();
    text.SetTextSize(0.029);

    text.DrawLatex(
        0.16, 0.87,
        "Herwig 7.2.2, #sqrt{s} = 13.6 TeV"
    );

    text.DrawLatex(
        0.16, 0.825,
        "10M generated events / sample"
    );

    text.DrawLatex(
        0.16, 0.780,
        "Leading GenJet, |y| < 0.5"
    );

    // Put the legend in the upper-right, away from the
    // pathological 737-790 GeV error bar.
    TLegend leg(0.59, 0.79, 0.92, 0.89);

    leg.SetBorderSize(0);
    leg.SetFillStyle(0);
    leg.SetTextSize(0.027);

    leg.AddEntry(
        &good,
        "Other bins",
        "p"
    );

    leg.AddEntry(
        &bad,
        "Anomalous-weight bin",
        "p"
    );

    leg.Draw();

    // The 3103-3273 GeV point lies far below the displayed range.
    TLatex note;
    note.SetNDC();
    note.SetTextSize(0.024);

    note.DrawLatex(
        0.17, 0.205,
        "3103-3273 GeV bin: ratio = 3.2#times10^{-4}"
    );

    note.DrawLatex(
        0.17, 0.165,
        "99.96% of plain-bin weight from one event"
    );

    c.RedrawAxis();

    c.SaveAs(
        "plots/herwig_modified_over_plain_clean.pdf"
    );

    c.SaveAs(
        "plots/herwig_modified_over_plain_clean.png"
    );

    std::cout
        << "Wrote plots/herwig_modified_over_plain_clean.{pdf,png}\n";
}
