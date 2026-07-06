"""
PyROOT script to reproduce the CMS control region yield plot
as a 4-pad canvas (one pad per CR: SingleMu, SingleEle, DoubleMu, DoubleEle).

Each pad shows 3 grouped bar sets (2016, 2017, 2018), each with:
  - MC background-like (score_0) as a stacked bar
  - MC signal-like    (score_1) on top
  - Data background-like (score_0) as a stacked bar  (grey, semi-transparent overlay)
  - Data signal-like  (score_1) on top               (dark grey)

All yields are normalised so that total (score_0 + score_1) = 100.
"""

import ROOT
import json
import math

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

# ── Load data ─────────────────────────────────────────────────────────────────
with open("yields_all_years_all_regions_threshold_0.71_rebin_1.json") as f:
    data = json.load(f)

# For 2016 we merge pre_VFP + post_VFP
def get_yields(year_str, cr):
    """Return (data_s0, data_s1, mc_s0, mc_s1) for a given year and CR."""
    yr = data[year_str]
    if "pre_VFP" in yr:          # 2016 has sub-eras
        d0 = yr["pre_VFP"][cr]["data"]["score_0"]  + yr["post_VFP"][cr]["data"]["score_0"]
        d1 = yr["pre_VFP"][cr]["data"]["score_1"]  + yr["post_VFP"][cr]["data"]["score_1"]
        m0 = yr["pre_VFP"][cr]["sum_bkg_mc"]["score_0"] + yr["post_VFP"][cr]["sum_bkg_mc"]["score_0"]
        m1 = yr["pre_VFP"][cr]["sum_bkg_mc"]["score_1"] + yr["post_VFP"][cr]["sum_bkg_mc"]["score_1"]
    else:
        d0 = yr[cr]["data"]["score_0"]
        d1 = yr[cr]["data"]["score_1"]
        m0 = yr[cr]["sum_bkg_mc"]["score_0"]
        m1 = yr[cr]["sum_bkg_mc"]["score_1"]
    return d0, d1, m0, m1

# ── Colours (matching screenshot) ─────────────────────────────────────────────
col_mc_bkg = {
    "2016": ROOT.TColor.GetColor("#9ecae1"),   # light blue
    "2017": ROOT.TColor.GetColor("#fcbba1"),   # light salmon/pink
    "2018": ROOT.TColor.GetColor("#a1d99b"),   # light green
}
col_mc_sig = {
    "2016": ROOT.TColor.GetColor("#2171b5"),   # blue
    "2017": ROOT.TColor.GetColor("#cb181d"),   # red
    "2018": ROOT.TColor.GetColor("#238b45"),   # green
}
col_dat_bkg = ROOT.TColor.GetColor("#cccccc")  # light grey
col_dat_sig = ROOT.TColor.GetColor("#555555")  # dark grey

# ── Control regions & labels ───────────────────────────────────────────────────
CRs = ["SingleMuCR", "SingleEleCR", "DoubleMuCR", "DoubleEleCR"]
CR_labels = {
    "SingleMuCR":  "Single muon validation region",
    "SingleEleCR": "Single electron validation region",
    "DoubleMuCR":  "Double muon validation region",
    "DoubleEleCR": "Double electron validation region",
}
years = ["2016", "2017", "2018"]

# ── Canvas & pads ─────────────────────────────────────────────────────────────
c = ROOT.TCanvas("c", "CMS CR yields", 1600, 1200)
#c.Divide(2, 2, 0.005, 0.005)   # 2 cols × 2 rows, small gaps
c.Divide(2, 2, 0.004, 0.08)   # 2 cols × 2 rows, small gaps

# Pad order: top-left=SingleMu, top-right=SingleEle,
#            bottom-left=DoubleMu, bottom-right=DoubleEle
pad_order = ["SingleEleCR", "SingleMuCR", "DoubleEleCR", "DoubleMuCR"]

# Keep ROOT objects alive
all_hists = []

def make_pad_plot(pad_idx, cr):
    """Draw stacked, normalised bars for one CR into pad pad_idx (1-based)."""
    pad = c.cd(pad_idx)
    pad.SetLeftMargin(0.14)
    pad.SetRightMargin(0.04)
    pad.SetBottomMargin(0.08)
    pad.SetTopMargin(0.08)#0.08

    # 3 year groups × 2 bar sets (MC, Data) = 6 bars total
    # We place them at x = 1,2,3 for MC and 1.4,2.4,3.4 for Data (offset)
    # Use THStack-like manual approach with TH1F of 6 bins

    n_groups = 3          # years
    bar_w    = 0.5 # 0.5 #0.35       # width of each bar in histogram units
    gap      = 0.5        # distance between group centres
    offset   = 0.5 #0.0 #0.38       # shift between MC bar and Data bar within group

    # Bin centres:  MC at i*gap,  Data at i*gap + offset   (i=0,1,2)
    n_bins = 10            # enough range
    #n_bins = 7            # enough range
    #x_min, x_max = 0.0, 3.5
    x_min, x_max = 0.0, 5.0 

    def make_h(name, fill_col, line_col=None):
        h = ROOT.TH1F(name, "", n_bins, x_min, x_max)
        h.SetFillColor(fill_col)
        h.SetLineColor(line_col if line_col else fill_col)
        h.SetLineWidth(0)
        h.SetBarWidth(bar_w)
        all_hists.append(h)
        return h

    # MC bkg + sig stacked  (one pair per year)
    # Data bkg + sig stacked (one pair per year)
    hmc_bkg, hmc_sig, hdat_bkg, hdat_sig = {}, {}, {}, {}

    for i, yr in enumerate(years):
        #x_mc  = (i + 1)*gap  - bar_w / 2        # histogram x-centre for MC bar
        x_mc = offset + gap/2  + 3*bar_w*i 
        print(f"Year {yr}, CR {cr}: MC bar at x({i})={x_mc:.2f}")
        x_dat = x_mc + gap                     # histogram x-centre for Data bar
        print(f"Year {yr}, CR {cr}: Data bar at x({i})={x_dat:.2f}")

        d0, d1, m0, m1 = get_yields(yr, cr)

        # Normalise to 100
        tot_mc  = m0 + m1
        tot_dat = d0 + d1
        mc_bkg_n  = 100.0 * m0 / tot_mc  if tot_mc  > 0 else 0.0
        mc_sig_n  = 100.0 * m1 / tot_mc  if tot_mc  > 0 else 0.0
        dat_bkg_n = 100.0 * d0 / tot_dat if tot_dat > 0 else 0.0
        dat_sig_n = 100.0 * d1 / tot_dat if tot_dat > 0 else 0.0

        # MC histograms (one per year so we can set different colours)
        hb = make_h(f"hmc_bkg_{cr}_{yr}", col_mc_bkg[yr], ROOT.kBlack)
        hs = make_h(f"hmc_sig_{cr}_{yr}", col_mc_sig[yr], ROOT.kBlack)
        hb.SetBarOffset((x_mc - (i + 1) * gap) / gap + 0.5 - bar_w / 2)
        # simpler: just fill bin i+1 for MC, bin i+1 but offset for data
        # Use separate TH1F per bar instead:
        hb.Fill(x_mc, mc_bkg_n)
        hs.Fill(x_mc, mc_sig_n + mc_bkg_n)   # we'll draw MC sig on top manually

        hmc_bkg[yr] = (hb, mc_bkg_n, x_mc, mc_sig_n)
        hmc_sig[yr] = hs

        hdb = make_h(f"hdat_bkg_{cr}_{yr}", col_dat_bkg, ROOT.kBlack)
        hds = make_h(f"hdat_sig_{cr}_{yr}", col_dat_sig, ROOT.kBlack)
        hdb.Fill(x_dat, dat_bkg_n)
        hds.Fill(x_dat, dat_sig_n + dat_bkg_n)
        hdat_bkg[yr] = (hdb, dat_bkg_n, x_dat, dat_sig_n)
        hdat_sig[yr] = hds

    # ── Draw frame ────────────────────────────────────────────────────────────
    frame = pad.DrawFrame(x_min, 0, x_max, 108)
    frame.GetYaxis().SetTitle("Event yield (%)")
    frame.GetYaxis().SetTitleSize(0.07)
    frame.GetYaxis().SetTitleOffset(0.85)
    frame.GetYaxis().SetLabelSize(0.065)
    frame.GetYaxis().SetLabelOffset(0.01)
    frame.GetYaxis().SetNdivisions(510)
    frame.GetYaxis().SetRangeUser(0, 130)
    frame.GetXaxis().SetNdivisions(0)     # no x ticks (we'll draw custom labels)
    frame.GetXaxis().SetLabelSize(0)
    all_hists.append(frame)

    # ── Draw bars (background first, then signal on top) ──────────────────────
    for i, yr in enumerate(years):
        x_mc  = (i + 1) * gap
        x_dat = x_mc + offset

        hb, bkg_val, xc, sig_val = hmc_bkg[yr]
        hdb, dat_bkg_val, xcd, dat_sig_val = hdat_bkg[yr]

        bw = bar_w  # half-width

        # MC background rectangle
        box = ROOT.TBox(xc - bw/2, 0, xc + bw/2, bkg_val)
        box.SetFillColor(col_mc_bkg[yr])
        box.SetLineColor(ROOT.kBlack)
        box.SetLineWidth(1)
        box.Draw("l")
        all_hists.append(box)

        # MC signal rectangle (stacked on top)
        if sig_val > 0:
            sbox = ROOT.TBox(xc - bw/2, bkg_val, xc + bw/2, bkg_val + sig_val)
            sbox.SetFillColor(col_mc_sig[yr])
            sbox.SetLineColor(ROOT.kBlack)
            sbox.SetLineWidth(1)
            sbox.Draw("l")
            all_hists.append(sbox)

        # Data background rectangle
        dbox = ROOT.TBox(xcd - bw/2, 0, xcd + bw/2, dat_bkg_val)
        dbox.SetFillColor(col_dat_bkg)
        dbox.SetLineColor(ROOT.kBlack)
        dbox.SetLineWidth(1)
        dbox.Draw("l")
        all_hists.append(dbox)

        # Data signal rectangle
        if dat_sig_val > 0:
            dsbox = ROOT.TBox(xcd - bw/2, dat_bkg_val, xcd + bw/2, dat_bkg_val + dat_sig_val)
            dsbox.SetFillColor(col_dat_sig)
            dsbox.SetLineColor(ROOT.kBlack)
            dsbox.SetLineWidth(1)
            dsbox.Draw("l")
            all_hists.append(dsbox)

        # Year labels under MC bar
        lat = ROOT.TLatex()
        lat.SetNDC(False)
        lat.SetTextSize(0.07)
        lat.SetTextFont(42)
        lat.SetTextAlign(22)
        lat.DrawLatex(xc+0.25, -6, yr)
        all_hists.append(lat)

        # Small "D" label under data bar (optional, skip to stay clean)

    # CR label at bottom centre
    lat2 = ROOT.TLatex()
    lat2.SetNDC(True)
    lat2.SetTextFont(42)
    lat2.SetTextSize(0.065)
    lat2.SetTextAlign(31)
    lat2.DrawLatex(0.92, 0.83, CR_labels[cr])
    #lat2.DrawLatex(0.68, 0.82, "validation region")
    # CMS label
    lat2.SetTextFont(62) #61
    lat2.SetTextSize(0.08)
    lat2.SetTextAlign(12)
    lat2.DrawLatex(0.19, 0.858, "CMS")
    #Luminosity label
    lat2.SetTextSize(0.06)
    lat2.DrawLatex(0.242, 0.96,"36.3 fb^{-1} (2016), 41.5 fb^{-1} (2017), 59.7 fb^{-1} (2018) (13 TeV)")

    all_hists.append(lat2)


# ── Draw each pad ─────────────────────────────────────────────────────────────
for idx, cr in enumerate(pad_order, start=1):
    make_pad_plot(idx, cr)

# ── Global legend in top-left pad ─────────────────────────────────────────────
c.cd()
leg = ROOT.TLegend(0.2, 0.44, 0.9, 0.57)
leg.SetNColumns(3)
leg.SetTextSize(0.025)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetHeader("Background-like MC               Signal-like MC                         Data")

# dummy boxes for legend
def dummy_box(col):
    b = ROOT.TBox(0, 0, 1, 1)
    b.SetFillColor(col)
    b.SetLineColor(ROOT.kBlack)
    all_hists.append(b)
    return b

leg.AddEntry(dummy_box(col_mc_bkg["2016"]), "2016               ", "f")
leg.AddEntry(dummy_box(col_mc_sig["2016"]), "2016               ", "f")
leg.AddEntry(dummy_box(col_dat_bkg), "Background-like", "f")
leg.AddEntry(dummy_box(col_mc_bkg["2017"]), "2017               ", "f")
leg.AddEntry(dummy_box(col_mc_sig["2017"]), "2017", "f")
leg.AddEntry(dummy_box(col_dat_sig), "Signal-like",     "f")
leg.AddEntry(dummy_box(col_mc_bkg["2018"]), "2018               ", "f")
leg.AddEntry(dummy_box(col_mc_sig["2018"]), "2018               ", "f")
#leg.AddEntry(dummy_box(ROOT.kWhite),  "",               "f")   # spacer

leg.Draw()
all_hists.append(leg)

# ── Save ──────────────────────────────────────────────────────────────────────
out_name = "ml_performance_CRs"
c.SaveAs(f"{out_name}.pdf")
c.SaveAs(f"{out_name}.png")
print(f"Saved {out_name}.pdf and {out_name}.png")
