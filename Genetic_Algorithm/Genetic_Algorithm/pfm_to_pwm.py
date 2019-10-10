import csv
import math 
import os


PWD=[]
with open(os.getcwd()+"/System/TF.pfm") as PFM_raw:
	csv_reader=csv.reader(PFM_raw , delimiter=' ')
	cnt=0
	cntbases=0
	for array in csv_reader:
		if len(array)==1:
			ab,bb,cb,db=list(array[0])
			ab="#"+ab
			bb="#"+bb
			cb="#"+cb
			db="#"+db
		PWD_elemts=""
		for element in array:
			try:
				a=float(element)
				aa=float(a)*0.25/19
				if aa==0:
					aa=-1000
				else:
					aa=math.log(aa,2)
				aga='{:6.3f}'.format(aa)
				if len(aga)>6:
					aga=aga[:6]
					if aga[-1]==".":
						aga=aga[:5]+" "
				PWD_elemts="    "+aga
				if cnt==1:
					ab=ab+PWD_elemts
					cntbases=cntbases+1
				elif cnt==2:
					bb=bb+PWD_elemts
				elif cnt==3:
					cb=cb+PWD_elemts
				elif cnt==4:
					db=db+PWD_elemts
			except:
				a=0
		cnt=cnt+1
	fl=""
	for i in range (0,cntbases):
		fl=fl+"       "+'{:3d}'.format(i)
	fl="#"+fl[1:]
	PWD.append(fl+"\n")
	PWD.append(ab+"\n")
	PWD.append(bb+"\n")
	PWD.append(db+"\n")
	PWD.append(cb+"\n")
with open(os.getcwd()+"/PoBT-master/src/data/yeast.tamo", 'r') as fi:
	h=fi.readlines()
fi.close()
for i in range (1,6):
	h[i]=PWD[i-1]
with open(os.getcwd()+"/PoBT-master/src/data/yeast.tamo",'w') as WW:	
	WW.writelines (h)
with open(os.getcwd()+"/PoBT-master/src/tdata/yeast.tamo",'w') as WW:	
	WW.writelines (h)
