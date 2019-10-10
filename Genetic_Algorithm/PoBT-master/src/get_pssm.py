#!/usr/bin/env python
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# title      Get PSSM Script                                                       +
# project    A-Study-of-Transcription-and-Its-Affects                              +
# repository https://github.com/johnletey/A-Study-of-Transcription-and-Its-Affects +
# author     John Letey                                                            +
# email      john.letey@colorado.edu                                               +
# copyright  Copyright (C) 2018                                                    +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Implementation of get_pssm
def get_pssm(filename, TF):
    """
        Given a specific transcription factor, get its corresponding pssm

        :param filename: the name of the file that contains the pssm's
        :param TF: the specific transcription factor we want to get the pssm for
    """
    # Open the tamo file
    fileID = open(filename, 'r')
    # Read in the tamo file
    tamoData = []
    fileID = open(filename, 'r')
    line = fileID.readline()
    while line:
        tamoData.append(line[:len(line)-1])
        line = fileID.readline()
    # Define what we're looking for
    correctLine = 'Source:  ' + TF
    # Search for your correct line
    for i in range(2):
        # Get line 19 + 42*i
        line = tamoData[19 + 42*i - 1]
        # Compare
        if line == correctLine:
            position = i
    # Set the start line for the PSSM
    startLine = 2 + 42*position
    # Get the startLine's length to figure out the length of the PSSM
    firstLine = tamoData[startLine]
    lenOfPSSM = int((len(firstLine) - 3)/10) - 1
    # Create a list that will contain the PSSM
    PSSM = [[0 for i in range(lenOfPSSM)] for i in range(4)]
    # Get the all the lines of the PSSM
    firstLine = tamoData[startLine]
    print (firstLine)
    secondLine = tamoData[startLine + 1]
    print (secondLine)
    thirdLine = tamoData[startLine + 2]
    print (thirdLine)
    fourthLine = tamoData[startLine + 3]
    print (fourthLine)
    # Get the values and insert them into the PSSM
    for i in range(lenOfPSSM):
        value = firstLine[(i*10 + 6):(i*10 + 12)]
        PSSM[0][i] = float(value)
        value = secondLine[(i*10 + 6):(i*10 + 12)]
        PSSM[1][i] = float(value)
        value = thirdLine[(i*10 + 6):(i*10 + 12)]
        PSSM[2][i] = float(value)
        value = fourthLine[(i*10 + 6):(i*10 + 12)]
        PSSM[3][i] = float(value)
    # Return the PSSM and the length of the PSSM
    return PSSM, lenOfPSSM
