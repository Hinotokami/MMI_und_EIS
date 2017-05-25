class Set:
    def __init__(self, a):
        self.array = []
        self.out = ""
        for i in a:
            if i not in self.array:
                self.array.append(i)

    def __str__(self):
        if len(self.array) != 0:
            self.out += "{"
            for i in self.array:
                self.out += str(i) + ", "
            self.out = self.out[:-2] + "}"
            return self.out
        else: return "∅"

# Vereinigung
    def union(self, B):
        for i in B:
            if i not in self.array:
                self.array.append(i)

# Durchschnitt
    def intersect(self, B):
        temp = []
        for i in B:
            if i in self.array:
                temp.append(i)
        self.array = temp
# A/B
    def complement(self, B):
        temp = []
        for i in B:
            if i not in self.array:
                temp.append(i)
        self.array = temp
# Teilmenge
    def subset(self, f):
        temp = list(filter(f, self.array))
        return temp

# __ functions implemented
    def __iter__(self):
        return iter(self.array)
    def __contains__(self, item):
        if item in self.array:
            return True
        else: return False

    def __len__(self):
        return len(self.array)

    def __getitem__(self, i):
        return self.array[i]

    def product(self, otherSet):
        tuple = []
        for i in self.array:
            for j in otherSet:
                tuple.append((i,j))
        return sorted(tuple)
class CartesianProduct(Set):
    def __init__(self, a, f):
        Set.__init__(self, a)
        while True:
            try:
                self.cart = list(filter(f, self.array))
                break
            except  Exception:
                print("keine richtige Funktion")

    def __call__(self, a):
        for i in self.cart:
            if i[0] == a:
                return i[1]
            if i[1] == a:
                return i[0]
            else: return False
# 3.1.4 nicht ganz klar was gewollt ist
# #B ^#A mögliche zuordnungen

class Relation(CartesianProduct):
    def reflex(self):
        for i in self.cart:
            if (i,i) in self.cart:
                continue
            else: return False

    def trans(self):
        for i in self.cart:
            for j in self.cart:
                if i != j:
                    if i[1] == j[0]:
                        if (i, j[1]) not in self.cart:
                            return False
                    if i[1] == j[1]:
                        if (i, j[0]) not in self.cart:
                            return False
        return True

    def symm(self):
        for i in self.cart:
            if (i[1], i[0]) not in self.cart:
                return False
        return True


def emptysets(n):
    temp = ["∅"]
    for i in range(n):
        temp.append(list(temp))
    for i in range(len(temp)):
        print(i, ":=", temp[i])

#emptysets(5)

def powerset(Array):
    result = [[]]
    for i in Array:
        newsub = [subset + [i] for subset in result]
        result.extend(newsub)
    return sorted(result, key=len)

#print(powerset([1,2,3]))

def binomialCoefficients(num):
    def factorial(n):
        if n == 1:
            return 1
        else: return n * factorial(n -1)

    for i in range(1,num):
        print((factorial(num))/(factorial(i)* factorial(num - i)))

#binomialCoefficients(5)

A = Set([1,2,3])
B = Set([4,5,6])
print(A.product(B))


# 3.1.5 Fragen
"""
- Aufgrund der Transitivität. Ist das eine Element in der Klasse nicht in Relation zu
    dem zu Untersuchenden, so ist es keines der Klasse. Und andersherum


        Alice Bob Charles Denise Eric
Alice     x
Bob             x
Charles             x
Denise                      x
Eric                              x         -> Reflexiv - Diagonale


        Alice Bob Charles Denise Eric
Alice          x            x
Bob       x
Charles
Denise    x
Eric                                    ->  Symmetrisch - gespiegelt an der Diagonale -> gleiches Muster


        Alice Bob Charles Denise Eric
Alice     x    x            x
Bob       x    x            x
Charles   x    x            x
Denise
Eric                                        -> Transitiv ->  wenn eine Person eine andere mag müssen beide Spalten identisch sein


"""
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import numpy as np

app = qw.QApplication(sys.argv)

main = qw.QMainWindow()  # erstellen eines MainWindows
main.setWindowTitle("MANDEEEEEELBROT")
main.resize(800, 600)
breite , hoehe = 800, 600
npbild = np.zeros([breite,hoehe,4], dtype=np.uint8) # RGBA (A: Transparenz)
npbild += 255 # nun ist das Bild schwarz
npbild [20,30,:]  = [135,23,53,0] # setzen eines Farbpixels im Numpy−Array
npbild [20,30,0]  = 255           # setzen des Rotwertes eines anderen Pixels
img = qg.QImage(npbild, breite, hoehe, qg.QImage.Format_RGB32)

# KA wie man Mandelbrot implementieren soll -.-
display = qw.QLabel()  # Display


main.setCentralWidget(display)
main.show()
sys.exit(app.exec_())