# run using python3 postFitPlot.py
from __future__ import absolute_import
from style import *
from utilities import *
import CombineHarvester.CombineTools.plotting as plot
import os, ROOT
#import cmsstyle as CMS #https://cms-analysis.docs.cern.ch/guidelines/plotting/general/#__tabbed_1_2 , pip3 install --user cmsstyle
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

fin = ROOT.TFile("fitDiagnostics.fullrun2Mx150Mv3000Zp1p0_rmin_0.root")
year = "2018"#"2016","2017","2018""
first_dir = "shapes_prefit"
second_dir = "ch%s"%year
my_var = "varZ_xgb_VLoose_0p1_var"
c1 = rt.TCanvas('c1','c1',800,800)
pad1 = rt.TPad("pad1","pad1",0,0.3,1,1)
pad1.Draw()
pad1.cd()
pad1.SetBottomMargin(0.001)
pad1.SetTicks(1, 1)
x1,x2,y1,y2 = get_legend_coords("right",my_var)  
legend = rt.TLegend(x1-0.05-0.08,y1-0.2,x2-0.05-0.09,y2)
legend.SetTextSize(0.05)
legend.SetNColumns(2)
texCMS,texCMS_2 = getCMSTex(scale=1.1,text_2=""); texLumi = getLumiTex("%s fb^{-1}"%lumi_map[year],'',scale=1)

#legend = ROOT.TLegend(0.60, 0.70, 0.90, 0.91, "", "NBNDC")

hs = ROOT.THStack("hs","ML_score_postfit")

h_sumbkg = fin.Get(first_dir + "/" + second_dir + "/total_background")
if (h_sumbkg.GetSumw2N() == 0): h_sumbkg.Sumw2(rt.kTRUE)
h_sig = fin.Get("shapes_prefit" + "/" + second_dir + "/total_signal")# same as Mx1_Mv3000 , first_dir
if (h_sig.GetSumw2N() == 0): h_sig.Sumw2(rt.kTRUE)
###2nd signal
sig_fit_val = 1
Mx_sig2 = '800'#'150'#
Mv_sig2 ='2000'#'3000'
file_second_sig = ROOT.TFile("fitDiagnostics.fullrun2Mx800Mv2000Zp1p0_rmin_0.root")
h_sig_2_raw = file_second_sig.Get("shapes_prefit" + "/" + second_dir + "/total_signal")
h_sig_2 = h_sig.Clone("Mx%s_Mv%s_second_sig"%(Mx_sig2,Mv_sig2))
h_sig_2.Reset()
xbins = h_sig.GetNbinsX()
for ibin in range(1,xbins+1):
        val = h_sig_2_raw.GetBinContent(ibin)*sig_fit_val*1#scale signal by 10 times
        h_sig_2.SetBinContent(ibin,val)   
if (h_sig_2.GetSumw2N() == 0): h_sig_2.Sumw2(rt.kTRUE)         
###2nd signal
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
h_sumbkg=get_new_ticks(h_sumbkg);h_sig=get_new_ticks(h_sig);h_dat=get_new_ticks(h_dat); h_sig_2=get_new_ticks(h_sig_2)
#print(bkg_proc_sorted)
#'''
bkg_hists = {}
h_test = h_sumbkg.Clone("h_test")
h_test.Reset()
for proc in bkg_proc_sorted:
        bkg_hists[proc] = fin.Get(first_dir + "/" + second_dir + "/%s"%proc)
        bkg_hists[proc].SetFillColor(Colormap[proc])
        bkg_hists[proc]=get_new_ticks(bkg_hists[proc])
        #legend.AddEntry(bkg_hists[proc], bkg_legends[proc], "F")# adding later so that data is first
        hs.Add(bkg_hists[proc],"hist")
        h_test.Add(bkg_hists[proc])

for i in range(0, h_test.GetNbinsX() + 2): # for dividing by ratio
    h_test.SetBinError(i, 0.0)

check_hist(h_test,h_sumbkg);print_bin_errors(h_test);print_bin_errors(h_sumbkg)#; raw_input("check?")
ymax = max(hs.GetMaximum(),gr_dat.GetMaximum(),h_sig.GetMaximum(),h_sig_2.GetMaximum())
if(year=="2018"):hs.SetMaximum(10**9); hs.SetMinimum(0.1)#2018
elif(year=="2017"):hs.SetMaximum(2*10**8); hs.SetMinimum(0.1)#2017
elif(year=="2016"):hs.SetMaximum(10**8); hs.SetMinimum(0.1)#2016
hs.Draw()
hs.GetYaxis().SetLabelSize(0.08)
hs.GetXaxis().SetLabelSize(0)
hs.GetXaxis().SetTickSize(0)
hs.GetXaxis().SetTitle('')
hs.GetYaxis().SetTitle('event count/0.1')
hs.GetYaxis().SetTitleSize(0.08)
hs.GetYaxis().SetTitleOffset(0.9)
#'''
pad1.SetLogy()

h_err = h_sumbkg.Clone()
h_err.SetFillColor(Colormap["All_unc"])  # Set grey colour (12) and alpha (0.3)
h_err.SetMarkerSize(0)
h_err.SetFillStyle(3001)
h_err.Draw("E2SAME")

#h_sumbkg.SetFillColor(ROOT.TColor.GetColor(100, 192, 232))
#h_sumbkg.Draw("same hist")
#legend.AddEntry(h_bkg, "Total Background", "F")

h_sig.SetLineColor(TColor.GetColor('#1b9e77'))#ROOT.kRed)#a96b59,#e76300
h_sig.SetLineWidth(3)
h_sig.Draw("same hist")

h_sig_2.SetLineColor(TColor.GetColor('#b9ac70'))#ROOT.kRed)
h_sig_2.SetLineWidth(3)
h_sig_2.Draw("same hist")

for i in range(gr_dat.GetN()):
    gr_dat.SetPointEXlow(i, 0)
    gr_dat.SetPointEXhigh(i, 0)

gr_dat.SetMarkerStyle(ROOT.kFullCircle)
gr_dat.SetMarkerSize(1.5)
gr_dat.Draw("P same")

legend.AddEntry(gr_dat, "data", "ep")
for proc in reversed(bkg_proc_sorted): legend.AddEntry(bkg_hists[proc], bkg_legends[proc], "F")
legend.AddEntry(h_err, "Sys uncertainty", "F")# Bkg. Postfit # stat not included in grey band 
legend.AddEntry(h_sig, "m_{Z'}=1GeV; m_{DM}=150GeV; m_{med}=3TeV", "L")
legend_2 = rt.TLegend(x1-0.05-0.08,y1-0.2-0.02-0.02,x2-0.05-0.09,y1-0.2-0.02)
legend_2.SetTextSize(0.05)
legend_2.SetNColumns(2)
legend_2.AddEntry(h_sig_2, "m_{Z'}=1GeV; m_{DM}=%sGeV; m_{med}=2TeV"%(Mx_sig2), "L")#x10^{5}
#legend.GetListOfPrimitives().At(9).SetY1(legend.GetY1() - 0.1)
#legend.GetListOfPrimitives().At(9).SetX1(legend.GetX1() - 0.1)
#h_sumbkg.SetMaximum(h_sumbkg.GetMaximum() * 1.4)

legend.Draw("same");texCMS.Draw("same");texCMS_2.Draw("same"); texLumi.Draw("same");
legend_2.Draw("same")
#CMS.SetExtraText("Preliminary")
#CMS.SetLumi("%s"%lumi_map[year])
#canv = CMS.cmsCanvas('', 0, 1, 0, 1, '', '', square = CMS.kSquare, extraSpace=0.01, iPos=11)
#CMS.CMS_lumi(pad1)
### ratio

c1.cd()
pad2 = rt.TPad("pad2","pad2",0,0,1,0.3)
#pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.001)
pad2.SetBottomMargin(0.3)
ratio_nom = h_dat.Clone("ratio_nom")
ratio_nom.Divide(h_test)# using h_test instead of h_sumbkg so that the errors in sumb bakg aren't included(they are part of grey band anyways)
ratio_nom.SetMarkerSize(1.5)
ratio_nom.Draw("E")
ratio_nom.SetTitle("")
ratio_nom.GetYaxis().SetTitle("Data/Exp.")
ratio_nom.GetYaxis().SetTitleSize(0.15)
ratio_nom.GetYaxis().SetTitleOffset(0.4)
ratio_nom.GetYaxis().SetRangeUser(0.3,1.7)#(0.5,1.5)#(0.1,2)#
ratio_nom.GetYaxis().SetLabelSize(0.12)
ratio_nom.GetYaxis().SetNdivisions(6)
ratio_nom.GetXaxis().SetLabelSize(0.15)
ratio_nom.GetXaxis().SetTitle("ML output")
ratio_nom.GetXaxis().SetTitleSize(0.15)
ratio_nom.GetXaxis().SetTitleOffset(0.7)
#ratio_nom.GetXaxis().SetLabelPrecision(1)
h_sumbkg_up = get_sum_bkg_var(h_sumbkg,"up")
h_sumbkg_dn = get_sum_bkg_var(h_sumbkg,"dn")
ratio_band = get_unc_band_from_bounds(h_sumbkg_up,h_sumbkg_dn,h_sumbkg,ratioplot=True)
UncBandStyle(ratio_band,color=Colormap["All_unc"])
ratio_band.Draw('2same') 
#ratio_err = ratio.Clone()
#ratio_err.SetFillColorAlpha(12,0.3)  # Set grey colour (12) and alpha (0.3)
#ratio_err.SetMarkerSize(0)
#ratio_err.Draw("E2SAME")

c1.SaveAs("prefit_with_updates_%s_paper.pdf"%second_dir)
c1.SaveAs("prefit_with_updates_%s_paper.png"%second_dir)
