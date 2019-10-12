import stickydesign
import matplotlib.pyplot as pyplot
from stickydesign import plots
import statistics
b=['ctgttt', 'tcattc', 'aacacc', 'taccca', 'ttacag', 'ttatcc', 'tatcag']


aa=stickydesign.endclasses.endarray(array=b,endtype="S")
aa=[aa,aa]

#aa=stickydesign.easyends('S',6,number=7, maxspurious=0.4,interaction=0, tries=2,energetics=stickydesign.EnergeticsBasic(temperature=37), adjs=['c','g'],alphabet='h')

print(aa)

i=1
toe=aa[0]

energyarray=stickydesign.energy_array_uniform(toe,stickydesign.EnergeticsBasic(temperature=37))
maxs=[]
for arr in energyarray:
	maxim= max(arr)
	maxs.append(maxim) 
print('Maxs:',maxs)
print("Variance of %s set is % s" %(i,statistics.variance(maxs))) 
print("Mean of %s set is % s" %(i,statistics.mean(maxs)))
print("Max Energy toehold %s - Min Energy Toehold %s is %s" %(max(maxs),min(maxs),max(maxs)-min(maxs)))

fig=stickydesign.plots.heatmap(toe,stickydesign.EnergeticsBasic(temperature=37))
pyplot.show(fig)
i=i+1


