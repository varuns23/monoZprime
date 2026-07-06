# run using python3.9 postFitPlot.py
from __future__ import absolute_import
from style import *
from utilities import *
import plotting as plot
import os, ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle()
ROOT.gStyle.SetErrorX(0)
ROOT.gStyle.SetTextFont(42)               # Default text font --42==helvetica
ROOT.gStyle.SetLabelFont(42, "X")         # X axis labels
ROOT.gStyle.SetLabelFont(42, "Y")         # Y axis labels
ROOT.gStyle.SetLabelFont(42, "Z")         # Z axis labels
ROOT.gStyle.SetTitleFont(42, "X")         # X axis title
ROOT.gStyle.SetTitleFont(42, "Y")         # Y axis title
ROOT.gStyle.SetTitleFont(42, "Z")         # Z axis title

fin = rt.TFile("fitDiagnostics.fullrun2Mx150Mv3000Zp1p0_rmin_0.root")
year = "2016"#"2016","2017","2018""
first_dir = "shapes_prefit"
second_dir = "ch%s"%year
my_var = "varZ_xgb_VLoose_0p1_var"

c1 = rt.TCanvas('c1','c1',800,800)
c1.SetTitle("")
pad1 = rt.TPad("pad1","pad1",0,0.3,1,1)
pad1.Draw()
pad1.cd()
pad1.SetBottomMargin(0.001)
pad1.SetTicks(1, 1)

hs = rt.THStack("hs","")

## Get Sum Bkg and 1st Signal
h_sumbkg = fin.Get(first_dir + "/" + second_dir + "/total_background")
if (h_sumbkg.GetSumw2N() == 0): h_sumbkg.Sumw2(rt.kTRUE)
h_sig = fin.Get("shapes_prefit" + "/" + second_dir + "/total_signal")# same as Mx1_Mv3000 , first_dir
if (h_sig.GetSumw2N() == 0): h_sig.Sumw2(rt.kTRUE)
###Get 2nd signal MC
sig_fit_val = 1
Mx_sig2 = '800'#'150'#
Mv_sig2 ='2000'#'3000'
file_second_sig = rt.TFile("fitDiagnostics.fullrun2Mx800Mv2000Zp1p0_rmin_0.root")
h_sig_2 = file_second_sig.Get("shapes_prefit" + "/" + second_dir + "/total_signal")

### Get Data
gr_dat = fin.Get(first_dir + "/" + second_dir + "/data")  # This is a TGraphAsymmErrors, not a TH1F
h_dat = makeHistogram(gr_dat,h_sig) # This is a TH1
bkg_proc_sorted = ['DYJets', 'Top', 'DiBoson', 'QCD', 'WJets', 'ZJets']#sorted_proc_order[year]
bkg_legends = {
        'DYJets':'Z(ll)+jets',
        'Top':'Top',
        'DiBoson':'WW/WZ/ZZ',
        'QCD':'QCD multijet',
        'WJets':'W(l#nu)+jets',
        'ZJets':'Z(#nu#nu)+jets',
}
h_sumbkg=get_new_ticks(h_sumbkg);
h_sig=get_new_ticks(h_sig);
h_dat=get_new_ticks(h_dat); 
h_sig_2=get_new_ticks(h_sig_2)

bkg_hists = {}
h_test = h_sumbkg.Clone("h_test")
h_test.Reset()
for proc in bkg_proc_sorted:
        bkg_hists[proc] = fin.Get(first_dir + "/" + second_dir + "/%s"%proc)
        bkg_hists[proc].SetFillColor(Colormap[proc])
        bkg_hists[proc]=get_new_ticks(bkg_hists[proc])
        hs.Add(bkg_hists[proc],"hist")
        h_test.Add(bkg_hists[proc])

for i in range(0, h_test.GetNbinsX() + 2): # for dividing by ratio
    h_test.SetBinError(i, 0.0)

#check_hist(h_test,h_sumbkg);print_bin_errors(h_test);print_bin_errors(h_sumbkg)#; raw_input("check?")
ymax = max(hs.GetMaximum(),gr_dat.GetMaximum(),h_sig.GetMaximum(),h_sig_2.GetMaximum())
hs.SetMaximum(10**9); hs.SetMinimum(0.1) #All years
#if(year=="2018"):hs.SetMaximum(10**9); hs.SetMinimum(0.1)#2018
#elif(year=="2017"):hs.SetMaximum(2*10**8); hs.SetMinimum(0.1)#2017
#elif(year=="2016"):hs.SetMaximum(10**8); hs.SetMinimum(0.1)#2016
hs.Draw()

hs.GetXaxis().SetLabelSize(0)
hs.GetXaxis().SetTickSize(0)
hs.GetXaxis().SetTitle('')
hs.GetYaxis().SetTitle('event count/0.1')
hs.GetYaxis().SetTitleSize(0.08)
hs.GetYaxis().SetTitleOffset(0.8)
hs.GetYaxis().SetLabelSize(0.07)

pad1.SetLogy()

h_err = h_sumbkg.Clone()
h_err.SetFillColor(Colormap["All_unc"])  # Set grey colour (12) and alpha (0.3)
h_err.SetMarkerSize(0)
h_err.SetFillStyle(3001)
h_err.Draw("E2SAME")

h_sig.SetLineColor(TColor.GetColor('#1b9e77'))#ROOT.kRed)#a96b59,#e76300
h_sig.SetLineWidth(3)
h_sig.Draw("same hist")

h_sig_2.SetLineColor(TColor.GetColor('#b9ac70'))#ROOT.kRed)
h_sig_2.SetLineWidth(3)
h_sig_2.Draw("same hist")

gr_dat.SetMarkerStyle(20)
gr_dat.SetMarkerSize(1.5)
gr_dat.Draw("P same")

x1,x2,y1,y2 = get_legend_coords("right",my_var)
#legend = rt.TLegend(x1-0.05-0.08,y1-0.2,x2-0.05-0.09,y2)
legend = rt.TLegend(x1-0.03,y1-0.18,x2-0.08,y2+.02)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.05)
legend.SetNColumns(2)
texCMS,texCMS_2 = getCMSTex(scale=1.1,text_2=""); 
texLumi = getLumiTex("%s fb^{-1}"%lumi_map[year],'',scale=1)

legend.AddEntry(gr_dat, "data", "ep")
for proc in reversed(bkg_proc_sorted): 
       legend.AddEntry(bkg_hists[proc], bkg_legends[proc], "F")
legend.AddEntry(h_err, "Sys uncertainty", "F")# Bkg. Postfit # stat not included in grey band 
legend.AddEntry(h_sig, "m_{Z'}=1GeV; m_{DM}=150GeV; m_{med}=3TeV", "L")
legend_2 = rt.TLegend(x1-0.03,y1-0.2-0.02-0.01,x2-0.08,y1-0.2-0.01)
legend_2.SetFillStyle(0)
legend_2.SetBorderSize(0)
legend_2.SetTextSize(0.05)
legend_2.SetNColumns(2)
legend_2.AddEntry(h_sig_2, "m_{Z'}=1GeV; m_{DM}=%sGeV; m_{med}=2TeV"%(Mx_sig2), "L")#x10^{5}

legend.Draw("same");texCMS.Draw("same");texCMS_2.Draw("same"); texLumi.Draw("same");
legend_2.Draw("same")

c1.cd()
pad2 = rt.TPad("pad2","pad2",0,0,1,0.3)
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.001)
pad2.SetBottomMargin(0.3)
ratio_nom = h_dat.Clone("ratio_nom")
ratio_nom.Divide(h_test)

ratio_nom.SetMarkerSize(1.3)
ratio_nom.Draw("E")
ratio_nom.SetTitle("")

ratio_nom.GetYaxis().SetTitle("Data/Exp.")
ratio_nom.GetYaxis().SetTitleSize(0.14)
ratio_nom.GetYaxis().SetTitleOffset(0.4)
ratio_nom.GetYaxis().SetRangeUser(0.4,1.6)#(0.5,1.5)#(0.1,2)#
ratio_nom.GetYaxis().SetLabelSize(0.14)
ratio_nom.GetYaxis().SetNdivisions(3)

ratio_nom.GetXaxis().SetLabelSize(0.2)
ratio_nom.GetXaxis().SetTitle("ML output")
ratio_nom.GetXaxis().SetTitleSize(0.15)
ratio_nom.GetXaxis().SetTitleOffset(0.9)
ratio_nom.GetXaxis().SetLabelOffset(0.015)

h_sumbkg_up = get_sum_bkg_var(h_sumbkg,"up")
h_sumbkg_dn = get_sum_bkg_var(h_sumbkg,"dn")
ratio_band = get_unc_band_from_bounds(h_sumbkg_up,h_sumbkg_dn,h_sumbkg,ratioplot=True)
UncBandStyle(ratio_band,color=Colormap["All_unc"])
ratio_band.Draw('2same') 
ratio_nom.Draw("Esame")

c1.SaveAs("plots/fig4-prefit-%s_paper.pdf"%second_dir)
#c1.SaveAs("plots/fig4-prefit-%s_paper.png"%second_dir)
