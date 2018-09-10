#!/bin/tcsh 

setenv  pwd $PWD

### Central production grid
foreach mx (1 10 50 150 500 1000)
  if(${mx} == 1) then
      foreach mzprime (10 20 50 100 200 300 500 1000 10000)
  else
      if(${mx} == 10)   foreach mzprime (10 15 50 100 10000)
      if(${mx} == 50)   foreach mzprime (10 50 95 200 300 10000)
      if(${mx} == 150)  foreach mzprime (10 200 295 500 1000 10000)
      if(${mx} == 500)  foreach mzprime (10 500 995 10000)
      if(${mx} == 1000) foreach mzprime (10 1000 10000)
endif

echo "DM_MonoZPrime_V_Mx${mx}_Mv${mzprime}_gDMgQ1_LO"
./gridpack_generation.sh DM_MonoZPrime_V_Mx${mx}_Mv${mzprime}_gDMgQ1_LO cards/examples/cards_monoZprime2017/DM_MonoZPrime_V_Mx${mx}_Mv${mzprime}_gDMgqQ1_LO

end
end


