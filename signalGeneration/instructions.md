- To create data cards you need to have a madgraph version in your area and MonoZprime model
 
```
cmsrel CMSSW_7_2_3
cd CMSSW_7_2_3/src
wget https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.2.2.tar.gz
tar -zxvf MG5_aMC_v2.2.2.tar.gz
cd MG5_aMC_v2_2_2
```
- Inside Madgraph, you have a model directory, get the model file and keep it there,
   
```
cd model
wget http://www.hep.wisc.edu/~varuns/monoZprime/model/DMEFT2ZpNewV2_UFO.zip
tar -xvf DMEFT2ZpNewV2_UFO.zip
```
- Now Script which prepare data cards:
```
prepareCards_vector_monoZprime2016.csh or prepareCards_vector_monoZprime2017.csh
```

- There is nothing that you ned to change, except if you want to change name of directory in which you want to keep data cards which is done at the top
 
```
setenv outDir cards_monoZprime2017
./prepareCards_vector_monoZprime2017.csh >& out.txt &
```
- After preparing datacards, we need to create gridpacks. It can be done only at lxplus /tmp area due to some technical issues.
- Go to lxplus /tmp/user area (no cmssw version needed)
   

```
git clone git@github.com:cms-sw/genproductions.git genproductions
cd genproductions/bin/MadGraph5_aMCatNLO/
```
- Copy your cards to directory in cards/examples/<DarkMatter>/
 
```
cp -r <Cards_Dir> cards/examples/<DarkMatter>/
```
- Basic command to run gridpacks
 
```
./gridpack_generation.sh <name of process card without _proc_card.dat>
<folder containing cards relative to current location>
```
- There is a script which can be used to run over all the cards:
```
generate_gridpack_MonoZprime.csh
```

- Before running the generation of grid pack check if your model file is present in cms central repository (its not present for monoZprime).
- Edit gridpack_generation.sh file
 
```
#wget --no-verbose --no-check-certificate https://cms-project-generators.web.cern.ch/cms-project-generators/$model
wget --no-verbose --no-check-certificate http://www.hep.wisc.edu/~varuns/monoZprime/model/$model
```
- Now edit "generate_gridpack_MonoZprime.csh", where you need to change the grid points mchi and mzh value and then where your cards are stored cards/examples/DarkMatter/ inside genproductions/bin/MadGraph5_aMCatNLO/cards/examples/.
 
 
#### Step-2 (GEN-SIM)
- Once you have gridpacks copy them to UW hdfs area, start the GEN_SIM step:
 
```
export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_1_23
cd CMSSW_7_1_23/src
cmsenv
```

- Create your fragment. 
- The "cmsDriver" command expects the fragment to be in the $CMSSW\_BASE/src/\<Package\>/\<SubPackage\>/python/ directory structure, so we will create such a directory and copy the fragment from an existing one using:
```
submit_monoZprime_LHE_GEN_SIM.py
```
- You need to scram build so that the fragment is registered with your release area.
```
mkdir -p Configuration/GenProduction/python/
Copy the fragment from here:
/cms/varuns/monoZprime/signalGeneration/CMSSW_7_1_23/src/Configuration/GenProduction/python/test_fragment_monop.py
and put it in Configuration/GenProduction/python/
scramv1 b -j2
```
#### Step-3 (DIGI)
```
cmsrel CMSSW_8_0_21
cd src
cmsenv 
```
- Use scripts in DIGI
#### Step-4 (RECO)
- Can be done using the same CMSSW as in DIGI
- Use scripts in RECO
#### Step-5 (MINIAOD)
- Can be done using the same CMSSW as in RECO
- Use scripts in MINIAOD


