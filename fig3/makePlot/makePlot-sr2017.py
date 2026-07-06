from plot_utils import *

if len(sys.argv) < 2:
    print("Usage: python3 makePlot.py input.root")
    sys.exit(1)

infile_name = sys.argv[1]
infile_base = os.path.splitext(infile_name)[0]

backgrounds = ["gjet", "zjet", "wjet", "qcd", "dyjet", "diboson", "top"]


# -----------------------
# Create histograms
# -----------------------
fIn = rt.TFile.Open(infile_name, "READ")
if not fIn or fIn.IsZombie():
    raise RuntimeError("Could not open ROOT file")

h_bkgs = {}
h_bkgs["zjet"] = get_root_object(fIn, "ZJets")
h_bkgs["wjet"] = get_root_object(fIn, "WJets")
h_bkgs["qcd"] = get_root_object(fIn, "QCD")
h_bkgs["diboson"] = get_root_object(fIn, "DiBoson")
h_bkgs["top"] = get_root_object(fIn, "Top")
h_bkgs["dyjet"] = get_root_object(fIn, "DYJets")
h_bkgs["gjet"] = get_root_object(fIn, "GJets")

h_bkg_err = get_root_object(fIn, "bkg_errband")
h_ratio = get_root_object(fIn, "ratio_nom_test")
h_ratio_band = get_root_object(fIn, "ratio_band")

h_sig1 = get_root_object(fIn, "Mx150_Mv3000")
h_sig1.SetLineColor(TColor.GetColor('#1b9e77'))
h_sig1.SetLineWidth(3)
h_sig1.SetFillStyle(0)

h_sig2 = get_root_object(fIn, "Mx800_Mv3000")
h_sig2.SetLineColor(TColor.GetColor('#b9ac70'))
h_sig2.SetLineWidth(3)
h_sig2.SetFillStyle(0)

h_data = get_root_object(fIn, "Data")
h_data.SetMarkerStyle(rt.kFullCircle)
h_data.SetLineColor(rt.kBlack)

xmin, xmax = getXrange(infile_base)
print("X range: ", xmin, " to ", xmax)

# -----------------------
# Stack backgrounds
# -----------------------
hs = rt.THStack("hs", "")
hs.SetTitle("")

for bkg in backgrounds:
    h_bkgs[bkg].SetFillColor(bkg_colors[bkg])
    h_bkgs[bkg].SetLineColor(rt.kBlack)

hs.Add(h_bkgs["gjet"])
hs.Add(h_bkgs["dyjet"])
hs.Add(h_bkgs["top"])
hs.Add(h_bkgs["diboson"])
hs.Add(h_bkgs["qcd"])
hs.Add(h_bkgs["wjet"])
hs.Add(h_bkgs["zjet"])

# -----------------------
# Canvas & pads
# -----------------------
c = rt.TCanvas("c", "Data/MC", 800, 800)
c.SetTitle("")

pad1 = rt.TPad("pad1", "", 0, 0.3, 1, 1)
pad2 = rt.TPad("pad2", "", 0, 0.01, 1, 0.295)

pad1.SetBottomMargin(0.001)
pad1.SetTicks(1,1)
pad1.Draw()
pad2.SetTopMargin(0.04)
pad2.SetBottomMargin(0.35)
pad2.SetGridy()
pad2.Draw()

# -----------------------
# Top pad (main plot)
# -----------------------
pad1.cd()
pad1.SetLogy()
h_data.SetTitle("")
h_data.SetStats(0)
h_data.SetMinimum(3e-2)
h_data.SetMaximum(3e4)
h_data.GetXaxis().SetRangeUser(xmin, xmax)
#h_data.SetMaximum(1.5 * max(hs.GetMaximum(), h_data.GetMaximum()))
h_data.GetXaxis().SetLabelSize(0)
h_data.GetXaxis().SetTickSize(0)
h_data.GetXaxis().SetTitle('')
h_data.GetYaxis().SetTitleSize(0.065)
h_data.GetYaxis().SetTitleOffset(0.9)
h_data.GetYaxis().SetLabelSize(0.055)
h_data.GetYaxis().SetLabelOffset(0.005)

if "recoil" in infile_base:
    h_data.GetYaxis().SetTitle("Events / 50 GeV")
    h_data.GetXaxis().SetRangeUser(250, 900)
if "HPSJetPtOverAssociatedJetPt" in infile_base:
    h_data.GetYaxis().SetTitle("Events / 0.1")
    h_data.SetMaximum(1e6)
if "Associatedjet_chHEF" in infile_base:
    h_data.GetYaxis().SetTitle("Events / 0.04")
if "Associatedjet_neEmEF" in infile_base:
    h_data.GetYaxis().SetTitle("Events / 0.04")
if "Associatedjet_neHEF" in infile_base:
    h_data.GetYaxis().SetTitle("Events / 0.04")
if "HPSJet_leadTkPtOverhpsPt" in infile_base:
    h_data.GetYaxis().SetTitle("Events / 0.1")
    h_data.SetMaximum(1e5)

h_data.Draw("E1")
hs.Draw("histsame")
h_sig1.Draw("hist same")
#h_sig2.Draw("hist same")
UncBandStyle(h_bkg_err,color=16)
h_bkg_err.Draw("E2same") 
h_data.Draw("E1 same")

texCMS = rt.TLatex(0.13,0.946,"#bf{CMS}")
texCMS.SetNDC()
texCMS.SetTextFont(42)
texCMS.SetTextSize(0.06)
texCMS.Draw()   
texLumi = rt.TLatex(0.57,0.946,"%s (13 TeV, %s)" % ("41.5 fb^{-1}", "2017"))
texLumi.SetNDC()
texLumi.SetTextFont(42)
texLumi.SetTextSize(0.057)
texLumi.Draw()
texExtra = rt.TLatex(0.17,0.864, "Signal Region")
texExtra.SetNDC()
texExtra.SetTextFont(42)
texExtra.SetTextSize(0.045)
texExtra.Draw()

leg = rt.TLegend(0.38, 0.58, 0.8, 0.91)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.045)
leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.AddEntry(h_data, "Data", "lep")
leg.AddEntry(h_bkgs["zjet"], "Z(#nu#nu)+jets", "f")
leg.AddEntry(h_bkgs["wjet"], "W(l#nu)+jets", "f")
leg.AddEntry(h_bkgs["qcd"], "QCD multijet", "f")
leg.AddEntry(h_bkgs["diboson"], "WW/WZ/ZZ", "f")
leg.AddEntry(h_bkgs["top"], "t#bar{t}/single-t", "f")
leg.AddEntry(h_bkgs["dyjet"], "Z(ll)+jets", "f")
leg.AddEntry(h_bkgs["gjet"], "#gamma+jets", "f")
#leg.AddEntry(h_bkg_err, "Sys uncertainty", "f")
leg.AddEntry(h_sig1, "m_{Z'}=1GeV; m_{DM}=150GeV; m_{med}=3TeV", "L")
#leg.AddEntry(h_sig2, "m_{Z'}=1GeV; m_{DM}=800GeV; m_{med}=3TeV", "L")
#leg.AddEntry(h_sig, "Signal", "l")
leg.Draw()

leg2 = rt.TLegend(0.38,0.52,0.8,0.58)
leg2.SetFillStyle(0)
leg2.SetBorderSize(0)
leg2.SetTextSize(0.045)
leg2.SetNColumns(2)
leg2.SetBorderSize(0)
leg2.AddEntry(h_bkg_err, "Sys uncertainty", "f")
#leg2.AddEntry(h_sig1, "m_{Z'}=1GeV; m_{DM}=150GeV; m_{med}=3TeV", "L")
#leg2.AddEntry(h_sig2, "m_{Z'}=1GeV; m_{DM}=800GeV; m_{med}=3TeV", "L")
leg2.Draw()
pad1.RedrawAxis()
pad1.Modified()
pad1.Update()
# -----------------------
# Bottom pad (ratio)
# -----------------------
pad2.cd()

ratio_band = h_ratio_band.Clone("ratio_band")
ratio = h_ratio.Clone("data_mc_ratio")
ratio.SetMarkerStyle(rt.kFullCircle)
ratio.SetLineColor(rt.kBlack)
ratio.SetStats(0)
ratio.SetTitle("")
ratio.GetYaxis().SetTitle("Data/Bkg")
ratio.GetYaxis().SetTitleOffset(0.31)
ratio.GetYaxis().SetTitleSize(0.16)#0.18
ratio.GetYaxis().SetLabelOffset(0.01)
ratio.GetYaxis().SetLabelSize(0.12)#0.14
ratio.GetXaxis().SetRangeUser(xmin, xmax)
ratio.GetXaxis().SetTitleOffset(0.92)#0.9
ratio.GetXaxis().SetTitleSize(0.16)#0.18
ratio.GetXaxis().SetLabelOffset(0.01)
ratio.GetXaxis().SetLabelSize(0.14)#0.15


if "recoil" in infile_base:
    ratio.GetXaxis().SetTitle("Recoil [GeV]")
    ratio.GetXaxis().SetRangeUser(250, 900)
    ratio.GetYaxis().SetRangeUser(0, 3)
    ratio.GetYaxis().SetNdivisions(303)
if "HPSJetPtOverAssociatedJetPt" in infile_base:
    ratio.GetXaxis().SetTitle("Pencil jet p_{T}/Associated jet p_{T}")    
    ratio.GetYaxis().SetRangeUser(0, 3)
    ratio.GetYaxis().SetNdivisions(303)
if "Associatedjet_chHEF" in infile_base:
    ratio.GetXaxis().SetTitle("Associated jet charged hadron energy fraction")
    ratio.GetYaxis().SetRangeUser(0, 2)
    ratio.GetYaxis().SetNdivisions(202)
if "Associatedjet_neEmEF" in infile_base:
    ratio.GetXaxis().SetTitle("Associated jet neutral em energy fraction")
    ratio.GetYaxis().SetRangeUser(0, 2)
    ratio.GetYaxis().SetNdivisions(202)
if "Associatedjet_neHEF" in infile_base:
    ratio.GetXaxis().SetTitle("Associated jet neutral hadron energy fraction")
    ratio.GetYaxis().SetRangeUser(0, 2)
    ratio.GetYaxis().SetNdivisions(202)
if "HPSJet_leadTkPtOverhpsPt" in infile_base:
    ratio.GetXaxis().SetTitle("Leading track p_{T}/Pencil jet p_{T}")
    ratio.GetYaxis().SetRangeUser(0, 2)
    ratio.GetYaxis().SetNdivisions(202)

ratio.Draw("E1")

UncBandStyle(ratio_band,color=16)
ratio_band.Draw("E2same") 
ratio.Draw("E1same")

pad2.RedrawAxis()
pad2.Modified()
pad2.Update()

#line = rt.TLine(xmin, 1.0, xmax, 1.0)
#line.SetLineStyle(2)
#line.Draw("same")

# -----------------------
# Save
# -----------------------
c.SaveAs("datamc-2017" + infile_base + ".pdf")
