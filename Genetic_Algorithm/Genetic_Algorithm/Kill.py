# selectseq
#
# Reads scores from a Piperine-produced .csv file, or combines scores from many such files,
# and compares all sequence designs according to a variety of metrics,
# ultimately selecting a "winner" based on a meta-rank score that "hedges bets".
#
# Run like this, for example:
# python selectseq.py oscillator_scores_bmax10.csv
# python selectseq.py oscillator_scores_bmax2000.csv
# python selectseq.py oscillator_scores_bmax10.csv oscillator_scores_bmax2000.csv

from __future__ import division, print_function

import sys, csv
import numpy as np
import os
import shutil

def cases(array,value):
    return [i for i in range(len(array)) if array[i]==value]

def mincases(array):
    return cases(array,min(array))

def strmincases(array):
    return str(mincases(array))

def strmaxcases(array):
    return str(cases(array,max(array)))

def metarank(scores, method = 'sum-of-metaranks'):
    methods = ['worst-rank', 'worst-weighted-rank', 'sum-of-ranks', 'sum-of-weighted-ranks', 'fractional-excess-sum',
               'weighted-fractional-excess-sum', 'percent-badness-sum', 'weighted-percent-badness-sum', 'sum-of-metaranks']
    assert(method in methods)
    print_fn = lambda x : print(x, end='')
    columns = list(zip(*scores))
    rawscores = []
    ranks = []
    fractions = []
    percents = []
    for col in columns:
        # print col
        # if 'Index' in col[0] or 'Defect' in col[0] or 'Toehold Avg' in col[0] or 'Range of toehold' in col[0]:  ### old EW
        # if 'Index' in col[0] or 'Defect' in col[0] or 'WSI' == col[0]:   ### recent James
        if 'Index' in col[0] or 'Defect' in col[0]:   ### new EW
            continue

        rawscores.append([float(x) for x in col[1:]])  # don't invert raw scores
        if 'SSU' in col[0] or 'SSTU' in col[0]:        # for these scores, higher is better
            col = [-float(x) for x in col[1:]]
        else:
            col = [float(x) for x in col[1:]]          # for these scores, lower is better

        # ties get same rank; next worse gets that rank+1; low rank is better
        array = np.array(col)
        array_uni = np.unique(array)
        array_ord = array_uni.argsort()
        rank_dict = dict(zip(array_uni, array_ord))
        temp_ranks = np.array([rank_dict[x] for x in array])
        temp = array.argsort()
        colranks = np.array([rank_dict[x] for x in array])
        ranks.append(colranks)
        fractions.append((array - array.min())/abs(array.min() + (array.min()==0) ))
        percents.append((array - array.min())/(array.max() - array.min() + (array.min()==array.max()) ))
    temp=ranks
    ranks=list(zip(*temp))
    temp=fractions
    fractions=list(zip(*temp))
    temp=percents
    percents=list(zip(*temp))
    temp=rawscores
    rawscores=list(zip(*temp))

    # with the latest piperine designer code, there should be no need to retitle columns, and this should do nothing
    # print(scores[0])
    newtitles={ "BM Score" : "BM sum", "Largest Match" : "BM max",
                "SSU Min" : "SSU min", "SSU Avg" : "SSU avg", "SSTU Min" : "SSTU min", "SSTU Avg" : "SSTU avg",
                "Max Bad Nucleotide %" : "BN% max", "Mean Bad Nucleotide %" : "BN% avg",
                "WSI-Intra" : "WSAS", "WSI-Inter" : "WSIS", "WSI-Intra-1" : "WSAS-M", "WSI-Inter-1" : "WSIS-M",
                "WSI" : "Spurious", "Toehold Avg dG" : "dG error", "Range of toehold dG's" : "dG range" }
    scores[0]=[ newtitles[t] if t in newtitles else t for t in scores[0] ]
    # print()
    # print(scores[0])

    print_fn("\nRaw scores array:")
    print_fn("\n                             ")
    for title in scores[0]:
        # if 'Index' in title or 'Defect' in title or 'Toehold Avg' in title or 'Range of toehold' in title:
        if 'Index' in title or 'Defect' in title:   # don't need design number, don't need Max Defect Component name
            continue
        print_fn("{:>9s}".format(title[0:9]))
    print_fn("\n")
    i=0
    for s in rawscores:
        print_fn("design {:3d}:                 [".format(i))
        for v in s:
            print_fn("{:9.2f}".format(v))
        print_fn("]\n")
        i=i+1

    print_fn("\nRank array:")
    print_fn("\n                             ")
    for title in scores[0]:
        # if 'Index' in title or 'Defect' in title or 'Toehold Avg' in title or 'Range of toehold' in title:
        if 'Index' in title or 'Defect' in title:   # don't need design number, don't need Max Defect Component name
            continue
        print_fn("{:>9s}".format(title[0:9]))
    print_fn("  :: worst \n")
    i=0
    for r in ranks:
        print_fn("design {:3d}: {:9d} = sum [".format(i,sum(r)))
        for v in r:
            print_fn("{:9d}".format(v))
        print_fn("] :: {:5d}\n".format(max(r)))
        i=i+1

    print_fn("\nFractional excess array:")
    print_fn("\n                             ")
    for title in scores[0]:
        # if 'Index' in title or 'Defect' in title or 'Toehold Avg' in title or 'Range of toehold' in title:
        if 'Index' in title or 'Defect' in title:
            continue
        print_fn("{:>9s}".format(title[0:9]))
    print_fn("\n")
    i=0
    for f in fractions:
        print_fn("design {:3d}: {:9.2f} = sum [".format(i,sum(f)))
        for v in f:
            print_fn("{:9.2f}".format(v))
        print_fn("]\n")
        i=i+1

    print_fn("\nPercent badness (best to worst) array:")
    print_fn("\n                             ")
    for title in scores[0]:
        # if 'Index' in title or 'Defect' in title or 'Toehold Avg' in title or 'Range of toehold' in title:
        if 'Index' in title or 'Defect' in title:
            continue
        print_fn("{:>9s}".format(title[0:9]))
    print_fn("\n")
    i=0
    for p in percents:
        print_fn("design {:3d}: {:9.2f} = sum [".format(i,100*sum(p)))
        for v in p:
            print_fn("{:9.2f}".format(100*v))
        print_fn("]\n")
        i=i+1


    # scores previously used:
    # TSI avg, TSI max, TO avg, TO max, BM, Largest Match, SSU Min, SSU Avg, SSTU Min, SSTU Avg, Max Bad Nt %,  Mean Bad Nt %, WSI-Intra, WSI-Inter, WSI-Intra-1, WSI-Inter-1, Verboten, WSI
    # CSV file has
    # TSI avg, TSI max, TO avg, TO max, BM Score, Largest Match, SSU Min, SSU Avg, SSTU Min, SSTU Avg, Max Bad Nucleotide %, [Max Defect Component], Mean Bad Nucleotide %, WSI-Intra, WSI-Inter, WSI-Intra-1, WSI-Inter-1, Verboten, WSI, Toehold Avg dG, Range of toehold dG's]
    # Want them to be:                    *       *        *        *         *         *        *        *       *    *      *       *                  *         *         *
    # TSI avg, TSI max, TO avg, TO max, BM sum, BM max, SSU min, SSU avg, SSTU min, SSTU avg, BN% max, BN% avg, WSAS, WSIS, WSAS-M, WSIS-M, Verboten, Spurious, dG error, dG range
    # yes spurious, no dG error, dG range  (i.e. old EW)
    #weights= [5,   20,     10,     30,      2,      3,      30,      10,       50,       20,      10,       5,    6,    4,      5,      3,        2,        8]
    # no spurious, yes dG error, dG range  (i.e. recent James)
    # weights = [5,   20,     10,     30,      2,      3,      30,      10,       50,       20,      10,       5,    6,    4,      5,      3,        2,        8,       20 ]
    # new weights, including dG error and dG range and spurious (i.e. new EW 2017)
    # weights = [5,   20,     10,     30,      2,      3,      30,      10,       50,       20,      10,       5,    6,    4,      5,      3,        2,        8,       10,       20 ]

    weights = [5,   20,     10,     30,      2,      3,      30,      10,       50,       20,      10,       5,    6,    4,      5,      3,        2,        8,       10,       20,	2 ]

    winner_dict = {}
    print()
    temp = [max(r) for r in ranks]
    winner_dict['worst-rank'] = mincases(temp)[0]
    print("Best worst-rank:                     {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))
    temp = [max(np.array(r)*weights/100.0) for r in ranks]
    winner_dict['worst-weighted-rank'] = mincases(temp)[0]
    print("Best worst-weighted-rank:            {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))
    temp = [sum(r) for r in ranks]
    winner_dict['sum-of-ranks'] = mincases(temp)[0]
    print("Best sum-of-ranks:                   {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))
    temp = [sum(np.array(r)*weights/100.0) for r in ranks]
    winner_dict['sum-of-weighted-ranks'] = mincases(temp)[0]
    print("Best sum-of-weighted-ranks:          {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))
    temp = [sum(f) for f in fractions]
    winner_dict['fractional-excess-sum'] = mincases(temp)[0]
    print("Best fractional excess sum:          {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))
    temp = [sum(np.array(f)*weights/100.0) for f in fractions]
    winner_dict['weighted-fractional-excess-sum'] = mincases(temp)[0]
    print("Best weighted fractional excess sum: {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))
    temp = [100*sum(p) for p in percents]
    winner_dict['percent-badness-sum'] = mincases(temp)[0]
    print("Best percent badness sum:            {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))
    temp = [sum(np.array(p)*weights) for p in percents]
    winner_dict['weighted-percent-badness-sum'] = mincases(temp)[0]
    print("Best weighted percent badness sum:   {:8.2f} by {:10s} and the worst: {:8.2f} by {:s}".format( min(temp), strmincases(temp), max(temp), strmaxcases(temp) ))

    # now make a new matrix showing, for each design:
    #  the worst-rank, sum-of-ranks, sum-of-weighted-ranks, fractional-excess, weighted-fractional-excess, percent-badness, weighted-percent-badness

    metascores=[
        [max(r) for r in ranks],
        [max(np.array(r)*weights/100.0) for r in ranks],
        [sum(r) for r in ranks],
        [sum(np.array(r)*weights/100.0) for r in ranks],
        [sum(f) for f in fractions],
        [sum(np.array(f)*weights/100.0) for f in fractions],
        [100*sum(p) for p in percents],
        [sum(np.array(p)*weights) for p in percents]
        ]

    metaranks=[]
    for col in metascores:
        # ties get same rank; next worse gets that rank+1; low rank is better
        array = np.array(col)
        array_uni = np.unique(array)
        array_ord = array_uni.argsort()
        rank_dict = dict(zip(array_uni, array_ord))
        temp_ranks = np.array([rank_dict[x] for x in array])
        temp = array.argsort()
        colranks = np.array([rank_dict[x] for x in array])
        metaranks.append(colranks)
    temp=metaranks
    metaranks=list(zip(*temp))

    print_fn("\nMetascores array:")
    print_fn("\n                                 Worst-rank (weighted)  Sum-of-ranks  (weighted) Fractional-excess (weighted) Percent-badness (weighted)")
    print_fn("\n")
    i=0
    for m in metaranks:
        print_fn("design {:3d}: {:6d} = sum [".format(i,sum(m)))
        for r in m:
            print_fn("{:13d}".format(r))
        print_fn("       ]\n")
        i=i+1

    temp = [sum(r) for r in metaranks]
    winner_dict['sum-of-metaranks'] = mincases(temp)[0]
    print("\nBest sum-of-metaranks: {:6d} by {:s}".format( min(temp), strmincases(temp) ))
    print()
    return winner_dict[method]

f1 = open(sys.argv[1])
OldLines=csv.reader(f1)
OldList=list(OldLines)
old_names=OldList[0]
old2=OldList[-1]
OldClose=csv.reader(f1,delimiter='\t')
f1.close()

f2 = open(sys.argv[2])
NewLines=csv.reader(f2)
NewList=list(NewLines)
new_names=NewList[0]
new2=NewList[-1]
NewClose=csv.reader(f2,delimiter='\t')
f2.close()

scores = [new_names]+[old2]+[new2]

winner = metarank(scores)
print (sys.argv[1:][winner])
#LowImportance=1
#HighImportance=10

#with open('current.csv') as f1:
#    old1 = f1.readline().split(',')
#    old2 = f1.readline().split(',')
#f1.close()
#
#with open('tempcurrent.csv') as f2:
#    new1 = f2.readline().split(',')
#    new2 = f2.readline().split(',')
#f2.close()

#scorer=0
#for i in range (1,len(old2)):
#    if i<7:
#        score=float(old2[i])-float(new2[i])
#	score=score*LowImportance
#    elif i<11:
#        score=float(new2[i])-float(old2[i])
#	score=score*HighImportance
#    else:
#        score=float(old2[i])-float(new2[i])
#	score=score*LowImportance
#    scorer=scorer+score

if ("tempc" in sys.argv[1:][winner]) and (float(old2[-1])<=float(new2[-1])):
    print (" ")
    print (" ")
    print (" ")
    print (" ")
    os.system('date')
    print ("Better sequence found!! Replacing...")
    os.system('notify-send "System Evolution" "Better sequence found!!"')
    print (" ")
    print (" ")
    print (" ")
    print (" ")
    os.remove('Best_Species/current.csv')
    dst_file='Best_Species/current.csv'
    src_file='Temporary_Species/tempcurrent.csv'
    shutil.copy(src_file, dst_file)
    os.remove('Best_Species/current.mfe')
    dst_file='Best_Species/current.mfe'
    src_file='Temporary_Species/tempcurrent.mfe'
    shutil.copy(src_file, dst_file)
    os.remove('Best_Species/current.pil')
    dst_file='Best_Species/current.pil'
    src_file='Temporary_Species/tempcurrent.pil'
    shutil.copy(src_file, dst_file)
    os.remove('Best_Species/current.seqs')
    dst_file='Best_Species/current.seqs'
    src_file='Temporary_Species/tempcurrent.seqs'
    shutil.copy(src_file, dst_file)
else:
    print (" ")
    print (" ")
    print (" ")
    print (" ")
    os.system('date')
    print ("Worse sequence found.")
    print (" ")
    print (" ")
    print (" ")
    print (" ")
