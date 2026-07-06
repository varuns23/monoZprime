#!/usr/bin/env python2
from ROOT import TH2D,TGraph,TGraphAsymmErrors,TMultiGraph,TCanvas,TLegend,TLatex,TLine,kRed, kGreen, kYellow,gStyle,gROOT, TColor
from array import *
import ctypes
import ROOT
mphi = 4000 #mphi = 4000 GeV

mediator = 'vector' # axial/vector

#Vector
if (mediator == 'vector'):
    limits_dict = {# for mphi=4000 # combined Run2
    #Mchi/Mx: {limits}
    #  "1.0": {
    #    "exp+1": 0.293102502822876,
    #    "exp+2": 0.4084193706512451,
    #    "exp-1": 0.14751136302947998,
    #    "exp-2": 0.11156310886144638,
    #    "exp0": 0.20546874403953552,
    #    "obs": 0.22052590829032542
    #  },
    #  "10.0": {
    #    "exp+1": 0.4135017693042755,
    #    "exp+2": 0.578970730304718,
    #    "exp-1": 0.20682859420776367,
    #    "exp-2": 0.15582275390625,
    #    "exp0": 0.2890625,
    #    "obs": 0.31007517601372697
    #  },
    #  "50.0": {
    #    "exp+1": 0.6293283104896545,
    #    "exp+2": 0.8812664747238159,
    #    "exp-1": 0.3109283447265625,
    #    "exp-2": 0.232421875,
    #    "exp0": 0.4375,
    #    "obs": 0.4775687768719478
    #  },
      "150.0": {
        "exp+1": 0.9421006441116333,
        "exp+2": 1.3213506937026978,
        "exp-1": 0.4641715884208679,
        "exp-2": 0.34697264432907104,
        "exp0": 0.653124988079071,
        "obs": 0.7196133535832563
      }, 
      "500.0": {
        "exp+1": 2.362013101577759,
        "exp+2": 3.333308458328247,
        "exp-1": 1.1558647155761719,
        "exp-2": 0.857128918170929,
        "exp0": 1.6375000476837158,
        "obs": 1.802457276458122
      },  
      "800.0": {
        "exp+1": 4.122344970703125,
        "exp+2": 5.808627605438232,
        "exp-1": 2.0117340087890625,
        "exp-2": 1.491796851158142,
        "exp0": 2.8499999046325684,
        "obs": 3.1235034877631644
      },   
      "1000.0": {
        "exp+1": 6.5631632804870605,
        "exp+2": 9.233814239501953,
        "exp-1": 3.1772217750549316,
        "exp-2": 2.3685548305511475,
        "exp0": 4.525000095367432,
        "obs": 4.8854999052207635
      },  
    }
elif(mediator == 'axial'):#Axial
    limits_dict = {# for mphi=4000 # combined Run2
    #Mchi/Mx: {limits}
    #  "1.0": {
    #    "exp+1": 0.3009037375450134,
    #    "exp+2": 0.41928985714912415,
    #    "exp-1": 0.1519460678100586,
    #    "exp-2": 0.1153564453125,
    #    "exp0": 0.2109375,
    #    "obs": 0.22482312738990826
    #  },  
    #  "10.0": {
    #    "exp+1": 0.4157746732234955,
    #    "exp+2": 0.5812801122665405,
    #    "exp-1": 0.20738758146762848,
    #    "exp-2": 0.15624389052391052,
    #    "exp0": 0.28984373807907104,
    #    "obs": 0.3101420656543189
    #  },
    #  "50.0": {
    #    "exp+1": 0.6158427000045776,
    #    "exp+2": 0.862382173538208,
    #    "exp-1": 0.3042655885219574,
    #    "exp-2": 0.22744140028953552,
    #    "exp0": 0.4281249940395355,
    #    "obs": 0.470546168425754
    #  },   
      "150.0": {
        "exp+1": 0.9060394167900085,
        "exp+2": 1.2707726955413818,
        "exp-1": 0.44410401582717896,
        "exp-2": 0.33369141817092896,
        "exp0": 0.628125011920929,
        "obs": 0.6869171320215889
      },
      "500.0": {
        "exp+1": 2.037461757659912,
        "exp+2": 2.8576579093933105,
        "exp-1": 0.9970436692237854,
        "exp-2": 0.7393555045127869,
        "exp0": 1.412500023841858,
        "obs": 1.5522482883469375
      }, 
      "800.0": {
        "exp+1": 4.013862133026123,
        "exp+2": 5.655769348144531,
        "exp-1": 1.9587936401367188,
        "exp-2": 1.452539086341858,
        "exp0": 2.7750000953674316,
        "obs": 3.024517802532775
      },  
      "1000.0": {
        "exp+1": 6.780726909637451,
        "exp+2": 9.539907455444336,
        "exp-1": 3.2825441360473633,
        "exp-2": 2.447070360183716,
        "exp0": 4.675000190734863,
        "obs": 5.11335917306175
      },                 
    }


ROOT.gStyle.SetTextFont(42)               # Default text font --42==helvetica
ROOT.gStyle.SetLabelFont(42, "X")         # X axis labels
ROOT.gStyle.SetLabelFont(42, "Y")         # Y axis labels
ROOT.gStyle.SetLabelFont(42, "Z")         # Z axis labels
ROOT.gStyle.SetTitleFont(42, "X")         # X axis title
ROOT.gStyle.SetTitleFont(42, "Y")         # Y axis title
ROOT.gStyle.SetTitleFont(42, "Z")         # Z axis title

limit_keys = ['exp0','exp-1','exp-2','exp+1','exp+2','obs']
xlist = []; ylist = []; ylist_exp_minus1 = [] ; ylist_exp_minus2 = [] ; ylist_exp_plus1 = [] ; ylist_exp_plus2 = []; ylist_obs = []
for mv in limits_dict.keys():
        x = float(mv); y = limits_dict[mv]['exp0']; y_exp_minus1 = limits_dict[mv]['exp-1']; y_exp_minus2 = limits_dict[mv]['exp-2']; y_exp_plus1 = limits_dict[mv]['exp+1']; y_exp_plus2 = limits_dict[mv]['exp+2']; y_obs = limits_dict[mv]['obs']
        xlist.append(x); ylist.append(y); ylist_exp_minus1.append(y_exp_minus1); ylist_exp_minus2.append(y_exp_minus2); ylist_exp_plus1.append(y_exp_plus1); ylist_exp_plus2.append(y_exp_plus2); ylist_obs.append(y_obs)

xlist = array('d',xlist)
ylists= [ylist,ylist_exp_minus1,ylist_exp_minus2,ylist_exp_plus1,ylist_exp_plus2,ylist_obs]
merged_list = list(zip(ylists,limit_keys))
limits_to_plot = {}
for i, my_list in enumerate(ylists):
        my_list = array('d',my_list); print(type(my_list))
        my_tag = merged_list[i][-1]; print(my_tag)
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
def make_plot(limits_to_plot, mediator, mphi):
        print (("Plotting 1D_1param for mphi=%s"%mphi))
        year = 'Run2'
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
                'obs' : { 'LineWidth' : 2, 'LineStyle': 1, 'MarkerSize': 1.2 ,'MarkerStyle': 20},
                'exp0' : { 'LineWidth' : 2, 'LineColor' : kRed, 'LineStyle': 1, 'MarkerSize': 0 ,'MarkerStyle': 4},
                'exp1' : { 'FillColor' : TColor.GetColor('#607641')},#kGreen
                'exp2' : { 'FillColor' : TColor.GetColor('#F5BB54')},#kYellow
                'exp-1' : { 'LineWidth' : 2, 'LineColor' : TColor.GetColor('#607641'), 'LineStyle': 1},#kGreen
                'exp+1' : { 'LineWidth' : 2, 'LineColor' : TColor.GetColor('#607641'), 'LineStyle': 1},#kGreen
                'exp-2' : { 'LineWidth' : 2, 'LineColor' : TColor.GetColor('#F5BB54'), 'LineStyle': 1},#kYellow
                'exp+2' : { 'LineWidth' : 2, 'LineColor' : TColor.GetColor('#F5BB54'), 'LineStyle': 1}#kYellow
        }

        legend_dict = {
                'obs' : { 'Label' : 'Observed', 'LegendStyle' : 'LP', 'DrawStyle' : 'PLSAME'},
                'exp0' : { 'Label' : 'Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'PLSAME'},
                'exp1' : { 'Label' : 'Expected (1 s.d.)', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'},##pm1#sigma
                'exp2' : { 'Label' : 'Expected (2 s.d.)', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'},##pm2#sigma 
                'exp-1' : { 'Label' : '-1 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'},
                'exp+1' : { 'Label' : '+1 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'},
                'exp-2' : { 'Label' : '-2 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'},
                'exp+2' : { 'Label' : '+2 sigma Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'}

        }

        gStyle.SetPadTickY(1)
        gStyle.SetOptStat(0);
        gStyle.SetLegendBorderSize(0);
        
        c = TCanvas("c","c",800,700)
        c.SetLogy()

        limits = TMultiGraph()
        legend = TLegend(0.52,0.14,0.82,0.44,"")#x1,y1,x2,y2
        legend.SetHeader("95% CL upper limits", "C")
        legend.SetTextSize(0.04)
        legend.SetFillColor(0)
        for key in draw:
                if key in limits_to_plot:
                        print(key)
                        limits_to_plot[key].Sort()
                        #legend.AddEntry(limits_to_plot[key],legend_dict[key]['Label'],legend_dict[key]['LegendStyle'])
                        if 'LineWidth' in style_dict[key]: limits_to_plot[key].SetLineWidth(style_dict[key]['LineWidth'])
                        if 'LineColor' in style_dict[key]: limits_to_plot[key].SetLineColor(style_dict[key]['LineColor'])
                        if 'FillColor' in style_dict[key]: limits_to_plot[key].SetFillColor(style_dict[key]['FillColor'])
                        if 'LineStyle' in style_dict[key]: limits_to_plot[key].SetLineStyle(style_dict[key]['LineStyle'])
                        if 'MarkerSize' in style_dict[key]: limits_to_plot[key].SetMarkerSize(style_dict[key]['MarkerSize'])
                        if 'MarkerStyle' in style_dict[key]: limits_to_plot[key].SetMarkerStyle(style_dict[key]['MarkerStyle'])
                        limits.Add(limits_to_plot[key],legend_dict[key]['DrawStyle'])

        legend.AddEntry(limits_to_plot['obs'],legend_dict['obs']['Label'],legend_dict['obs']['LegendStyle'])
        legend.AddEntry(limits_to_plot['exp0'],legend_dict['exp0']['Label'],legend_dict['exp0']['LegendStyle'])
        legend.AddEntry(limits_to_plot['exp1'],legend_dict['exp1']['Label'],legend_dict['exp1']['LegendStyle'])
        legend.AddEntry(limits_to_plot['exp2'],legend_dict['exp2']['Label'],legend_dict['exp2']['LegendStyle'])
        limits.Draw('a')
        limits.GetXaxis().SetLimits(minX,maxX) #limits.GetXaxis().SetRangeUser(minX,maxX)
        limits.GetYaxis().SetRangeUser(8*10**-2,2*10**1)#SetRangeUser(10**-3,2*10**1) #SetRangeUser(10**-3.5,10**5.5)
        limits.GetXaxis().SetRangeUser(1.5*10**2,10**3)
        limits.GetXaxis().SetTitle("m_{DM} [GeV]")
#        limits.GetYaxis().SetTitle("95% CL limit on #mu")
        ytitletext = ROOT.TLatex(0.04, 0.478, "95% CL upper limits on#kern[-0.5]{ }#mu")
        ytitletext.SetNDC()
        ytitletext.SetTextSize(0.04)
        ytitletext.SetTextFont(42)
        ytitletext.SetTextAngle(90)
        ytitletext.Draw()

        limits.GetXaxis().SetTitleSize(0.041)
        limits.GetYaxis().SetTitleSize(0.041)
        limits.GetXaxis().SetTitleOffset(0.99)
        limits.GetYaxis().SetTitleOffset(0.99)
        limits.GetXaxis().SetLabelSize(0.041)
        limits.GetYaxis().SetLabelSize(0.041)            
        ################################################################

        texts = []
        if(mediator == 'axial'): texts.append(ROOT.TLatex(0.15, 0.82, "Axial vector mediator"))
        elif(mediator == 'vector'): texts.append(ROOT.TLatex(0.15, 0.82, "Vector mediator"))
        texts.append(ROOT.TLatex(0.15, 0.77, "m_{Z'} = 1 GeV, m_{med} = 4 TeV"))
        texts.append(ROOT.TLatex(0.67, 0.91,"138 fb^{-1} (13 TeV)"));

        #texts.append(ROOT.TLatex(0.15, 0.62, "95% CL upper limits on#kern[-0.5]{ }#mu"))
 
        for t in texts:
            t.SetNDC()
            t.SetTextSize(0.04)
            t.SetTextFont(42)
            t.Draw()

        texS2 = TLatex(0.10,0.91,"#bf{CMS}");
        texS2.SetNDC();
        texS2.SetTextFont(42);
        texS2.SetTextSize(0.040);
        texS2.Draw('same');        

        legend.Draw('same')

        line = TLine(minX,1,maxX,1)
        line.SetLineStyle(8)
        line.Draw('same')

        #c.Modified()
        #c.Update()
        gROOT.GetListOfCanvases().Draw()
        c.RedrawAxis()
        c.Modified()
        c.Update()
        outdir = outdir_base# % year
        fname = "limits_%s_1D_%s_Zprime1GeV_mphi=%sGeV_paper.pdf"%(year, mediator, mphi)#axial,vector
        c.SaveAs( "%s/%s" % (outdir,fname) )

make_plot(limits_to_plot, mediator, mphi)
