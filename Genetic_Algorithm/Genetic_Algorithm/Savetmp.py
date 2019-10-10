import os
a=os.listdir("/tmp")
with open ("System/tmps.txt",'w') as f1:
    f1.write (str(a))
f1.close()
