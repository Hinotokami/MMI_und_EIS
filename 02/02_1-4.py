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

def temp(val):
    n = len(val)
    index = np.square(np.arange(n))
    n += 1
    return(12*(np.sum(index*val)*(20*(n**4)+10*(n**3)+7*n*n+17*n+6)+
        np.sum(val)*n*(10*(n**5)+21*(n**4)+12*(n**3)-15*n*n-20*n-6))/
        (n*(100*(n**6)+62*(n**5)+337*(n**4)+530*(n**3)+199*n*n+8*n-36)))

tempT = temp(values[:,0])
tempM = temp(values[:,1])

def ace(val, temps):
    n = len(val)
    index = np.arange(n)
    n += 1
    return(12*(np.sum(index*val))-n*(np.sum(val)*(n+1)/2-
        6*temps*(2*n*n+6*n+4))/(n*n*(2*(n**3)+8*n*n+9*n+4)))

def cee(val,temps):
    n = len(val)
    index = np.arange(n)
    n += 1
    return((2*n+1)*(temps+np.sum(index*val))-np.sum(val)*(n*n+n)/
        (2*n*n*(n+1)))
    

aTSquared = ace(values[:,0], tempT)
aMSquared = ace(values[:,1], tempM)
bTSquared = tempT
bMSquared = tempM
cTSquared = cee(values[:,0], tempT)
cMSquared = cee(values[:,1], tempM)

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

plt.plot(range(n),[f(i,0) for i in range(n)],'k')
plt.plot(range(n),[f(i,1) for i in range(n)],'k')

plt.show()
