import numpy as np
import matplotlib.pyplot as plt

values=np.loadtxt("02_werte.txt",dtype=np.float,skiprows=3,usecols=(6,12))
n = len(values)
plt.plot(range(n),values[:,0],'o')
plt.plot(range(n),values[:,1],'o')
sampleSize = 10
sampleBounds = [int(i) for i in np.linspace(0,n-1,sampleSize)]
meanT = []
meanM = []
meanX = []
for i in range(sampleSize-1):
    intervalT = []
    intervalM = []
    for j in range(sampleBounds[i],sampleBounds[i+1]):
        intervalT.append(values[j,0])
        intervalM.append(values[j,1])
    meanT.append(np.mean(intervalT))
    meanM.append(np.mean(intervalM))
    meanX.append(int((sampleBounds[i]+sampleBounds[i+1])/2));

meanSize = 100
plt.plot(meanX,meanT,'k')
plt.plot(meanX,meanM,'k')

plt.show()
