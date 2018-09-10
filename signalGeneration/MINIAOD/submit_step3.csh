#!/bin/tcsh

setenv pwd $PWD

##For private production - 2016
#foreach mchi (1 10 50 100 150 500 1000) #all
foreach mchi (100 1000 )
  if(${mchi} == 1) then
     foreach mzh (10 20 50 100 200 300 500 1000 10000)
  else
      if(${mchi} == 10)   foreach mzh (10 15 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000) #all
      if(${mchi} == 50)   foreach mzh (10 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000) #all 
      if(${mchi} == 100)  foreach mzh (10 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000) #all
      if(${mchi} == 150)  foreach mzh (10 200 295 500 1000 10000) #all
      if(${mchi} == 500)  foreach mzh (10 500 995 10000) #all
      if(${mchi} == 1000) foreach mzh (10 1000 10000) #all
endif


echo ${mchi},${mzh}

farmoutAnalysisJobs  --input-files-per-job=1 --input-dir=/hdfs/store/user/varuns/MonoZprime_Mx${mchi}_Mv${mzh}_RECO-step2_RECO   --match-input-files='step2_RECO-*.root' MonoZprime_Mx${mchi}_Mv${mzh}_MINIAOD /cms/varuns/monoZprime/signalGeneration/CMSSW_8_0_21 /cms/varuns/monoZprime/signalGeneration/CMSSW_8_0_21/src/MINIAOD/step3_MINIAOD.py   --vsize-limit=10000 --site-requirements='OpSysAndVer == "SL6" && TARGET.HAS_CMS_HDFS && TARGET.Arch == "X86_64" && (MY.RequiresSharedFS=!=true || TARGET.HasAFS_OSG) && (TARGET.OSG_major =!= undefined || TARGET.IS_GLIDEIN=?=true) && IsSlowSlot=!=true'

end
end
