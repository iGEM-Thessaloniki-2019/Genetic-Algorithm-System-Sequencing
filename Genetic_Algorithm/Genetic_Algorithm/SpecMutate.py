import re
import random
import os
from datetime import datetime
import argparse
os.getcwd()

parser = argparse.ArgumentParser(description='The script mutates tempcurrent.pil .')
parser.add_argument('-sm','--specific_mut', default=None, type=str, help='The domains or toeholds to be mutated specificaly. For example, solo-d ')
parser.add_argument('-f', default=None)
args = parser.parse_args()

specific_mut=args.specific_mut
f=int(args.f)

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


random.seed(datetime.now())


f1=open(os.getcwd()+'/System/system.pil')
Htext=f1.read()
f1.close()
f1=open(os.getcwd()+'/System/system.pil')
l1=f1.readlines()[:1]
f1.close()
Htext=Htext[len(l1[0]):]

a=list(find_all(Htext, 'H'))
#filter non domain H's
fa=[]
for i in range (0,len(a)):
    if i==0:
        if a[0]+1==a[1]:
	    fa.append(a[0])
    elif i==len(a)-1:
	if a[len(a)-2]+1==a[len(a)-1]:
	    fa.append(a[len(a)-1])
    else:
	if a[i-1]+1==a[i] or a[i]+1==a[i+1]:
	    fa.append(a[i])

l=len(fa)
if specific_mut:
	ss=None
	p=Htext.find(specific_mut)
	for n in range(l-1):
		if fa[n] > p and (fa[n-1]<p or fa[n-1]==fa[-1]):
			ss=n
			print('ss ',ss)
			continue
		if ss and fa[n]!=fa[n-1]+1:
			ee=n-1
			print('ee ',ee)
			break

	r=random.randint(ss,ee)
else:
	print('No domain do be mutated was specified.\nProceeding to random mutataion.')
	r=random.randint(0,l-1)

if f:
    direc='/Temporary_Species/tempcurrent.pil'
else:
    direc='/Best_Species/current.pil'

f2=open(os.getcwd()+direc)
ctext=f2.read()
f2.close()
f2=open(os.getcwd()+direc)
l1=f2.readlines()[:1]
f2.close()
Ctext=ctext[len(l1[0]):]

Ttext=list(Ctext)
old=Ttext[fa[r]]
new=''.join(random.choice("ACT") for _ in range(1))
while old==new:
    new=''.join(random.choice("ACT") for _ in range(1))
Ttext="".join(Ttext)

Ttext="".join((Ttext[:fa[r]],new,Ttext[fa[r]+1:]))
with open(os.getcwd()+'/Temporary_Species/tempcurrent.pil','w') as f3:
    f3.write ('\n'+Ttext)
    print ("Mutation done! ** {}-{}-{}->{}".format(r,fa[r],old,new))
f3.close()
