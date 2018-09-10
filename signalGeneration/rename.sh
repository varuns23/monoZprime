#!/bin/tcsh

setenv filePath "/hdfs/store/user/varuns/NTuples/monoZprime_2016_80X"

foreach mchi (1 10 50 100 150 500 1000) #all
#foreach mchi (100 1000)
  if(${mchi} == 1) then
  foreach mzh (10 20 50 100 200 300 500 1000 10000) #all
  else
      if(${mchi} == 10)   foreach mzh (10 15 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000) #all
      if(${mchi} == 50)   foreach mzh (10 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000) #all
      if(${mchi} == 100)  foreach mzh (10 50 95 100 200 300 400 500 600 800 1000 1200 1500 1800 2000 2200 2500 3000 10000) #all
      if(${mchi} == 150)  foreach mzh (10 200 295 500 1000 10000) #all
      if(${mchi} == 500)  foreach mzh (10 500 995 10000) #all
      if(${mchi} == 1000) foreach mzh (10 1000 10000) #all
endif


rename run_mc_80X-MonoZprime MonoZprime ${filePath}/MonoZprime_Mx${mchi}_Mv${mzh}/*.root
rename _MINIAOD- - ${filePath}/MonoZprime_Mx${mchi}_Mv${mzh}/*.root

end
end



