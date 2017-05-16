import numpy as np
import matplotlib.pyplot as plt

values=np.loadtxt("02_werte.txt",dtype=np.float,skiprows=3,usecols=(6,12))
n = len(values)
plt.plot(range(n),values[:,0],'o')
plt.plot(range(n),values[:,1],'o')

def mLinear(value):
    return((12*np.sum([(i-1)*value[i] for i in range(n)])-6*n*n*np.mean(value))/(n*(n*(n-6)-2)))

mTLinear = mLinear(values[:,0])
mMLinear = mLinear(values[:,1])
bTLinear = np.mean(values[:,0])-mTLinear*(n-1)/2
bMLinear = np.mean(values[:,1])-mMLinear*(n-1)/2

plt.plot([0,n-1],[bTLinear, bTLinear+mTLinear*(n-1)],'k')
plt.plot([0,n-1],[bMLinear, bMLinear+mMLinear*(n-1)],'k')

aTSquared = 1   #
aMSquared = 1   #
bTSquared = 1   #
bMSquared = 1   #
cTSquared = 1   #
cMSquared = 1   #

def f(x,K):
    if K==0:
        a=aTSquared
        b=bTSquared
        c=cTSquared
    else:
        a=aMSquared
        b=bMSquared
        c=cMSquared
    return(a*x*x+b*x+c*x)

#plt.plot(range(n),[f(i,0) for i in range(n)],'k')
#plt.plot(range(n),[f(i,1) for i in range(n)],'k')

plt.show()
