import os, sys
import ROOT as rt
from ROOT import TFile, TH1, TH1F, THStack, TCanvas, TPad, TLine, TColor

rt.gROOT.SetBatch(True)
rt.TH1.AddDirectory(False)

#rt.gStyle.SetErrorX(0)
rt.gStyle.SetTextFont(42)               # Default text font --42==helvetica
rt.gStyle.SetLabelFont(42, "X")         # X axis labels
rt.gStyle.SetTitleFont(42, "X")         # X axis title
rt.gStyle.SetLabelFont(42, "Y")         # Y axis labels
rt.gStyle.SetTitleFont(42, "Y")         # Y axis title
rt.gStyle.SetLabelFont(42, "Z")         # Z axis labels
rt.gStyle.SetTitleFont(42, "Z")         # Z axis title
rt.gStyle.SetPadTickY(1)
rt.gStyle.SetPadTopMargin(0.07)
#rt.gStyle.SetPadBottomMargin(0.13)
rt.gStyle.SetPadLeftMargin(0.13)
rt.gStyle.SetPadRightMargin(0.05)

bkg_colors = {
    "gjet": TColor.GetColor("#2db6a2"),
    "zjet": TColor.GetColor('#5790fc'),
    "wjet": TColor.GetColor('#f89c20'),
    "qcd": TColor.GetColor('#FAF71A'),
    "dyjet": TColor.GetColor('#964a8b'),
    "diboson": TColor.GetColor('#7a21dd'),
    "top": TColor.GetColor('#e42536'),
}

def get_root_object(file, name):
    obj = file.Get(name)
    print(obj.GetName())
    if not obj:
        raise RuntimeError(f"Object {name} not found in file")

    if isinstance(obj, rt.TH1):
        obj.SetDirectory(0)
    
    elif isinstance(obj, rt.TGraph):
        obj = obj.Clone()
        obj.SetName(name)

    return obj


def UncBandStyle(uncband,color=16):
    #uncband.SetTitle("")
    uncband.SetFillColor(color)
    uncband.SetFillStyle(3001)#3002#3144)
    #uncband.SetMarkerStyle(0)
    #uncband.SetMarkerSize(-1)
    uncband.SetLineColor(color)
    #uncband.SetLineColor(-1)
    uncband.SetLineWidth(1)


def getXrange(infile):
    xmin = 0.0
    xmax = 1.0
    if "recoil" in infile:
        xmin = 250.0
        xmax = 1200.0
    if "HPSJetPtOverAssociatedJetPt" in infile:
        xmin = 0.3
        xmax = 1.6
    if "Associatedjet_neEmEF" in infile:
        xmin = 0.0
        xmax = 1.0
    if "Associatedjet_chHEF" in infile:
        xmin = 0.0
        xmax = 1.0
    
    return xmin, xmax

