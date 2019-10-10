import pandas as pd
import os

with open (os.getcwd()+"/System/tf.config",'r') as f1:
	aa=f1.readlines()
f1.close()
hitno=int(aa[0].split("=")[1].split("\n")[0])
strand=[]
pos=[]
scor=0
for i in range(1,hitno*2+1,2):
	strand.append(aa[i].split("=")[1].split("\n")[0].replace(" ",""))
	pos.append(int(aa[i+1].split("=")[1].split("\n")[0].replace(" ","")))
try:
	scor=0
	b=pd.read_csv(os.getcwd()+"/PoBT-master/toutput/hits/HitsHSF1.gff",delimiter='\t',header=None)
	for i in range(0,len(b)):
		if b.iloc[i,0] in strand:
			if b.iloc[i,3]==pos[strand.index(b.iloc[i,0])]:
				scor=scor+b.iloc[i,5]
			else:
				scor=scor-b.iloc[i,5]
		else:
			scor=scor-b.iloc[i,5]
except:
	b=0
	scor=0
with open(os.getcwd()+"/Temporary_Species/tempcurrent.csv",'r') as f2:
	ss=f2.readlines()

f2.close()
l1=(ss[0].split("\n")[0]).split(",")
l2=(ss[1].split("\n")[0]).split(",")
if l1[-1]!="Tf_score":
	l1.append("Tf_score")
	l2.append(str(scor))

	with open(os.getcwd()+"/Temporary_Species/tempcurrent.csv", "w") as f3:
		for i in l1:
			f3.write(i)
			if (i==l1[-1]):
				f3.write("\n")
			else:
				f3.write(",")
		for i in l2:
			f3.write(i)
			if (i==l2[-1]):
				f3.write("\n")
			else:
				f3.write(",")
	f3.close()
print(scor)

