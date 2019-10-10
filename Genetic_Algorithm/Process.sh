#!/bin/bash
echo "***********************"
echo "***GENETIC ALGORITHM***"
echo "***********************"
# Genetic algorithm (GA) is a script aimed to find better sequences for our system.
# It is called genetic algorithm, as it tries to improve the sequenses using an
# evolution logic. More specific, it randomly mutates the sequenses and evaluates
# the new system, in order to decide which system is better. You can run GA simply
# by typing "bash Readme.sh" inside the GA directory.

# The script uses the following python scripts-libraries-packages:
# --Both python2 and python3 as different modules are built in different versions
# --POBT script (Patterns Of Binding Targets) that is included in the GA files 
#   and should not be installed manualy 
# --NUPACK
# --Peppercompiler
# --sudo apt install trash-cli

#For the script to run the user must define the NUPACK directory 
echo " "
default_directory="/home/lamphs/Desktop/iGem/dry_lab/packages/nupack3.0.6/nupack3.0.6"
echo "Please type the exact NUPACK 3 directory in your computer ex:"
echo "/home/lamphs/Desktop/iGem/dry_lab/packages/nupack3.0.6/nupack3.0.6"
echo "Type 0 to use the default directory"
read NUPACK_directory
if [ $NUPACK_directory -eq $NUPACK_directory 2>/dev/null ]
then
    echo "Default directory selected!"
    export NUPACKHOME="/home/lamphs/Desktop/iGem/dry_lab/packages/nupack3.0.6/nupack3.0.6"
else
    echo "$input directory selected"
    export NUPACKHOME=$NUPACK_directory
fi

# For the script to run the user must also provide the files describing the system.
# In the "System" folder the user must place the following five files that describe 
# the system.
# --system.pil
# --system.save
# --systemsys.sys
# --plato_2_0.comp
# --TF.pfm
# The user can also optionally add the initial sequences for GA to work on. To do that
# place the current system file "current.pil" into the "Best_Species" folder. Otherwise,
# the GA script will randomly create the initial sequences.
echo "Searching for initial sequences..."
if [ -f "Best_Species/current.pil" ]
then
    echo "Initial sequences found!"
else 
    echo "Initial sequences not found. Generating..."
    python Genetic_Algorithm/RandomReplace.py -ip System/system.pil -op Best_Species/current.pil
fi
python3 Genetic_Algorithm/Savetmp.py
python3 Genetic_Algorithm/pfm_to_pwm.py
pepper-design-spurious -o Best_Species/current.mfe Best_Species/current.pil
pepper-finish --save System/system.save Best_Species/current.mfe
python Genetic_Algorithm/EvaluationInputs.py --sys System/systemsys -bn Best_Species/current -sig solo-Dtg solo-Btd solo-Ntb solo-tbB solo-taA solo-Btr solo-Rtq solo-Ctb solo-Itc solo-tcC
python3 Genetic_Algorithm/Convert_seqs.py
python3 PoBT-master/src/main.py PoBT-master/src/data 0 n PoBT-master/output
python3 Genetic_Algorithm/Calc_tf_binding_sites.py
echo "*****************************"
echo "***INITIAL FILES PROCESSED***"
echo "*****************************"

# Finally, the user should enter the mutation steps and the mutations at each step.
# Also, the script can save all previous species at the "Ark" folder.
echo "Enter mutation steps number, followed by [ENTER]:"
read mutationsteps
echo "Enter mutations at each step number, followed by [ENTER]:"
read mutationeach
while true; do
    read -p "Save all mutations? Y / N followed by [ENTER]:" yn
    case $yn in
        [Yy]* ) save=true; break;;
        [Nn]* ) save=false; break;;
        * ) echo "Please answer yes or no.";;
    esac
done

for (( i=0; i<$mutationsteps; i++ ))
do
    echo "Generation = " $i
    for (( j=0; j<$mutationeach; j++ ))
    do
        echo "Mutating = " $j
        python Genetic_Algorithm/SpecMutate.py -f $j #--specific_mut solo-b
    done
    pepper-design-spurious -o Temporary_Species/tempcurrent.mfe Temporary_Species/tempcurrent.pil
    pepper-finish --save System/system.save Temporary_Species/tempcurrent.mfe
    python Genetic_Algorithm/EvaluationInputs.py --sys System/systemsys -bn Temporary_Species/tempcurrent -sig solo-Dtg solo-Btd solo-Ntb solo-tbB solo-taA solo-Btr solo-Rtq solo-Ctb solo-Itc solo-tcC
    python3 Genetic_Algorithm/Convert_temp_seqs.py
    python3 PoBT-master/src/main.py PoBT-master/src/tdata 0 n PoBT-master/toutput 
    python3 Genetic_Algorithm/Calc_tf_temp_binding_sites.py
    if $save; then
        echo "Saving..."
        python Genetic_Algorithm/Noah.py
    fi
    echo "Killing..."
    python Genetic_Algorithm/Kill.py Best_Species/current.csv Temporary_Species/tempcurrent.csv
    trash-empty
    python3 Genetic_Algorithm/Cleantmp.py
done
notify-send "System Evolution" "Reached last Generation"

