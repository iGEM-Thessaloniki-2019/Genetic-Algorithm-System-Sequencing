# Genetic-Algorithm-System-Sequencing #

The scripts here are used to mutate one nucleotide in a existing DNA Strand Displacement system, to revaluate the system and to choose to keep the mutated system or discard it.

In order to use the software, the user has to put some input files and make some small changes to the code.

## Dependencies ##
python 2.7 and python 3 and the python packages pandas, os, numpy, re, argparse, pkg_resources, statistics, sys, csv, shutil, math, random, datetime

NUPACK 3.0.6 http://nupack.org/downloads

piperine https://github.com/DNA-and-Natural-Algorithms-Group/piperine

stickydesign https://github.com/DNA-and-Natural-Algorithms-Group/stickydesign

trash-cli by using the command ```$ sudo apt-get install trash-cli ```

notify-osd by using the command ```$ sudo apt-get install notify-osd```

## Creating the system files ##

First of all the users have to know the system they want to create the sequences for. This system should be described by a .comp file like those in "Genetic_Algorithm/Examples/P65_example/System" and "Genetic_Algorithm/Examples/ELK1_example/System". Note that if the user does not intend to put restrictions for specific nucleotides, the .comp nucleotide restriction has to be H for the upper strands, which indicates that only A,T,C nucleotides are allowed (ex. sequence tb = "<t>H"). Otherwise the .comp nucleotide restriction has to be in accordance with the user's restriction alphabet.  

The system will be initially imported in peppercompiler, so a .sys file is also needed. Examples of .sys files can be found in "Genetic_Algorithm/Examples/P65_example/System" and "Genetic_Algorithm/Examples/ELK1_example/System". The .comp and the .sys files have to be in the file Genetic_Algorithm/System and the .sys file has to be named systemsys.sys. The .comp file has to have a different name.

Once those files are ready the users are ready to create the system.pil file which will contain the user's restrictions on the nucleotides. This is done with the following command in the terminal:
```
$ pepper-compiler systemsys.sys --output system.pil
```
The users can open the system.pil and put nucleotides in the wanted positions. Those nucleotides will never be mutated through the Genetic Algorithm runs. A file named system.save will be also produced by the above command.

About the TF files, two files are needed. The first contains data about the Position Frequency Matrix for the TF. To create the file the users have to search for their Transcription Factor in Jaspar and download the RAW PFM file or they just have to create a file similar to the one provided by JASPAR. This file must be renamed to TF.pfm and in its first line should be edited in order to contain only the four letters, that declare the order of rows providing the data for each nuclotide of the PFM, for example ACGT. Examples of TF.pfm can be found in "Genetic_Algorithm/Examples/P65_example/System" and "Genetic_Algorithm/Examples/ELK1_example/System". The second file defines the intentend positions of the binding sites. The file must be named tf.config and its first line must be the number of those intended positions, so if there are 2 intended positions, the first line is: Hits = 2. Every intended hit, is defined by the name of the strand and the position of the first nucleotide of the binding site. Note that counting for the position starts from 0. The name of the strands are found in "Genetic_Algorithm/PoBT-master/src/data". Examples of tf.config files are found in Genetic_Algorithm/Examples/P65_example/System" and "Genetic_Algorithm/Examples/ELK1_example/System".

Those five files, systemsys.sys, .comp, system.pil, TF.pfm and tf.config must be in the System directory.

## Creating the inital sequences ##

This step is not necessary but is strongly recommended.
Using the system.pil and system.save the user can create sequences containing the specified restrains, if any. It can be done by using the following commands:
```
$ pepper-design-spurious system.pil
$ pepper-finish system.mfe
```
Two new files are produced system.mfe and system.seqs.
Now the initial sequences are produced but the initial files are not ready yet. All files should now be copied to a different directory. The users now open the system.seqs file and copy all lines containing the sequences for the toeholds and the domains. Next, a file .fixed is created by the user and the copied text is pasted. Examples of .fixed files can be found in Genetic_Algorithm/Examples/ELK1_example/ELK1.fixed and Genetic_Algorithm/Examples/ELK1_example/P65.fixed. By running the following commands, the initial sequences are created:
```
$ pepper-compiler systemsys.sys --fixed name.fixed
$ pepper-design-spurious system.pil
$ pepper-finish system.mfe
```
The file needed for the initial sequences is the system.pil. This file must be renamed to current.pil and must be placed in the Best_Species directory.

If no initial sequences are given, the software creates a .pil with random sequences, respecting the user specified restrictions.

## Running on a different computer or different dna system ##

In the Process.sh the users have to change the lines specifying the NUPACK 3.0.6 directory. Those lines are 21, 23 and 29. More specifically the users have to change the "/home/lamphs/Desktop/iGem/dry_lab/packages/nupack3.0.6/nupack3.0.6" with the path to their computer's installation of NUPACK 3.0.6

Another important change in done in the flag --sig of the EvalutionInputs.py. This flag must followed by the names of the system's signal strands. The lines 91 and 81 must look like this ```$ python Genetic_Algorithm/EvaluationInputs.py --sys System/systemsys -bn Best_Species/current -sig solo-Dtg solo-Btd solo-Ntb solo-tbB solo-taA solo-Btr solo-Rtq solo-Ctb solo-Itc solo-tcC```

## Using the software ##

Once all above are ready, the users can run the software by opening the terminal in Genetic_Algorithm/ and typing the following command:
```
$ bash Process.sh
```
From here the user should specify the NUPACK 3.0.6 path, the number of generations and the number of mutations in each generation, following the instructions.

The user can specify a particular domain to be mutated by adding the flag --specific_mut with the domain in the line 87 of the Process.sh file, for example ```$ python Genetic_Algorithm/SpecMutate.py -f $j --specific_mut solo-b ```

In usual runs, the BN% measures are not calculated due to their excessive computational time. If the users want to calculate the BN% measures the have to put the --ted or -t flag in the lines 91 and 81, of the Process.sh. Specifically, the line should be
```$ python Genetic_Algorithm/EvaluationInputs.py --sys System/systemsys -bn Best_Species/current -t -sig signal1 signal2 signalN```

## Calculating the toehold energies ##

The toehold energies can be calculated by using the script Toeholds_Energies/toeholds.py. The users have to open toeholds.py, and change the array b. In this array the users have to import the toehold sequences. The binding energy of each toehold, the mean value of the energies, the energy variance, the energy range and a heatmap are printed in the terminal by running the following command:

```
$ python toeholds.py
```

## Contact ##
For questions or troubleshooting, the users can send emails to igemthessaloniki@gmail.com
