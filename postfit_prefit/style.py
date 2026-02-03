#!/usr/bin/env python
import ROOT as rt
from ROOT import TColor, kBlack, kBlue, kRed, kGreen, kMagenta, kYellow, kOrange, kGray

def getCMSTex(x=0.16,y=0.95,scale=1,text="#bf{CMS}",text_2="#it{Preliminary}"):#Private Work(#bf{CMS} #it{Data/Simulation})
    texCMS = rt.TLatex(x,y,text); 
    texCMS.SetNDC();
    texCMS.SetTextFont(42);
    texCMS.SetTextSize(0.060*scale);

    texCMS_2 = rt.TLatex(x+0.1,y,text_2); 
    texCMS_2.SetNDC();
    texCMS_2.SetTextFont(42);
    texCMS_2.SetTextSize(0.060*scale);

    return texCMS,texCMS_2

def getLumiTex(lumi_label,year,x=0.67,y=0.95,scale=3,text="%s (13 TeV%s)"):
    texLumi = rt.TLatex(x,y,text % (lumi_label,year))
    texLumi.SetNDC()
    texLumi.SetTextFont(42)
    texLumi.SetTextSize(0.060*scale)
    return texLumi

def getCMSText(lumi_label,year,scale=1):
    texS = getLumiTex(lumi_label,year,scale=scale)
    texS.Draw();
    texS1 = getCMSTex(scale=scale)
    texS1.Draw();

    return texS,texS1

def get_custom_range(hist,my_var):
        (xmin,xmax)= (hist.GetXaxis().GetXmin(),hist.GetXaxis().GetXmax())
        if 'Associatedfatjet_mass' in my_var : (xmin,xmax)=(0,300)
        elif (('Associatedfatjet_msoftdrop'  in my_var) and 'corr' not in my_var) : (xmin,xmax)=(0,200)
        elif 'subjet_mass' in my_var : (xmin,xmax)=(0,60)
        elif 'HPSJet_mass' in my_var : (xmin,xmax)=(0,10)
        elif 'Associatedjet_mass' in my_var : (xmin,xmax)=(0,200)
        #elif 'recoil' in my_var : (xmin,xmax)=(0,1500)
        elif 'HPSJet_decaymode' in my_var : (xmin,xmax)=(0,18)
        elif my_var in ['Associatedfatjet_tau1','Associatedfatjet_tau2bytau1','Associatedfatjet_tau3bytau2','subjet_tau2bytau1']: (xmin,xmax)=(0,2)
        elif any([x in my_var for x in['subjet_tau1','subjet_tau2','subjet_tau3','subjet_tau4','Associatedfatjet_tau2','Associatedfatjet_tau3','Associatedfatjet_tau4']]): (xmin,xmax)=(0,0.5)
        elif my_var in ['leadTkPtOverAssociatedJetPt']: (xmin,xmax)=(0,1.4)
        elif my_var in ['recoil','recoil_after_siglike_cut_sig','recoil_after_siglike_cut_bkg']: (xmin,xmax)=(250,1200)
        elif(my_var=='dphi_HPSJet_recoil'): (xmin,xmax)=(0,4.0)
        elif(my_var=='HPSJet_leadTkPtOverhpsPt'): (xmin,xmax)=(0,1.5)
        elif(my_var=='HPSJet_leadTkDeltaR'): (xmin,xmax)=(0,0.15)
        elif(my_var=='HPSJetPtOverAssociatedJetPt'): (xmin,xmax)=(0,2.1)
        elif(my_var=='HPSJet_AssociatedJet_DeltaR'): (xmin,xmax)=(0,0.4)
        elif(my_var=='Associatedjet_chHEF'): (xmin,xmax)=(0,1.1)
        #elif('s2_cutflow' in my_var) : (xmin,xmax)=(5,18); hist.SetMaximum(2*10**5)#hist.GetYaxis().SetRangeUser(0,hist.GetMaximum()*1.2)
        elif ('_sig_like' in my_var): (xmin,xmax)=(0,1.2)
        hist.GetXaxis().SetRangeUser(xmin,xmax)
        return xmin,xmax

def get_minimum_plotvar(my_var):
        if(my_var=='recoil'): min_y_value = 0.1
        elif(my_var=='dphi_HPSJet_recoil'): min_y_value  = 0.1
        elif('xgb_rsc_contin' in my_var): min_y_value = 0.1
        elif('varZ_' in my_var): min_y_value  = 10 # dense vars
        elif(my_var=='HPSJet_leadTkPtOverhpsPt'): min_y_value  = 0.1
        elif(my_var=='HPSJet_leadTkDeltaR'): min_y_value  = 0.1
        elif(my_var=='HPSJet_mass'): min_y_value  = 0.1
        elif(my_var=='leadTkPtOverAssociatedJetPt'): min_y_value  = 0.1
        elif(my_var=='HPSJetPtOverAssociatedJetPt'): min_y_value  = 0.1
        elif(my_var=='HPSJet_AssociatedJet_DeltaR'): min_y_value  = 0.1
        elif(my_var=='Associatedjet_chHEF'): min_y_value  = 0.1
        elif(my_var=='Associatedjet_neEmEF'): min_y_value  = 0.1
        elif(my_var=='Associatedjet_neHEF'): min_y_value  = 0.1
        elif(my_var=='Associatedjet_mass'): min_y_value  = 0.1
        else: min_y_value  = 0.1
        return min_y_value            

#https://cms-analysis.docs.cern.ch/guidelines/plotting/colors/#categorical-data-eg-1d-stackplots
Colormap = { 
        "Mx1_Mv1000": TColor.GetColor('#bd1f01'),
        "Mx1_Mv2000": TColor.GetColor('#bd1f01'),
        "Mx1_Mv3000": TColor.GetColor('#bd1f01'),
        "Mx1_Mv4000": TColor.GetColor('#bd1f01'),
        "Mx1_Mv5000": TColor.GetColor('#bd1f01'),
        "Mx10_Mv3000":TColor.GetColor('#bd1f01'),
        "Mx50_Mv3000":TColor.GetColor('#bd1f01'),
        "Mx150_Mv3000":TColor.GetColor('#bd1f01'),
        "Mx500_Mv3000":TColor.GetColor('#bd1f01'),
        "Mx800_Mv3000":TColor.GetColor('#bd1f01'),
        "Mx1000_Mv3000": TColor.GetColor('#bd1f01'),
        "Mx1000_Mv4000": TColor.GetColor('#bd1f01'),
        "Mx1000_Mv5000": TColor.GetColor('#bd1f01'),
        "Z1Jets":TColor.GetColor('#5790fc'),#  #3f90da
        "Z2Jets":TColor.GetColor('#5790fc'),
        "ZJets":TColor.GetColor('#5790fc'),
        "WJets":TColor.GetColor('#f89c20'), # #ffa90e
        "GJets":TColor.GetColor('#832db6'),
        "QCD":TColor.GetColor('#9c9ca1'),# #94a4a2
        "DYJets":TColor.GetColor('#964a8b'),# #a96b59
        "DY1Jets":TColor.GetColor('#964a8b'),
        "DY2Jets":TColor.GetColor('#964a8b'),
        "Top":TColor.GetColor('#e42536'),# #b9ac70
        "DiBoson":TColor.GetColor('#7a21dd'),# #92dadd
        "Data":kBlack,
        "SumBkg": kGray,
        "Theory_unc": 13,
        "Stat_unc" :12,
        "Exp_unc": 14, 
        "All_unc": TColor.GetColor("#D3D3D3"),#medium:TColor.GetColor("#C0C0C0"),#dark: TColor.GetColor('#717581'),                                                           
}
other_sig_masses = ['Mx500_Mv1500', 'Mx800_Mv5000', 'Mx150_Mv5000', 'Mx10_Mv4000', 'Mx10_Mv2000', 'Mx1000_Mv4000', 'Mx50_Mv5000', 'Mx500_Mv5000', 'Mx150_Mv1000', 'Mx1000_Mv5000', 'Mx50_Mv2000', 'Mx500_Mv4000', 'Mx10_Mv1000', 'Mx500_Mv2000', 'Mx10_Mv5000', 'Mx50_Mv4000', 'Mx800_Mv2000', 'Mx150_Mv2000', 'Mx50_Mv1000', 'Mx800_Mv4000', 'Mx150_Mv4000']        
for other_Zprime_mass in other_sig_masses: Colormap[other_Zprime_mass] = TColor.GetColor('#bd1f01')
QBH_masses = ['M1000', 'M3000', 'M8000', 'M1200', 'M2800', 'M1800', 'M9000', 'M10000', 'M2000', 'M7000', 'M400', 'M2200', 'M3500', 'M2600', 'M600', 'M1400', 'M2400', 'M4500', 'M5000', 'M11000', 'M6000', 'M1600', 'M800', 'M4000']
for QBH_mass in QBH_masses: Colormap[QBH_mass] = TColor.GetColor('#bd1f01')


def get_legend_coords_location_based(leg_loc):
        if(leg_loc=='left') : x1 = 0.1 ;  x2 = 0.5; y1 = 0.7 ; y2 = 0.9 
        elif(leg_loc=='left_large') : x1 = 0.15 ;  x2 = 0.45; y1 = 0.15 ; y2 = 0.85
        elif(leg_loc=='center') : x1=0.3 ;  x2=0.7; y1=0.5 ; y2=0.9 
        #elif(leg_loc=='center_small'): x1=0.3 ;  x2=0.7; y1=0.5 ; y2=0.9 
        elif(leg_loc=='right') : x1=0.3 ;  x2=0.9; y1=0.7 ; y2=0.9
        elif(leg_loc=='right_small') : x1=0.7 ;  x2=0.9; y1=0.7 ; y2=0.9
        return [x1,x2,y1,y2]

def get_legend_coords(leg_loc,my_var):
        if(my_var=='recoil'): x1=0.5 ;  x2=0.9; y1=0.5 ; y2=0.9
        elif(my_var=='dphi_HPSJet_recoil'): x1 = 0.2 ;  x2 = 0.5; y1 = 0.5 ; y2 = 0.9 
        elif('varZ_' in my_var): [x1,x2,y1,y2] = get_legend_coords_location_based(leg_loc) # dense vars
        elif(my_var=='HPSJet_leadTkPtOverhpsPt'): x1=0.7 ;  x2=0.9; y1=0.1 ; y2=0.9
        elif(my_var=='HPSJet_leadTkDeltaR'): x1=0.5 ;  x2=0.9; y1=0.5 ; y2=0.9
        elif(my_var=='HPSJet_mass'): x1=0.5 ;  x2=0.9; y1=0.5 ; y2=0.9
        elif(my_var=='leadTkPtOverAssociatedJetPt'): x1=0.7 ;  x2=0.9; y1=0.1 ; y2=0.9
        elif(my_var=='HPSJetPtOverAssociatedJetPt'): x1=0.5 ;  x2=0.9; y1=0.5 ; y2=0.9
        elif(my_var=='HPSJet_AssociatedJet_DeltaR'): x1=0.5 ;  x2=0.9; y1=0.5 ; y2=0.9
        elif(my_var=='Associatedjet_chHEF'): x1=0.2 ;  x2=0.6; y1=0.6 ; y2=0.9 
        elif(my_var=='Associatedjet_neEmEF'): x1=0.5 ;  x2=0.9; y1=0.55 ; y2=0.9 
        elif(my_var=='Associatedjet_neHEF'): x1=0.5 ;  x2=0.9; y1=0.55 ; y2=0.9 
        elif(my_var=='Associatedjet_mass'): x1=0.5 ;  x2=0.9; y1=0.5 ; y2=0.9
        else:        
                [x1,x2,y1,y2] = get_legend_coords_location_based(leg_loc)
        return [x1,x2,y1,y2]

def UncBandStyle(uncband,color=33):
    uncband.SetTitle("")
    uncband.SetFillStyle(3001)#3144)
    #uncband.SetFillStyle(2001)
    uncband.SetFillColor(color)

    uncband.SetMarkerStyle(1)
    uncband.SetMarkerSize(0)
    uncband.SetLineColor(0)
    uncband.SetLineWidth(0)

def get_norm_yrange(hist,my_var):
        (ymin,ymax)= (0,1.2)
        if (my_var=="HPSJet_mass"): ymax = 0.6
        elif(my_var=="HPSJet_leadTkPtOverhpsPt"): ymax = 0.3
        elif(my_var=="HPSJet_leadTkDeltaR"): ymax = 1.2   
        elif(my_var=="Associatedjet_chHEF"): ymax = 0.2
        elif(my_var=="Associatedjet_neHEF"): ymax = 0.5
        elif(my_var=="Associatedjet_neEmEF"): ymax = 0.4
        elif(my_var=="Associatedjet_mass"): ymax = 0.6
        elif(my_var=="Associatedjet_nConstituents"): ymax = 0.2
        elif(my_var=="leadTkPtOverAssociatedJetPt"): ymax = 0.2
        elif(my_var=="HPSJetPtOverAssociatedJetPt"): ymax = 0.6
        elif(my_var=="HPSJet_AssociatedJet_DeltaR"): ymax = 1.2
        elif(my_var=="dphi_HPSJet_recoil"): ymax = 0.4
        elif(my_var=="recoil"): ymax = 0.4
        elif('_sig_like' in my_var): ymax = 0.7   
        return ymin,ymax
