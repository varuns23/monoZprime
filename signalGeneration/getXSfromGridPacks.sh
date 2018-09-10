#!/bin/tcsh

# Instructions to follow
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO#Standalone_production_running_th
#cmsrel CMSSW_X_Y_Z 
#cd CMSSW_X_Y_Z/src
#cmsenv
#tar -xavf <path of gridpack creation>/wplustest_LO_tarball.tar.xz
#bash
#./runcmsgrid.sh <NEvents> <RandomSeed> <NumberOfCPUs>


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

tar -xavf gridPacks/DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_gDMgQ1_LO_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz
#bash
./runcmsgrid.sh 20 ${1} 20

grep "Integrated weight" events_presys.lhe > monoZprime_XS-2016_tmp.txt
sed -e "s/Integrated weight/MonoZPrime_V_Mx${mchi}_Mv${mzh}/g" < monoZprime_XS-2016_tmp.txt >> monoZprime_XS-2016.txt

rm monoZprime_XS-2016_tmp.txt

rm -rf CMSSW_7_1_30 cmsgrid_final.lhe gridpack_generation.log process syscalc_card.dat InputCards events_presys.lhe mgbasedir runcmsgrid.sh

end
end
