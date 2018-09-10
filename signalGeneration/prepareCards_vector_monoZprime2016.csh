#!/bin/tcsh 

setenv pwd $PWD
setenv outDir cards_monoZprime2016

mkdir ${pwd}/${outDir}
setenv RunDir ${pwd}/${outDir}


### Central production grid
##foreach mchi (1 10 50 150 500 1000)
##  if(${mchi} == 1) then
##      foreach mzh (10 20 50 100 200 300 500 1000 10000)
##  else
##      if(${mchi} == 10)   foreach mzh (10 15 50 100 10000)
##      if(${mchi} == 50)   foreach mzh (10 50 95 200 300 10000)
##      if(${mchi} == 150)  foreach mzh (10 200 295 500 1000 10000)
##      if(${mchi} == 500)  foreach mzh (10 500 995 10000)
##      if(${mchi} == 1000) foreach mzh (10 1000 10000)
##endif

foreach mchi (1 10 50 100 150 500 1000)
  if(${mchi} == 1) then
      foreach mzh (10 20 50 100 200 300 500 1000 10000)
  else
      if(${mchi} == 10)   foreach mzh (10 15 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000)
      if(${mchi} == 50)   foreach mzh (10 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000)
      if(${mchi} == 100)  foreach mzh (10 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000)
      if(${mchi} == 150)  foreach mzh (10 200 295 500 1000 10000)
      if(${mchi} == 500)  foreach mzh (10 500 995 10000)
      if(${mchi} == 1000) foreach mzh (10 1000 10000)
endif

echo ${mchi},${mzh}

setenv Dir DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgqQ1_LO

cd ${pwd}

cat>DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgqQ1_LO.dat<<EOF
set loop_optimized_output True
set group_subprocesses Auto
set ignore_six_quark_processes False
set gauge unitary
set complex_mass_scheme False
import model DMEFT2ZpNewV2_UFO
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm
define vl~ = ve~ vm~
generate p p > vt vt~ Zp QED=0 dmvector=3 dmzpu=1,Zp > u u~
output DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO
launch

set run_card ebeam1 6500
set run_card ebeam2 6500
set run_card nevents 50
set run_card misset 200
set run_card drjj 0.0
set param_card Mv3  ${mchi}
set param_card MZh  ${mzh}
set param_card gchi 1.0
set param_card gvhq 0.25
set param_card MZp  1.0
set param_card DECAY 600002 Auto
EOF

./bin/mg5_aMC DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgqQ1_LO.dat

if( -d ${RunDir}/${Dir} ) then
    echo "directory *${Dir}* already exists Check for it"
    else
    mkdir ${RunDir}/${Dir}

# For 2017 production
#sed -e "s/nn23lo1/lhapdf/g" -e "s/230000/"'$'"DEFAULT_PDF_SETS/g" -e "/Enable/s/F/T/g" <${pwd}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO/Cards/run_card.dat >${pwd}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO/Cards/run_card1.dat
# For 2016 production
sed -e "s/nn23lo1/'lhapdf'/g" -e "s/230000/263400/g" -e "/Enable/s/F/T/g" <${pwd}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO/Cards/run_card.dat >${pwd}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO/Cards/run_card1.dat

cp ${pwd}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO/Cards/run_card1.dat ${RunDir}/${Dir}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO_run_card.dat
cp ${pwd}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO/Cards/proc_card_mg5.dat ${RunDir}/${Dir}/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO_proc_card.dat

cd ${RunDir}/${Dir}
cat>DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO_customizecards.dat<<EOF
set run_card misset 200
set run_card drjj 0.0
set param_card Mv3  ${mchi}
set param_card MZh  ${mzh}
set param_card gchi 1.0
set param_card gvhq 0.25
set param_card MZp  1.0
set param_card DECAY 600002 Auto
EOF


cat>DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO_extramodels.dat<<EOF
DMEFT2ZpNewV2_UFO.zip
EOF

end
end
