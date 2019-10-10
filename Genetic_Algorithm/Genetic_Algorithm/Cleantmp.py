import os
with open ("System/tmps.txt",'r') as f1:
    a=f1.readline ().replace("[","").replace("]","").replace("'","").replace(" ","").split(',')
f1.close()
b=os.listdir("/tmp")
for i in b:
    if i not in a:
        try:
            os.remove("/tmp/"+i)
        except:
            print ("Unable to delete temporary file " +i)
    
