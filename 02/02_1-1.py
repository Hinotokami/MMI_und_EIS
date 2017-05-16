import numpy as np
import matplotlib.pyplot as plt

def lagr(k,x,valueX):
    fraction = 1
    for i in range(len(valueX)):
        if not i==k:
            fraction *= (x-valueX[i])
            fraction /= (valueX[k]-valueX[i])
    return fraction
    
    
def polX(x,valueX,valueY):
    prod = 1
    for i in range(1,len(valueX)):
        prod += valueY[i]*lagr(i,x,valueX)
    return prod

values=np.loadtxt("02_werte.txt",dtype=np.float,skiprows=3,usecols=(6,12))
n = len(values)
randSize = 10
randTX = [int(i) for i in np.linspace(0,n-1,randSize)]
randTY = values[randTX,0]
randMX = [int(i) for i in np.linspace(0,n-1,randSize)]
randMY = values[randMX,1]
sampleSize = 100
samples = np.linspace(0,n-1,sampleSize)
interpoledT = []
interpoledM = []
for i in samples:
    interpoledT.append(polX(i,randTX,randTY))
    interpoledM.append(polX(i,randMX,randMY))

plt.plot(range(n),values[:,0],'o')
plt.plot(range(n),values[:,1],'o')
plt.plot(samples,interpoledT,'k')
plt.plot(samples,interpoledM,'k')

plt.show()


"""In Matplotlib plotten, verschiedene Achsen, Farben
   Linie zeichnen -> Interpolation
   lagrenge-polynome als transparente im Hintergrund"""
