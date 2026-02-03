from ROOT import TH2D,TGraph,TGraphAsymmErrors,TMultiGraph,TCanvas,TLegend,TLatex,TLine,kRed, kGreen, kYellow,gStyle,gROOT
from array import *
import ctypes

mx = 150 #GeV

#Axial full lumi
limits_dict_axial = {# for mx=150 # run2
#Mphi/Mv: {limits}
  "2000.0": {
    "exp+1": 0.042607445269823074,
    "exp+2": 0.06021954491734505,
    "exp-1": 0.02031731605529785,
    "exp-2": 0.01535797119140625,
    "exp0": 0.02978515625,
    "obs": 0.031159158271750042
  },
  "3000.0": {
    "exp+1": 0.17776177823543549,
    "exp+2": 0.25009575486183167,
    "exp-1": 0.08651062846183777,
    "exp-2": 0.06415176391601562,
    "exp0": 0.12255859375,
    "obs": 0.1335148603840326
  },
  "4000.0": {
    "exp+1": 0.8927227258682251,
    "exp+2": 1.2578991651535034,
    "exp-1": 0.4356551170349121,
    "exp-2": 0.32305908203125,
    "exp0": 0.6171875,
    "obs": 0.6839545733530398
  },
  "5000.0": {
    "exp+1": 4.441012859344482,
    "exp+2": 6.238527297973633,
    "exp-1": 2.1672463417053223,
    "exp-2": 1.60711669921875,
    "exp0": 3.0703125,
    "obs": 3.3724309556618395
  }
}

#Vector full lumi
limits_dict_vector = {# for mx=150 # run2
#Mphi/Mv: {limits}
  "2000.0": {
    "exp+1": 0.04284319281578064,
    "exp+2": 0.05982353165745735,
    "exp-1": 0.02087116241455078,
    "exp-2": 0.015106201171875,
    "exp0": 0.029296875,
    "obs": 0.03084891732990638
  },
  "3000.0": {
    "exp+1": 0.18130286037921906,
    "exp+2": 0.2550777494907379,
    "exp-1": 0.08823394775390625,
    "exp-2": 0.0654296875,
    "exp0": 0.12499999999999999,
    "obs": 0.13792202706095807
  },
  "4000.0": {
    "exp+1": 0.9322737455368042,
    "exp+2": 1.3136287927627563,
    "exp-1": 0.4525566101074219,
    "exp-2": 0.337371826171875,
    "exp0": 0.64453125,
    "obs": 0.7154944231000852
  },
  "5000.0": {
    "exp+1": 5.4467387199401855,
    "exp+2": 7.6513237953186035,
    "exp-1": 2.658047676086426,
    "exp-2": 1.9710693359375,
    "exp0": 3.765625,
    "obs": 4.1864764288390734
  }
}

mediator = 'A'#A,V
if(mediator=='V'): limits_dict = limits_dict_vector
elif(mediator=='A'): limits_dict = limits_dict_axial

limit_keys = ['exp0','exp-1','exp-2','exp+1','exp+2','obs']#'exp1','exp2',
xlist = []; ylist = []; ylist_exp_minus1 = [] ; ylist_exp_minus2 = [] ; ylist_exp_plus1 = [] ; ylist_exp_plus2 = []; ylist_obs = []
for mv in limits_dict.keys():
        x = float(mv); y = limits_dict[mv]['exp0']; y_exp_minus1 = limits_dict[mv]['exp-1']; y_exp_minus2 = limits_dict[mv]['exp-2']; y_exp_plus1 = limits_dict[mv]['exp+1']; y_exp_plus2 = limits_dict[mv]['exp+2']; y_obs = limits_dict[mv]['obs']
        print("x=%s,y=%s,y_exp_minus1=%s,y_exp_minus2=%s,y_exp_plus1=%s,y_exp_plus2=%s,y_obs=%s"%(x,y,y_exp_minus1,y_exp_minus2,y_exp_plus1,y_exp_plus2,y_obs))#;raw_input("load next?")
        xlist.append(x); ylist.append(y); ylist_exp_minus1.append(y_exp_minus1); ylist_exp_minus2.append(y_exp_minus2); ylist_exp_plus1.append(y_exp_plus1); ylist_exp_plus2.append(y_exp_plus2); ylist_obs.append(y_obs)

xlist = array('d',xlist)
ylists= [ylist,ylist_exp_minus1,ylist_exp_minus2,ylist_exp_plus1,ylist_exp_plus2,ylist_obs]
merged_list = list(zip(ylists,limit_keys))
print(merged_list)#;raw_input("lol")
limits_to_plot = {}
for i, my_list in enumerate(ylists):
        my_list = array('d',my_list); print(type(my_list))
        my_tag = merged_list[i][-1]; print(my_tag)#;raw_input("ok?")
        limits_to_plot[my_tag] = TGraph(len(xlist),xlist,my_list)

def get_band(up_y,down_y,name,xlist=xlist,central_y=array('d',ylist)):
        print("####") ; print(up_y) ; print("####")
        print("####") ; print(down_y) ; print("####")
        print("####") ; print(name) ; print("####")
        print("####") ; print(xlist) ; print("####")
        print("####") ; print(central_y) ; print("####")
        yvals_lo = [a_i - b_i for a_i,b_i in zip(central_y,down_y)]
        yvals_hi = [a_i - b_i for a_i,b_i in zip(up_y,central_y)]
        print("$$$$") ; print(yvals_lo) ; print("$$$$")
        print("$$$$") ; print(yvals_hi) ; print("$$$$")
        limits_to_plot[name] = TGraphAsymmErrors(len(xlist),xlist,central_y,array('d', [0]),array('d', [0]),array('d', yvals_lo), array('d', yvals_hi)); limits_to_plot[name].Sort()

get_band(ylist_exp_plus1,ylist_exp_minus1,'exp1')    
get_band(ylist_exp_plus2,ylist_exp_minus2,'exp2')      

outdir_base = './'
def make_plot(limits_to_plot,mx):
        print("Plotting 1D_1param for mchi= ", mx)
        year = 'Run2'#'2018'#'2016'#'Run2'
        print(limits_to_plot) 
        class Bounds:
                def __init__(self):
                        self.xmax = None
                        self.xmin = None
                        self.ymax = None
                        self.ymin = None
                def setBounds(self,x,y):
                        if self.xmax is None: self.xmax = x
                        if self.xmin is None: self.xmin = x
                        if self.ymax is None: self.ymax = y
                        if self.ymin is None: self.ymin = y

                        self.xmax = max(self.xmax,x)
                        self.xmin = min(self.xmin,x)
                        self.ymax = max(self.ymax,y)
                        self.ymin = min(self.ymin,y)
                def getBounds(self): return self.xmin,self.xmax,self.ymin,self.ymax
                def __str__(self): return 'x: [%f-%f] y: [%f-%f]' % (self.xmin,self.xmax,self.ymin,self.ymax)
        bounds = Bounds()
        for graph_type,graph in limits_to_plot.items():
                x,y = ctypes.c_double(0),ctypes.c_double(0)
                for i in range(graph.GetN()):
                        graph.GetPoint(i,x,y)
                        bounds.setBounds(x.value,y.value)

        minX,maxX,minY,maxY = bounds.getBounds()
        print(bounds)
        ######################################################################
        draw=['exp2', 'exp1', 'exp0', 'obs']
        #draw=['exp-2', 'exp-1', 'exp0','exp+1', 'exp+2', 'obs']
        style_dict = {
                'obs' : { 'LineWidth' : 2, 'LineStyle': 9, 'MarkerSize': 1.5 ,'MarkerStyle': 20},
                'exp0' : { 'LineWidth' : 2, 'LineColor' : kRed, 'LineStyle': 1, 'MarkerSize': 2 ,'MarkerStyle': 3},
                'exp1' : { 'FillColor' : kGreen},
                'exp2' : { 'FillColor' : kYellow},
                'exp-1' : { 'LineWidth' : 2, 'LineColor' : kGreen, 'LineStyle': 1},
                'exp+1' : { 'LineWidth' : 2, 'LineColor' : kGreen, 'LineStyle': 1},
                'exp-2' : { 'LineWidth' : 2, 'LineColor' : kYellow, 'LineStyle': 1},
                'exp+2' : { 'LineWidth' : 2, 'LineColor' : kYellow, 'LineStyle': 1}
        }

        legend_dict = {
                'obs' : { 'Label' : 'Observed', 'LegendStyle' : 'LP', 'DrawStyle' : 'PLSAME'},
                'exp0' : { 'Label' : 'Expected', 'LegendStyle' : 'LP', 'DrawStyle' : 'PLSAME'},
                'exp1' : { 'Label' : '#pm1#sigma Expected', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'},
                'exp2' : { 'Label' : '#pm2#sigma Expected', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'},
                'exp-1' : { 'Label' : '-1 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'},
                'exp+1' : { 'Label' : '+1 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'},
                'exp-2' : { 'Label' : '-2 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'},
                'exp+2' : { 'Label' : '+2 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'}

        }

        c = TCanvas("c","c",800,800)
        c.SetLogy()#; c.SetLogx()
        # c.SetMargin(0.15,0.15,0.15,0.08)
        gStyle.SetOptStat(0);
        gStyle.SetLegendBorderSize(0);
        # gStyle.SetPalette(kRainBow)

        limits = TMultiGraph()
        legend = TLegend(0.6,0.2,0.9,0.5,"")#x1,y1,x2,y2
        legend.SetTextSize(0.02)
        legend.SetFillColor(0)
        for key in draw:
                if key in limits_to_plot:
                        print(key)#; raw_input("lol?")
                        limits_to_plot[key].Sort()
                        legend.AddEntry(limits_to_plot[key],legend_dict[key]['Label'],legend_dict[key]['LegendStyle'])
                        if 'LineWidth' in style_dict[key]: limits_to_plot[key].SetLineWidth(style_dict[key]['LineWidth'])
                        if 'LineColor' in style_dict[key]: limits_to_plot[key].SetLineColor(style_dict[key]['LineColor'])
                        if 'FillColor' in style_dict[key]: limits_to_plot[key].SetFillColor(style_dict[key]['FillColor'])
                        if 'LineStyle' in style_dict[key]: limits_to_plot[key].SetLineStyle(style_dict[key]['LineStyle'])
                        if 'MarkerSize' in style_dict[key]: limits_to_plot[key].SetMarkerSize(style_dict[key]['MarkerSize'])
                        if 'MarkerStyle' in style_dict[key]: limits_to_plot[key].SetMarkerStyle(style_dict[key]['MarkerStyle'])
                        limits.Add(limits_to_plot[key],legend_dict[key]['DrawStyle'])

        limits.Draw('a')
        limits.GetXaxis().SetLimits(minX,maxX) #limits.GetXaxis().SetRangeUser(minX,maxX)
        limits.GetYaxis().SetRangeUser(0.8*10**-4,2*10**1) #SetRangeUser(10**-3.5,10**5.5)
        limits.GetXaxis().SetTitle("m_{med} (GeV)")
        limits.GetYaxis().SetTitle("95% CL limit on #sigma/#sigma_{theory}")
        limits.GetXaxis().SetTitleSize(0.04)
        limits.GetYaxis().SetTitleSize(0.04)
        limits.GetXaxis().SetTitleOffset(0.92)
        limits.GetYaxis().SetTitleOffset(0.92)
        limits.GetXaxis().SetLabelSize(0.03)
        limits.GetYaxis().SetLabelSize(0.03)            
        ################################################################

        lumi_label = '137.5 fb^{-1}'#'%s' % float('%.3g' % (lumi/1000.)) + " fb^{-1}"# 137.5, 36.3, 41.5,
        texS = TLatex(0.20,0.837173,("#sqrt{s} = 13 TeV, "+lumi_label+", m_{DM}=%s GeV"%mx));
        texS.SetNDC();
        texS.SetTextFont(42);
        texS.SetTextSize(0.040);
        texS.Draw('same');
        if(mediator=='V'):  texS1 = TLatex(0.12092,0.907173,"#bf{CMS} : #it{Preliminary} (%s) -- Vector Mediator, m_{Z'} = 1 GeV" % year)
        elif(mediator=='A'): texS1 = TLatex(0.12092,0.907173,"#bf{CMS} : #it{Preliminary} (%s) -- Axial Mediator, m_{Z'} = 1 GeV" % year)
        texS1.SetNDC();
        texS1.SetTextFont(42);
        texS1.SetTextSize(0.040);
        texS1.Draw('same');

        legend.Draw('same')

        line = TLine(minX,1,maxX,1)
        line.SetLineStyle(8)
        line.Draw('same')

        c.Modified()
        c.Update()
        gROOT.GetListOfCanvases().Draw()
        outdir = outdir_base# % year
        if(mediator=='V'): fname = 'limits_%s_1D_vector_Zprime1GeV_mchi=%sGeV_fitbased_with_observed_fulllumi.png'%(year,mx)
        elif(mediator=='A'): fname = 'limits_%s_1D_axial_Zprime1GeV_mchi=%sGeV_fitbased_with_observed_fulllumi.png'%(year,mx)
        c.SaveAs( '%s/%s' % (outdir,fname) )

make_plot(limits_to_plot,mx)        
