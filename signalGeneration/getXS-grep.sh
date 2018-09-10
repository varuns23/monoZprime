#!/bin/tcsh

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


grep "HTML/run_01/results.html" Temp_DM_MonoZPrime_V_Mx${mchi}_Mv${mzh}_XS/crossx.html > monoZprime_XS-2016-defaultPDF_tmp.txt

sed -e "s/        <td rowspan=1><center><a href=/MonoZPrime_V_Mx${mchi}_Mv${mzh} (pb): /g" -e 's/".\/HTML\/run_01\/results.html">//g' -e 's/<font face=symbol>&#177;<\/font>/ +\/- /g'  -e "s/<\/a>  <\/center><\/td>//g" < monoZprime_XS-2016-defaultPDF_tmp.txt >> monoZprime_XS-2016-defaultPDF.txt
 
rm monoZprime_XS-2016-defaultPDF_tmp.txt

end
echo " " >> monoZprime_XS-2016-defaultPDF.txt
end
