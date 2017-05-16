import numpy as np
import matplotlib.pyplot as plt

# Einlesen der Daten aus der Datei Rohdaten.txt
tabelle =np.loadtxt("Rohdaten.txt")
# extrahieren der passenden Spalten
temp = tabelle[:,6]                 # Temperatur Werte
nied = tabelle[:,12]                # Niederschlagswerte


#   Datensatz für das Lagrange Polynom aufteilen
#   Gleichzeitig Erstellen eines Train und Test Satzes für die Cross Validation
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
    eingabe: Stelle der auswertung und x-Werte , y-Werte des Datensatzes
    """
    def basis(j):
        import functools
        import operator
        p = [(x - xs[m])/(xs[j] - xs[m]) for m in range(k) if m != j]
        return functools.reduce(operator.mul , p)
    assert len(xs) != 0 and (len(xs) == len(ys)) , "x and y darf nicht leer sein"
    k = len(xs)
    return sum(basis(j) * ys[j] for j in range(k))

temp3 = []
# erstellen der x,y Werte für das Lagrange Polynom
for i in range(0,500):
    temp3.append(lagrange(i, temp2x, temp2))



# Mittelwert
tempmiddle = []         # y werte
tempmiddlex = []        # x werte
for i in range(50, len(temp), 50):
    tempmiddle.append(np.mean(temp[i - 50:i]))
    tempmiddlex.append((i + (i - 50)) / 2)

# laufender Mittelwert
tempmidrun = []
tempmidrunx = []
# for Schleife fängt bei 50 an und geht 1er Schritte
for i in range(50, len(temp)):
    tempmidrun.append(np.mean(temp[i - 50:i]))      # Sliced immer 50er Fenster and Werten
    tempmidrunx.append((i + (i - 50)) / 2)          # appended mittelwert und x wert

# erstellen der subplots
fig, ax1 = plt.subplots()
# statt plt.plot nun ax1.plot

# aus xlabel und xlim wird set_xlabel und set_xlim
ax1.set_xlabel("Zeitpunkt")
ax1.set_ylabel("Temp")
# Färben der y−Achse
ax1.tick_params("y", colors="r")
ax1.plot(temp, "r")

# plottet Mittelwert und den Laufenden Mittelwert
plt.plot(tempmiddlex, tempmiddle, "k--", color="r")
plt.plot(tempmidrunx, tempmidrun, "k--", color="g")

# plottet lagrange
plt.plot(temp3, "k--")

# lineare regression  mithilfe der im Aufgabenteil gegebenen formel
x2 = np.arange(0,500)
A = np.vstack([x2, np.ones(len(temp))]).T      # transponiert die x-Achse mit einsen
m, c = np.linalg.lstsq(A, temp)[0]              # berechnet mittels Numpy Befehl m und c
plt.plot(x2, m*x2 +c, "r", label="Fitted Line")    # plottet die Gleichung m*x+c

# Moving least Squares mittels linear Reg
movey = []
for i in range(450):            # Fensterbreite 50
    A1 = np.vstack([x2[i:i+50], np.ones(50)]).T
    m1, c1 = np.linalg.lstsq(A1, temp[i:i+50])[0]
    movey.append(m1*((i+i+50)/2) + c1)

plt.plot([i+50/2 for i in range(len(movey))], movey)        # X-Achse Anpassung da Fensterbreite = 50

def polyfit(x2, temp):
    """
    polyfit Methode - Polynomielle Regression
    Eingabe : x-Werte und Y-Werte
    Ausgabe : [X-Werte] , [Y-Werte]
    """
    coeff = np.polyfit(x2, temp, 5)
    poly = np.poly1d(coeff)
    poly3 = poly(np.linspace(0,500,500))
    poly2 = np.linspace(0,500,500)
    return poly2, poly3

p2, p3 = polyfit(x2, temp)      # Polynomielle Reg über den Kompletten Datensatz
plt.plot(p2, p3, "--", color="k")

# zweite y−Achse (mit der gleichen x−Achse)
ax2 = ax1.twinx()
ax2.set_ylabel("Niederschlag")
ax2.tick_params("y")
ax2.plot(nied, "b .")
def cross(trainx, trainy, temp):
    """
    :param temp3:  erstellter datensatz datensatz Y-Werte
    :param temp:  kompletter datensatz
    :param temp2x: train datensatz  - X-Werte
    :return: Qualität E
    """
    e = 0
    for i in range(len(trainy)):
        if i not in trainx:                     # überspringt die für den Train Datensatz verwendete Daten
            e += (trainy[i] - temp[i])**2       # Berechnung aus der Aufgabenstellung
    e = e/(len(temp)- len(trainx))
    return e

eLagrange = cross(temp2x, temp3, temp)

# testfälle für den Polyfit
p5, p6 = polyfit(x2[::50], temp[::50])
p5train = [i for i in range(500) if i%50 == 0]

ePolyReg = cross(p5train, p6, temp)
print(eLagrange)
print(ePolyReg)

"""
# Gitter Für den Plot
for i in range(10):
    plt.axhline(5*i, color="b", alpha=2)
    plt.axvline(50*i, color="b", alpha=2)
"""


plt.show()


