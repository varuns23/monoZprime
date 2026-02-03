from ROOT import TGraphErrors,TGraphAsymmErrors, TMath
from array import array
import ctypes

def get_unc_band_from_bounds(up_bound,low_bound,nominal,ratioplot=False):
    xbins = nominal.GetNbinsX(); xbins_up = up_bound.GetNbinsX(); xbins_low = low_bound.GetNbinsX()
    if not((xbins==xbins_up) and (xbins==xbins_low)): 
        print("Returning due to unequal # of bins")
        print("Nominal bins=%s, up_bound_bins=%s, low_bound_bins=%s\n"%(xbins,xbins_up,xbins_low))
        return
    x = []; y = []; ex = []; ey_low = []; ey_up = []
    nbins = 0
    for ibin in range(1,xbins+1):# 0=underflow,xbins+1=overflow
        #print("&&&&&&&&&&&&&&&&&&ibin=%s&&&&&&&&&&&&&"%ibin)
        y_nom = nominal.GetBinContent(ibin); y_low_tmp = low_bound.GetBinContent(ibin); y_up_tmp = up_bound.GetBinContent(ibin)
        if( (y_low_tmp == y_nom) and (y_up_tmp == y_nom)): continue# this means no room to move
        if( (y_nom == 0)): continue# this means no room to move
        x.append(up_bound.GetBinCenter(ibin)) # can take any of the hist as all have same
        ex.append(up_bound.GetBinWidth(ibin)/2)# ex_low = ex_up = ex
        if(y_low_tmp<0): raw_input("y_low_tmp<0 = %s for bin =%s"%(y_low_tmp,ibin))
        if(y_up_tmp<0): raw_input("y_up_tmp<0 = %s for bin =%s"%(y_up_tmp,ibin))
        y_low = min(y_low_tmp,y_up_tmp); y_up = max(y_low_tmp,y_up_tmp) # as it can happen that y_low > y_up(in case of dense band: y_low < y_up always), we are only interested in band, so can swap
        #print("ylow=%s;y_up=%s;y_nom=%s"%(y_low,y_up,y_nom))
        y_low = y_nom-y_low; y_up = y_up-y_nom
        if(ratioplot): 
                #y_nom = 1 
                y_low=y_low/y_nom; y_up=y_up/y_nom; y_nom= y_nom/y_nom
                #y_low,y_up = y_up,y_low# up and down flipped because we are plotting data/mc and not mc/data in ratio--already taken care by taking low as min and up as max of the low_tmp and up_tmp values!
                #print("center_to_one: ylow=%s;y_up=%s;y_nom=%s"%(y_low,y_up,y_nom))
        y.append(y_nom); ey_low.append(y_low); ey_up.append(y_up)
        nbins += 1
        #print(low_bound.GetBinContent(ibin)); print(up_bound.GetBinContent(ibin))
        #print(y_low_tmp); print(y_up_tmp)
    #print("xbins=%s, nbins=%s"%(xbins,nbins))  # both should be same  
    #print(ey_low)
    #print(y)
    #print(ey_up)
    #for i in range(len(y)):
    #    print("%s,%s"%(ey_low[i]/y[i],ey_up[i]/y[i]))
    return TGraphAsymmErrors(nbins,array('d',x),array('d',y),array('d',ex),array('d',ex),array('d',ey_low),array('d',ey_up))  

lumi_map  = {
        '2016':'36.3',
        '2017':'41.5',
        '2018':'59.7',
}

sorted_proc_order = {
        '2016':['DYJets', 'Top', 'DiBoson', 'QCD', 'WJets', 'ZJets'],
        '2017':['Top','DYJets', 'DiBoson', 'QCD', 'WJets', 'ZJets'],
        '2018':['DYJets', 'Top', 'DiBoson', 'QCD', 'WJets', 'ZJets'],
}

def get_sum_bkg_var(h_sumbkg,var):
        h_var = h_sumbkg.Clone()
        h_var.Reset()
        xbins = h_var.GetNbinsX()
        for ibin in range(1,xbins+1):# 0=underflow,xbins+1=overflow
              if(var=="up"): val = h_sumbkg.GetBinContent(ibin) + h_sumbkg.GetBinError(ibin)
              elif(var=="dn"): val = h_sumbkg.GetBinContent(ibin) - h_sumbkg.GetBinError(ibin)
              h_var.SetBinContent(ibin,val) 
        if (h_var.GetSumw2N() == 0): h_var.Sumw2(rt.kTRUE)          
        return h_var     

def get_new_ticks(hist):
        for ibin in range(1,hist.GetNbinsX()+1): 
                tmp_ibin = f"{0.1*ibin:.1f}"
                label = "  %s"%str(tmp_ibin)
                hist.GetXaxis().SetBinLabel(ibin,label)
                hist.GetXaxis().SetLabelSize(0.3)
                #hist.GetXaxis().LabelsOption("R")
        return hist


def makeHistogram(graph,template):
    hs = template.Clone()
    hs.Reset()
    npoints = graph.GetN()
    for i in range(npoints):
        x,y=ctypes.c_double(0),ctypes.c_double(0)
        graph.GetPoint(i,x,y)
        xerr = graph.GetErrorX(i)
        yerr = graph.GetErrorY(i)
        hs.SetBinContent(i+1,y)
        hs.SetBinError(i+1,yerr)
    if (hs.GetSumw2N() == 0): hs.Sumw2(rt.kTRUE)    
    return hs

def check_hist(hist_1,hist_2):
        xbins = hist_1.GetNbinsX()
        for ibin in range(1,xbins+1):
                x = hist_1[ibin] - hist_2[ibin]
                print("ibin=%s,x=%s"%(ibin,x))

def print_bin_errors(hist):
        xbins = hist.GetNbinsX()
        for ibin in range(1,xbins+1):
                x = hist.GetBinError(ibin)
                print("ibin=%s,bin error=%s"%(ibin,x))                        