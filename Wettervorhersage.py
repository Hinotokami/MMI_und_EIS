import numpy as np
import matplotlib.pyplot as plt

# reading data from data file
table =np.loadtxt("Rohdaten.txt")
# extract the respective coloumns
temp = table[:,6]                 # temperature
rain = table[:,12]                # rainfall


#   splitting dataset for langrange polynome
#   train and test sets for cross validation
temp2 = []
temp2x = []
for i in range(0, len(temp)+1, 75):
    temp2.append(temp[i])
    temp2x.append(i)
temp2test = []
temp2xtest = []
for i in range(0, len(temp)):
    if i % 75 != 0:
        temp2test.append(temp[i])
        temp2xtest.append(i)

def lagrange(x, xs, ys):
    """
    input: dataset values xs and ys, point of evaluation x
    """
    def basis(j):
        import functools
        import operator
        p = [(x - xs[m])/(xs[j] - xs[m]) for m in range(k) if m != j]
        return functools.reduce(operator.mul , p)
    assert len(xs) != 0 and (len(xs) == len(ys)) , "x and y cannot be empty"
    k = len(xs)
    return sum(basis(j) * ys[j] for j in range(k))

temp3 = []
# get values for lagrange
for i in range(0,500):
    temp3.append(lagrange(i, temp2x, temp2))



# mean values
tempmiddle = []         # y values
tempmiddlex = []        # x values
for i in range(50, len(temp), 50):
    tempmiddle.append(np.mean(temp[i - 50:i]))
    tempmiddlex.append((i + (i - 50)) / 2)

# running averages
tempmidrun = []
tempmidrunx = []
for i in range(50, len(temp)):
    tempmidrun.append(np.mean(temp[i - 50:i]))      # slice intervals
    tempmidrunx.append((i + (i - 50)) / 2)          # appended mean

fig, ax1 = plt.subplots()

# axis modification
ax1.set_xlabel("Time")
ax1.set_ylabel("Temp")
ax1.tick_params("y", colors="r")
ax1.plot(temp, "r")

# plot mean and running average
plt.plot(tempmiddlex, tempmiddle, "k--", color="r")
plt.plot(tempmidrunx, tempmidrun, "k--", color="g")

# plot lagrange
plt.plot(temp3, "k--")

# linear regression
x2 = np.arange(0,500)
A = np.vstack([x2, np.ones(len(temp))]).T      # transpose x axis
m, c = np.linalg.lstsq(A, temp)[0]              # get m, c
plt.plot(x2, m*x2 +c, "r", label="Fitted Line")    # plot graph

# moving least squares
movey = []
for i in range(450):            # chunks of width 50
    A1 = np.vstack([x2[i:i+50], np.ones(50)]).T
    m1, c1 = np.linalg.lstsq(A1, temp[i:i+50])[0]
    movey.append(m1*((i+i+50)/2) + c1)

plt.plot([i+50/2 for i in range(len(movey))], movey)        # adjust axis

def polyfit(x2, temp):
    """
    polyfit method - polynomial regression
    input : data values
    output: fitting values
    """
    coeff = np.polyfit(x2, temp, 5)
    poly = np.poly1d(coeff)
    poly3 = poly(np.linspace(0,500,500))
    poly2 = np.linspace(0,500,500)
    return poly2, poly3

p2, p3 = polyfit(x2, temp)      # polyfit for complete  data
plt.plot(p2, p3, "--", color="k")

# second y axis
ax2 = ax1.twinx()
ax2.set_ylabel("Rainfall")
ax2.tick_params("y")
ax2.plot(rain, "b .")
def cross(trainx, trainy, temp):
    """
    :param temp3:  selected data Y
    :param temp:  complete data
    :param temp2x: training data X
    :return: quality E
    """
    e = 0
    for i in range(len(trainy)):
        if i not in trainx:                     # use non-training data
            e += (trainy[i] - temp[i])**2
    e = e/(len(temp)- len(trainx))
    return e

eLagrange = cross(temp2x, temp3, temp)

# test cases for polyfit
p5, p6 = polyfit(x2[::50], temp[::50])
p5train = [i for i in range(500) if i%50 == 0]

ePolyReg = cross(p5train, p6, temp)
print(eLagrange)
print(ePolyReg)

"""
# sections for plot
for i in range(10):
    plt.axhline(5*i, color="b", alpha=2)
    plt.axvline(50*i, color="b", alpha=2)
"""


plt.show()


