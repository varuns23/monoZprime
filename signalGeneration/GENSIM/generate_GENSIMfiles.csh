#!/bin/tcsh 

setenv pwd $PWD

##For central prodution - 2017
##foreach mchi (1 10 50 150 500 1000)
##  if(${mchi} == 1) then
##      foreach mzh (10 20 50 100 200 300 500 1000 10000)
##  else
##      if(${mchi} == 10)   foreach mzh (10 15 50 300 400 500 600 800 1200 2200 3000 10000)
##      if(${mchi} == 50)   foreach mzh (10 50 95 300 400 600 800 1200 2200 3000 10000)
##      if(${mchi} == 100)  foreach mzh (10 50 95 300 400 500 600 800 1200 2200 3000 10000)
##      if(${mchi} == 150)  foreach mzh (10 200 295 500 1000 10000)
##      if(${mchi} == 500)  foreach mzh (10 500 995 10000)
##      if(${mchi} == 1000) foreach mzh (10 1000 10000)
##endif

##For private production - 2016
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

cd ${pwd}

sed -e "s/MX/Mx${mchi}/g" -e "s/MV/Mv${mzh}/g" <${pwd}/submit_monoZprime_LHE_GEN_SIM.py >${pwd}/MonoZprime_GENSIM_Mx${mchi}_Mv${mzh}.py

end
end
