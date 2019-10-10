import os
with open(os.getcwd()+"/Temporary_Species/tempcurrent.seqs",'r')as f1:
    a= f1.readlines ()
f1.close()
j=[]
for i in a:
    if "strand" in i:
        j.append((i.split("=")[1])[1:-1])
b=[]
start=0
tup=[]
for i in range (0,len(j)):
    b.append('>')
    b.append('S')
    b.append('T')
    b.append('R')
    start=start+4
    t=list(str(i))
    for k in t:
        start=start+1
        b.append(str(k))
    b.append("\n")
    start=start+1
    s1=start
    t=list(j[i])
    for k in t:
        start=start+1
        b.append(k)
    b.append("\n")
    start=start+1
    s2=start
    s3=s2-s1
    tup.append(("STR"+str(i),s3-1,s1,s3))
with open("./PoBT-master/src/tdata/SGDv3.fasta",'w')as f2:
    f2.write("".join(b))
f2.close()
with open("./PoBT-master/src/tdata/SGDv3.fasta.fai",'w')as f3:
    for i in range (0,len(tup)):
        a,b,c,d=tup[i]
        f3.writelines(a+"\t"+str(b)+"\t"+str(c)+"\t"+str(b)+"\t"+str(d)+"\n")
f3.close()




