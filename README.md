# Genetic-Algorithm-System-Sequencing #

The scripts here are used to mutate one nucleotide in a existing DNA Strand Displacement system, to revaluate it and to choose to keep the mutation or discard it.

In order to use the software, the user has to put some input files and make some small changes to the code.

## Dependencies ##
python 2.7 and python 3
the python packages pandas, os, numpy, re, argparse, pkg_resources, statistics, sys, csv, shutil, math, random, datetime
NUPACK 3.0.6 http://nupack.org/downloads
piperine https://github.com/DNA-and-Natural-Algorithms-Group/piperine
stickydesign https://github.com/DNA-and-Natural-Algorithms-Group/stickydesign

## Creating the system files ##

First of all the users have to know the system they want to create the sequences for. This system should be described by a .comp file like those in Genetic_Algorithm/Examples/P65_example/System and Genetic_Algorithm/Examples/ELK1_example/System. Note that if the user does not intend to put restrictions for specific nucleotides, the .comp nucleotide restriction has to be H. Otherwise the .comp nucleotide restriction has to be in accordance with the user's restriction alphabet.  

The system will be initially imported in peppercompiler, so a .sys file is also needed. Examples of .sys files can be found in Genetic_Algorithm/Examples/P65_example/System and Genetic_Algorithm/Examples/ELK1_example/System. The .comp and the .sys have to be in the file Genetic_Algorithm/System and the .sys file has to be named system.sys. The .comp file has to have a different name.

Once those files are ready the users are ready to create the system.pil file which will contain the user's restrictions on the nucleotides. This is done with the following command in the terminal:
```
$ pepper-compiler system.sys
```
The users can open the system.pil and put nucleotides in the wanted positions. Those nucleotides will never be mutated through the Genetic Algorithm runs. A file named system.save will be also produced by the above command.

About the TF files ....

Those .... files, system.sys, .comp, system.pil, system.save .... must be in the System directory.

## Creating the inital sequences ##

This step is not necessary but is strongly recommended.
Using the system.pil and system.save the user can create sequences containing the specified restrains,if any. It can be done by using the following commands:
```
$ pepper-design-spurious system.pil
$ pepper-finish systemsys.mfe
```
Two new files are produced system.mfe and system.seqs.
Now the initial sequences are produced but the initial files are not ready yet. All files should now be copied to a different directory. The users now open the system.seqs file and copy all lines containing the sequences for the toeholds and the domains. Next, a file .fixed is created by the user and the copied text is pasted. Examples of .fixed files can be found in Genetic_Algorithm/Examples/ELK1_example/ELK1.fixed and Genetic_Algorithm/Examples/ELK1_example/P65.fixed. By running the following commands, the initial sequences are created:
```
$ pepper-compiler system.sys --fixed name.fixed
$ pepper-design-spurious system.pil
$ pepper-finish system.mfe
```
The file needed for the initial sequences is the system.pil. This file must be renamed to current.pil and must be placed in the Best_Species directory.

If no initial sequences are given, the software creates a .pil with random sequences, respecting the user specified restrictions.

## Running to a different computer and system ##

In the Process.sh the users have to change the lines specifying the NUPACK 3.0.6 directory. Those lines are 21, 23 and 29. More specifically the users have to change the "/home/lamphs/Desktop/iGem/dry_lab/packages/nupack3.0.6/nupack3.0.6" with the path to their computer's installation of NUPACK 3.0.6

Another important change in done in the flag --sig of the EvalutionInputs.py. This flag must followed by the names of the system's signal strands. The lines 91 and 81 must look like this ```$ python Genetic_Algorithm/EvaluationInputs.py --sys System/systemsys -bn Best_Species/current -sig solo-Dtg solo-Btd solo-Ntb solo-tbB solo-taA solo-Btr solo-Rtq solo-Ctb solo-Itc solo-tcC```

## Changing the code for a different transcription factor ##

## Using the software ##

Once all above are ready, the users can run the software by openning the terminal in Genetic_Algorithm/ and typing the following command:
```
$ bash Process.sh
```
From here the user should specify NUPACK 3.0.6 path, number of generations and number of mutations in each generation, by following the instructions.

The user can specify a domain to be mutated by adding the flag --specific_mut with the domain in the line 87 of the Process.sh file, for example ```$ python Genetic_Algorithm/SpecMutate.py -f $j --specific_mut solo-b ```

In usual runs, the BN% measures are not calculated due to their excessive computational time. If the users want to calculate the BN% measures the have to put the --ted or -t flag in the lines 91, and maybe in 81 as well , of the Process.sh. Specifically, the line should be
```$ python Genetic_Algorithm/EvaluationInputs.py --sys System/systemsys -bn Best_Species/current -t -sig signal1 signal2 signalN```
