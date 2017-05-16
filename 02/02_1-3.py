import numpy as np
import matplotlib.pyplot as plt

values=np.loadtxt("02_werte.txt",dtype=np.float,skiprows=3,usecols=(6,12))
n = len(values)
plt.plot(range(n),values[:,0],'o')
plt.plot(range(n),values[:,1],'o')
intervalSize = 100
runAv = np.array([np.mean(values[i-intervalSize/2:i+intervalSize/2,:],axis=0) 
    for i in range(intervalSize/2,n-intervalSize/2)])


plt.plot(range(intervalSize/2,n-intervalSize/2),runAv[:,0],'k')
plt.plot(range(intervalSize/2,n-intervalSize/2),runAv[:,1],'k')

plt.show()
