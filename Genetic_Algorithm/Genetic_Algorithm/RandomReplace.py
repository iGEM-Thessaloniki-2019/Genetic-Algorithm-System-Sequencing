import os
import re
import argparse 
import random

parser = argparse.ArgumentParser(description='The script puts random Nuclotides in a .pil file.')
parser.add_argument('-ip','--pil_file', help='The input .pil file')
parser.add_argument('-op','--new_pil', help='The output .pil file')
args = parser.parse_args()

pil_file = args.pil_file
new_pil = args.new_pil

# pil_file = 'SolovL1_0_0.pil'
# new_pil = 'Skata.pil'

pil_copy = open(new_pil,'w')

choises_dict=group = {"A": "A", "T": "T", "C": "C", "G": "G", \
    "W": "AT", "S": "CG", "M": "AC", "K": "GT", \
        "B": "CGT", "V": "ACG", "D": "AGT", "H": "ACT", \
            "N": "ACGT"}

with open(pil_file) as p:
    #### for every line it finds '=' and ':'
    #### it checks that between there is one thing, that it is uppercase and that the thing before '=' is lowercase
    #### takes the thing between '=' and ':'
    for line in p:
        if re.match('sequence', line) or re.match('sup-sequence', line):
            words = line.split()
            for word_num in range(len(words)):
                if words[word_num]=='=' and str(words[word_num-1]).islower():
                    s=word_num
                    continue
                if words[word_num]==':':
                    e=word_num
            if str(words[s+1:e]).isupper() and str(words[s-1]).islower() and len(words[s+1:e])==1:
                #### Every thing is now an array wich contains one string
                #### The first and only element of 
                tochange=list(str((words[s+1:e][0])))
                for i in range(len(tochange)):
                    if tochange[i] in choises_dict:
                        letter=tochange[i]
                        r=random.choice(choises_dict[letter])
                        #print('before', letter)
                        tochange[i]=r
                        #print('after',tochange[i])
                lin_arr = words[0:s+1]+[''.join(str(x) for x in tochange)]+words[e:] 
                new_line = ' '.join([str(x) for x in lin_arr])+'\n'
                #print(new_line)   
                pil_copy.write(new_line)        
            else:
                pil_copy.write(line)
        else:
            pil_copy.write(line)

pil_copy.close()
p.close()

old_pil_lines = sum(1 for line in open(pil_file))
new_pil_lines = sum(1 for line in open(new_pil))
if old_pil_lines!= new_pil_lines:
    raise ValueError('Number of lines between file %s and % s are not equal' % (new_pil,pil_file))
