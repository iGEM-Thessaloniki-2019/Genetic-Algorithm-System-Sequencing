import os
import shutil
i=0
while os.path.isfile(os.getcwd()+'/Ark/save{a:05d}.csv'.format(a=i)):
    i=i+1
dst_file=os.getcwd()+'/Ark/save{a:05d}.csv'.format(a=i)
src_file=os.getcwd()+'/Best_Species/current.csv'
shutil.copy(src_file, dst_file)
dst_file=os.getcwd()+'/Ark/save{a:05d}.seqs'.format(a=i)
src_file=os.getcwd()+'/Best_Species/current.seqs'
shutil.copy(src_file, dst_file)
