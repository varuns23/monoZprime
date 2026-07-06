#!/nfs_scratch/mallampalli/improve_plotting/FR_stuff/2dlimit_env/bin/python
import os
import json
import numpy as np
import pandas as pd
import scipy.interpolate
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.ndimage import gaussian_filter1d
import matplotlib.colors as mcolors
from matplotlib import rc
import sys
import mplhep as hep

# Set up matplotlib rcParams
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['TeX Gyre Heros']
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.rm'] = 'TeX Gyre Heros'
mpl.rcParams['mathtext.it'] = 'TeX Gyre Heros:italic'
mpl.rcParams['mathtext.bf'] = 'TeX Gyre Heros:bold'
mpl.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "TeX Gyre Heros",
    "text.latex.preamble": r"\usepackage{tgheros} \usepackage{sansmath} \sansmath"
})

cwd = os.getcwd()
#mediator = 'vector' #'axial' or 'vector'
mediator = 'vector' #'axial' or 'vector'
input_dir = cwd + '/%s/'%(mediator)

limits_exp0={}; limits_exp_plus1={}; limits_exp_minus1={}; limits_exp_plus2={}; limits_exp_minus2={};  limits_obs = {}

def load_from_json(json_path,key,limit_dict,variation):
    with open(json_path,'r') as jf:
        mx_dict = json.load(jf)
        dict_to_add = {}
        for Mv in mx_dict.keys():
            value_to_get = round(mx_dict[Mv][variation],3)
            Mv = float(Mv) 
            if(Mv not in [2000, 3600,3750,3800, 4000]): continue
            dict_to_add[Mv] =  value_to_get
        key = float(key.replace('Mx',''))       
        limit_dict[key] =  dict_to_add
    return limit_dict

def get_line(points):
    point_1 = points[0]
    point_2 = points[-1]
    slope = (point_2[-1]-point_1[-1])/(point_2[0]-point_1[0])
    intercept = (point_1[-1]*point_2[0]-point_2[-1]*point_1[0])/(point_2[0]-point_1[0])
    return round(slope,3),round(intercept,3)

def get_nan_value(limit_dict_to_use):
    Mv_line = get_line(([3600,limit_dict_to_use[1000][3600]],[3750,limit_dict_to_use[1000][3750]])) 
    Mx_line = get_line(([500,limit_dict_to_use[500][2000]],[800,limit_dict_to_use[800][2000]])) 
    nan_1 = Mv_line[0]*2000+Mv_line[-1]
    nan_2 = Mx_line[0]*1000+Mx_line[-1]
    nan_value = (nan_1 + nan_2)/2
    return nan_value

def load_from_dict(limit_dict_to_use):
    limit_df_to_use =  pd.DataFrame.from_dict(limit_dict_to_use,orient='index')
    limit_df_to_use.sort_index(ascending=False,inplace=True)
    limit_df_to_use.sort_index(axis=1,ascending=True,inplace=True)
    any_nan = limit_df_to_use.isnull().values.any()
    if(any_nan):
        nan_value = get_nan_value(limit_dict_to_use)
        limit_df_to_use.fillna(nan_value,inplace=True)
    return limit_df_to_use

for Mx in os.listdir(input_dir):
    if(not("Mx" in Mx)): continue
    if(Mx=="Mx1"): continue
    if(Mx=="Mx10"): continue
    limits_exp0 = load_from_json('%s/%s/limits_.json'%(input_dir,Mx),Mx,limits_exp0,'exp0')
    limits_exp_plus1 = load_from_json('%s/%s/limits_.json'%(input_dir,Mx),Mx,limits_exp_plus1,'exp+1')
    limits_exp_minus1 = load_from_json('%s/%s/limits_.json'%(input_dir,Mx),Mx,limits_exp_minus1,'exp-1')
    limits_exp_plus2 = load_from_json('%s/%s/limits_.json'%(input_dir,Mx),Mx,limits_exp_plus2,'exp+2')
    limits_exp_minus2 = load_from_json('%s/%s/limits_.json'%(input_dir,Mx),Mx,limits_exp_minus2,'exp-2') 
    limits_obs = load_from_json('%s/%s/limits_.json'%(input_dir,Mx),Mx,limits_obs,'obs')

limits_exp0_df = load_from_dict(limits_exp0)
limits_exp_plus1_df = load_from_dict(limits_exp_plus1)
limits_exp_minus1_df = load_from_dict(limits_exp_minus1)
limits_exp_plus2_df = load_from_dict(limits_exp_plus2)
limits_exp_minus2_df = load_from_dict(limits_exp_minus2)
limits_obs_df = load_from_dict(limits_obs)

n_interp_x = 21
n_interp_y = 21

def get_interp_lims(lim_df,tag):
    Mx_arr = np.array(lim_df.index) ; Mv_arr = np.array(lim_df.columns)
    lim_df.sort_index(ascending=False,inplace=True)
    lim_df.sort_index(axis=1,ascending=True,inplace=True)
    lim_df.fillna(5,inplace=True)# arbit high value so it doesn't affect limit boundary
    x,y = np.meshgrid(Mv_arr,Mx_arr)
    available_points = np.array((x,y)).T.reshape(-1, 2) 
    #create fine grid to avoid weird interpolation effects
    if('minus' not in tag): xi, yi = np.linspace(Mv_arr.min(), Mv_arr.max(), n_interp_x), np.round(np.linspace(Mx_arr.min(), Mx_arr.max(), n_interp_y))
    else: xi, yi = np.concatenate([np.linspace(2000,3500,16),np.round(np.linspace(3501,4000,6))]), np.concatenate([np.round(np.linspace(1,500, 10)),np.round(np.linspace(501,800, 3)),np.round(np.linspace(801,1000, 4))])
    xi, yi = np.meshgrid(xi, yi)

    points = np.array((x.flatten(), y.flatten())).T
    vals = lim_df.values.flatten()
    zi_griddata = scipy.interpolate.griddata(points, vals,(xi,yi), method='cubic')

    fig, ax = plt.subplots()
    cs_griddata = ax.contour(xi, yi, zi_griddata, levels=[1.0], linewidths=0.5, colors='k')
    cs_rbf=[]
    cs_griddata.collections[0].set(edgecolor='k',label='griddata')
    plt.close(fig) # close figure so it does not pop up during script execution
    return (cs_rbf,cs_griddata)

contor_lines = {}
contor_lines['exp0'] = get_interp_lims(limits_exp0_df,'exp0')
contor_lines['plus1'] = get_interp_lims(limits_exp_plus1_df,'plus1')
contor_lines['minus1'] = get_interp_lims(limits_exp_minus1_df,'minus1')
contor_lines['plus2'] = get_interp_lims(limits_exp_plus2_df,'plus2')
contor_lines['minus2'] = get_interp_lims(limits_exp_minus2_df,'minus2')
contor_lines['obs'] = get_interp_lims(limits_obs_df,'obs')

to_use = 1

exp0_contour = contor_lines['exp0'][to_use].collections[0].get_paths()[0].vertices.copy()
plus1_contour = contor_lines['plus1'][to_use].collections[0].get_paths()[0].vertices.copy()
minus1_contour = contor_lines['minus1'][to_use].collections[0].get_paths()[0].vertices.copy()
plus2_contour = contor_lines['plus2'][to_use].collections[0].get_paths()[0].vertices.copy()
minus2_contour = contor_lines['minus2'][to_use].collections[0].get_paths()[0].vertices.copy()
obs_contour = contor_lines['obs'][to_use].collections[0].get_paths()[0].vertices.copy()

##Contour extraction introduces noise: so make sure the contours pass through the same points that the 1d limits pass (which didn't have to rely on contours as they are more robust and reliable), this helps fix any issues with extracted contours
# Axial: 
####exp:4257.91511311
####obs:4201.92694475
####minus_1:4463.70192287
####minus_2:4656.69541289
####plus_1:4058.30556922
####plus_2:3885.24408211
# vector: 
####exp:4204.46865069
####obs:4153.60366171
####minus_1:4385.37824319
####minus_2:4553.26483149
####plus_1:4031.25517263
####plus_2:3882.15211473

axial_dm_150_values = {
    'exp0':4257, 
    'obs':4201,
    'minus1':4463,
    'minus2':4656,
    'plus1':4058,
    'plus2':3885,        
}

vector_dm_150_values = {
    'exp0':4204,
    'obs':4153,
    'minus1':4385,
    'minus2':4553,
    'plus1':4031,
    'plus2':3882,        
}            

def edit_contours(contour,tag,contour_to_copy=None,exp0_contour=exp0_contour):
    if(mediator=='vector'): dm_150_values = vector_dm_150_values
    elif(mediator=='axial'): dm_150_values =  axial_dm_150_values 
    new_contour = []; added = 0
    for contour_point in contour:
        if(tag in ['minus1','minus2']): 
            if(round(contour_point[0],2)==2000):  
                med_mass_2k_index = np.where(contour_to_copy[:, 0] == 2000)[0][0]
                symmetric_value = exp0_contour[med_mass_2k_index][-1] + abs(exp0_contour[med_mass_2k_index][-1]-contour_to_copy[med_mass_2k_index][-1])
                contour_point[-1] = symmetric_value
        if(contour_point[0]<dm_150_values[tag]): new_contour.append(contour_point)
        else: 
            if(added==0):
                added = 1
                contour_point[-1] = 150
                contour_point[0] = dm_150_values[tag]
                new_contour.append(contour_point) 
                break 
    if(added==0): 
        to_add = np.zeros_like(contour[0])
        to_add[0],to_add[-1] = dm_150_values[tag], 150
        new_contour.append(to_add)
    new_contour = np.array(new_contour)   
    new_contour = new_contour[new_contour[:, 0].argsort()] 
    return new_contour

exp0_contour = edit_contours(exp0_contour,'exp0')
obs_contour = edit_contours(obs_contour,'obs')
plus1_contour = edit_contours(plus1_contour,'plus1')
plus2_contour = edit_contours(plus2_contour,'plus2')
minus1_contour = edit_contours(minus1_contour,'minus1',plus1_contour)
minus2_contour = edit_contours(minus2_contour,'minus2',plus2_contour)
#smoothing the contours
spline_k = 1
exp0_spline = scipy.interpolate.make_interp_spline(exp0_contour[:,0],exp0_contour[:,1],k=spline_k)
plus1_spline = scipy.interpolate.make_interp_spline(plus1_contour[:,0],plus1_contour[:,1],k=spline_k)
minus1_spline = scipy.interpolate.make_interp_spline(minus1_contour[:,0],minus1_contour[:,1],k=spline_k)
plus2_spline = scipy.interpolate.make_interp_spline(plus2_contour[:,0],plus2_contour[:,1],k=spline_k)
minus2_spline = scipy.interpolate.make_interp_spline(minus2_contour[:,0],minus2_contour[:,1],k=spline_k)
obs_spline = scipy.interpolate.make_interp_spline(obs_contour[:,0],obs_contour[:,1],k=spline_k)

spline_points= 301
X_ = np.linspace(2000, 5000, spline_points)
y_exp0 = exp0_spline(X_)
y_plus1 = plus1_spline(X_)
y_minus1 = minus1_spline(X_)
y_plus2 = plus2_spline(X_)
y_minus2 = minus2_spline(X_)
y_obs = obs_spline(X_)

y_exp0 = gaussian_filter1d(y_exp0, sigma=15)
y_plus1 = gaussian_filter1d(y_plus1, sigma=15)
y_minus1 = gaussian_filter1d(y_minus1, sigma=15)
y_plus2 = gaussian_filter1d(y_plus2, sigma=15)
y_minus2 = gaussian_filter1d(y_minus2, sigma=15)
y_obs = gaussian_filter1d(y_obs, sigma=15)

root_green = '#607641'
root_yellow = '#F5BB54'

sys.path.append("../add_xsec_to_2d_plots/")
from mcinfo_2017 import *
xsec_dict = xsec_sigs

def to_sci_notation(value, significant_digits=3):
    value = float(value)
    exponent = int(np.floor(np.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    formatted_value = f"{mantissa:.2f}e{exponent:+d}"
    formatted_value = float(formatted_value)
    return formatted_value

def load_xsec_from_dict(xsec_dict,Zp_mass='1p0'):
    modified_xsec_dict = {}
    for sig_proc in xsec_dict.keys():
        Mx = float(sig_proc.split('_')[0].replace('Mx',''))
        Mv = float(sig_proc.split('_')[1].replace('Mv',''))
        if(Mv in [1000.0,1500.0]): continue
        if(Mx not in modified_xsec_dict.keys()): modified_xsec_dict[Mx] = {}
        modified_xsec_dict[Mx][Mv] = to_sci_notation(xsec_dict[sig_proc]['theo'])
    return modified_xsec_dict

def load_dataframe(dict_to_use):
    xsec_df_to_use =  pd.DataFrame.from_dict(dict_to_use,orient='index')
    xsec_df_to_use.sort_index(ascending=False,inplace=True)
    xsec_df_to_use.sort_index(axis=1,ascending=True,inplace=True)
    return xsec_df_to_use

modified_xsec_dict = load_xsec_from_dict(xsec_dict)
xsec_df = load_dataframe(modified_xsec_dict)
# fix the interpolated values using the values from the MC generator for smoother interpolation
xsec_df_cleaned  = xsec_df[(xsec_df.index >= 50) & (xsec_df.index <= 800)].copy()
xsec_df_cleaned.at[800,2000] = 0.00045

xsec_df_cleaned.insert(2,3500.0,[0.00035,0.0016,0.004,0.00615])
xsec_df_cleaned.insert(4,4500.0,[0.000186,0.0003,0.0007,0.0011])

xsec_df_cleaned.loc[600] = {2000.0: 0.00099, 3000.0: 0.0008, 3500.0: 0.00045, 4000.0: 0.00035, 4500.0: 0.00025, 5000.0: 0.00009}
xsec_df_cleaned.loc[700] = {2000.0: 0.0007, 3000.0: 0.0006, 3500.0: 0.00038, 4000.0: 0.00032, 4500.0: 0.0002, 5000.0: 0.00008}
xsec_df_cleaned.loc[900] = {2000.0: 0.00035, 3000.0: 0.0003, 3500.0: 0.00032, 4000.0: 0.00028, 4500.0: 0.000175, 5000.0: 0.000065}

xsec_df_cleaned.sort_index(ascending=False,inplace=True)
xsec_df_cleaned.sort_index(axis=1,ascending=True,inplace=True)

x = xsec_df_cleaned.columns
y = xsec_df_cleaned.index 
X, Y = np.meshgrid(x, y) 
xnew = np.linspace(2000, 5000, 1000) 
#ynew = np.linspace(100, 800, 200)
ynew = np.linspace(100, 900, 200)
Xnew, Ynew = np.meshgrid(xnew, ynew)
points = np.array([X.flatten(), Y.flatten()]).T
values = xsec_df_cleaned.values.flatten()
Znew = scipy.interpolate.griddata(points, values, (Xnew, Ynew), method='linear')

fig, ax = plt.subplots()

plt.plot(X_,y_obs,linestyle='-',color='k', label = 'Observed')
plt.plot(X_,y_exp0,linestyle='--',color='r', label = 'Expected')
plt.plot(X_,y_minus2,linestyle='-.',color=root_yellow, label = 'Expected (1 s.d.)')
plt.plot(X_,y_plus2,linestyle='-.',color=root_yellow)
plt.plot(X_,y_minus1,linestyle=':',color='w', label = 'Expected (2 s.d.)')
plt.plot(X_,y_plus1,linestyle=':',color='w')

c = ax.pcolormesh(Xnew, Ynew, Znew, cmap='viridis', shading='gouraud', norm=mcolors.LogNorm(vmin=10**(-5), vmax=1))
cbar = fig.colorbar(c,ax=ax, pad=0.02)
#cbar.set_label('Cross section [pb]', fontsize=15)
#cbar.ax.yaxis.set_label_coords(2, 0.8)
cbar.ax.tick_params(axis='both', which='major', labelsize=14.5)

cbar.ax.text(
    3.9, 0.78,
    'Cross section [pb]',
    rotation=90,
    transform=cbar.ax.transAxes,
    fontsize=15,
    va='center',
    ha='left'
)

ax.minorticks_on()
#plt.title(r"$138~\mathrm{fb^{-1}} \mathrm{(13 TeV)}$", fontsize=15,x=0.81,y=0.99)
plt.title(r"$138~\mathrm{fb^{-1}} \mathrm{(13 TeV)}$", fontsize=15,x=0.81,y=0.993)
ax.set_xlabel(r"$\mathrm{m}_{\mathrm{med}}\ \mathrm{[GeV]}$", fontsize=15,loc='right')
ax.set_ylabel(r"$\mathrm{m}_{\mathrm{DM}}\ \mathrm{[GeV]}$", fontsize=15, loc='top')
legend = ax.legend(loc="lower left", prop={'size': 15})
#legend.set_title('Exclusion region', prop={'size': 18, 'weight': 'bold'})
legend.set_frame_on(False)
#ax.set_ylim([100, 800])
ax.set_ylim([150, 900])
#ax.set_xlim([2000, 5000])
ax.set_xlim([2000, 4800])
ax.tick_params(axis='both', which='major', labelsize=14.5)
ax.tick_params(axis='both', which='minor', labelsize=7)

mediator_name = {'axial':' Axial vector mediator','vector':' Vector mediator'}
ax.text(0.008, 1.063, r"\textbf{CMS}", color='black', transform=ax.transAxes, fontsize=17,verticalalignment='top', horizontalalignment='left')
ax.text(0.04, 0.43, "Exclusion region", color='black', transform=ax.transAxes, fontsize=17,verticalalignment='top', horizontalalignment='left')
#ax.text(0.97, 0.95, mediator_name[mediator], color='white', transform=ax.transAxes, fontsize=18,verticalalignment='top', horizontalalignment='right')
if(mediator=='vector'):
    ax.text(0.445, 0.96, mediator_name[mediator], color='white', transform=ax.transAxes, fontsize=17,verticalalignment='top', horizontalalignment='right')
elif(mediator=='axial'):
    ax.text(0.574, 0.96, mediator_name[mediator], color='white', transform=ax.transAxes, fontsize=17,verticalalignment='top', horizontalalignment='right')
#ax.text(0.38, 0.95, r"$\mathrm{m}_{\mathrm{Z'}}=1\ \mathrm{GeV}\ $", color='white', transform=ax.transAxes, fontsize=18,verticalalignment='top', horizontalalignment='right')
ax.text(0.35, 0.86, r"$\mathrm{m}_{\mathrm{Z'}}=1\ \mathrm{GeV}\ $", color='white', transform=ax.transAxes, fontsize=17,verticalalignment='center', horizontalalignment='right')

fig.savefig('limit2d_{}.pdf'.format(mediator), bbox_inches='tight',dpi=300)
