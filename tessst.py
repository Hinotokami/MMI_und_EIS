import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class MainWindow(qw.QMainWindow):           # Klasse mit parent qw.QMainWindow , welche auf Tastendruck reagiert
    def __init__(self, parent=None):
        qw.QMainWindow.__init__(self, parent)

    def keyPressEvent(self, e):
        if e.key() == qc.Qt.Key_Left:
            snake.addSpeed(-1, 0)
        if e.key() == qc.Qt.Key_Right:
            snake.addSpeed(1, 0)
        if e.key() == qc.Qt.Key_Up:
            snake.addSpeed(0, -1)
        if e.key() == qc.Qt.Key_Down:
            snake.addSpeed(0, 1)
        if e.key() == qc.Qt.Key_Space:
            enablebtn()

# Farbwerte, welche zum anzaigen gebraucht werden
color1 = 0xff50B4D8  # blue
color2 = 0xffFFBC46  # orange
color3 = 0xffffffff  # white
color4 = 0xff000000  # black
color5 = 0xff00BFFF  # dark blueh


class Snake():
    def __init__(self):     # Initialisiert die KLasse mit wichtigen Variablen
        self.x = 1
        self.y = 1
        self.movex = 1
        self.movey = 0
        self.point = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.eatennode = []
        self.node = []
        self.loose = False
        self.count = 0
        self.pause = True
        self.won = False
        self.eaten = False
        self.points = 0

    #def addPoint(self) war redundant, wurde auch nie aufgerufen

    def restart(self):              # Funktion für den Button "Neustart"
        self.x = 1
        self.y = 1
        self.movex = 1
        self.movey = 0
        self.point = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.node = []
        self.loose = False
        self.won = False
        self.pause = True
        self.eatennode = []
        self.eaten = False
        self.points = 0
        timer.start()
        enableAll()

    def drawSnake(self):
        import random

        if not self.loose:                      # zeichnet Display bei nicht verlorenem Spiel
            self.deleatennode()
            btn.setEnabled(False)
            bild = qg.QImage(feldbreite, feldbreite, qg.QImage.Format_RGB32)
            if self.pause:
                bild.fill(qc.Qt.white)
            else:
                bild.fill(qc.Qt.black)
            if self.pause:
                for i in self.point:
                    bild.setPixel(i[0], i[1], color4)
            else:
                for i in self.point:
                    bild.setPixel(i[0], i[1], color1)
            if len(self.eatennode) != 0:
                bild.setPixel(self.eatennode[0], self.eatennode[1], color5)
            z = random.randint(0, 10000000)
            if z < chance:
                self.addNode()
            self.NodeEat()
            if len(self.node) != 0:
                if self.pause:
                    bild.setPixel(self.node[0][0], self.node[0][1], color4)
                else:
                    bild.setPixel(self.node[0][0], self.node[0][1], color2)
            pixmap = qg.QPixmap.fromImage(bild)
            scaledpixmap = pixmap.scaled(Zoom, Zoom, qc.Qt.KeepAspectRatio)
            display.setPixmap(scaledpixmap)
            main.show()
        else:                           # zeichnet Display im Falle einer Niederlage
            timer.stop()
            btn.setEnabled(True)
            if self.won:
                self.wonText()
            else:
                self.lostText()
            self.showText()
            bild = qg.QImage(feldbreite, feldbreite, qg.QImage.Format_RGB32)
            bild.fill(qc.Qt.white)
            pixmap = qg.QPixmap.fromImage(bild)
            scaledpixmap = pixmap.scaled(Zoom, Zoom, qc.Qt.KeepAspectRatio)
            display.setPixmap(scaledpixmap)
            main.show()

    def addSpeed(self, x, y):               # Richtungsspeed bei Tastendruck (ArrowKeys)
        if self.isvalidmove(x, y):
            self.movex = x
            self.movey = y
        else:
            pass

    def isvalidmove(self, x, y):        # Fängt die Fälle des Übertretens am Bildschrimrand ab
        if self.movex == x:             # -> if self.movex == x => self.movex = x, self.movey = y??
            return False                # warum brauchen wir das? Der Bildschirmrand wird in moveIt abgefangen
        elif self.movey == y:
            return False
        else:
            return True

    def moveIt(self):               # für das Bewegen der Schlange verantwortlich
        if not self.pause:
            self.lose()
            x = self.point[0][0] + self.movex
            y = self.point[0][1] + self.movey
            if x > feldbreite - 1:
                x = 0
            if x < 0:
                x = feldbreite - 1
            if y < 0:
                y = feldbreite - 1
            if y > feldbreite - 1:
                y = 0
            self.point.insert(0, (x, y))
            if not self.eaten:
                self.point.__delitem__(-1)
        else:
            pass

    def grow(self):                             # Lässt die Schlange wachsen
        self.eaten = True                       # hab das mal geändert...
        self.moveIt()
        self.eaten = False
        self.points += 1

    def addNode(self):              # fügt eine Frucht auf das Feld hinzu
        import random
        if len(self.node) == 0:
            x = random.randint(0, feldbreite - 1)
            y = random.randint(0, feldbreite - 1)
            if not ((x, y) in self.point):
                self.node = [(x, y)]

    def deleatennode(self):             # Löscht node aus dem eatenarray
        if self.eatennode == self.point[-1]:
            self.eatennode = []

    def NodeEat(self):              # prüft, ob eine Frucht gegessen wurde
        if len(self.node) != 0:
            if self.point[0] == self.node[0]:
                self.eatennode = self.node[0]
                self.node = []
                self.grow()

    def lose(self):
        for i in self.point[1:]:
            if self.point[0] == i:
                self.loose = True
                self.pause = True
        if len(self.point) == 900:  # number of fields; variable
            self.won = True

    def lostText(self):
        self.title = "%s! You \'lost\': %d" % (player_name, self.points)
    
    def wonText(self):
        self.title = "%s! You won: %d" % (player_name, self.points)
    
    def showText(self):
        path = "highscores.txt"
        pos = False
        data = open(path, 'r+')
        scores = data.readlines()
        playerPoints = []
        playerNames = []
        if len(scores) == 0:
            playerPoints.append(self.points)
            playerNames.append(player_name)
            position = 1
            pos = True
        else:
            for i in scores:
                current = i.split()
                playerPoints.append(int(current[0]))
                playerNames.append(current[1])
            playerPoints.append(0)
            for i in range(0, len(playerPoints)):
                if playerPoints[i] <= self.points:
                    playerPoints.insert(i, self.points)
                    playerNames.insert(i, player_name)
                    position = i+1
                    pos = True
                    break
            playerPoints.pop()
            if len(playerPoints) > 10:
                playerPoints.pop()
                playerNames.pop()

        data.truncate(0)
        data.seek(0)
        showA = []
        for i in range(0, len(playerPoints)):
            line = "%d %s\n" % (playerPoints[i], playerNames[i])
            data.write(line)
            lineS = "%d. %s" % (i + 1, line)
            showA.append(lineS)
        data.close()
        show = ''.join(showA)
        
        if pos:
            if self.won:
                inStr = "And"
            else:
                inStr = "But"
            message = "%s you made the Highscore at %d. place! Wanna see?" % (inStr, position)
        else:
            if self.won:
                inStr = "But"
            else:
                inStr = "And"
            message = "%s didn't make the Highscore... still wanna see?" % inStr
        
        showMess = qw.QMessageBox.question(display, self.title, message, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                          qw.QMessageBox.Yes)
        if showMess == qw.QMessageBox.Yes:
            highsc = qw.QMessageBox.question(display, "Highscores", show, qw.QMessageBox.Ok, qw.QMessageBox.Ok)



def menue():  # verwaltet alle Menue Funktionen
    global chance, player_name, feldbreite, Zoom
    timer.setInterval(1 / e1.value() * 300)           # Geschwindigkeit
    chance = e5.value() * 100000                    # Fruchtwahrscheinlichkeit
    player_name = e7.text()                         # SPieler Name für den Highscore
    feldbreite = e9.value()
    Zoom = (2 + e11.value()) * 200


def enablebtn():            # Aktiviert Pause / Start
    e2.setEnabled(True)
    e3.setEnabled(True)


def enableAll():            # Aktiviert Alle Buttons / Settings
    e1.setEnabled(True)
    e2.setEnabled(True)
    e3.setEnabled(True)
    e4.setEnabled(True)
    e5.setEnabled(True)
    e6.setEnabled(True)
    e7.setEnabled(True)
    e8.setEnabled(True)
    e9.setEnabled(True)
    e10.setEnabled(True)
    e11.setEnabled(True)


def pauseIt():
    snake.pause = True


def startIt():
    snake.pause = False
    e1.setEnabled(False)
    e2.setEnabled(False)
    e3.setEnabled(False)
    e4.setEnabled(False)
    e5.setEnabled(False)
    e7.setEnabled(False)
    e9.setEnabled(False)
    e11.setEnabled(False)

    enablebtn()



def formate():
    mainform = qw.QWidget()         # Complete widgets
    form = qw.QWidget()             # Widget for display
    form2 = qw.QWidget()            # Widget for settings
    form4 = qw.QGridLayout()        # Layout for display
    form3 = qw.QGridLayout()        #layout for settings

    form3.addWidget(e6, 0, 0)       # fügt alle Widgets in das Layout für Settings hinzu
    form3.addWidget(e7, 0, 1)
    form3.addWidget(e0)
    form3.addWidget(e1)
    form3.addWidget(e4)
    form3.addWidget(e5)
    form3.addWidget(e8)
    form3.addWidget(e9)
    form3.addWidget(e10)
    form3.addWidget(e11)
    form3.addWidget(e2)
    form3.addWidget(e3)
    form3.addWidget(btn)

    form4.addWidget(display)        # fügt das display in layout fürs display hinzu
    form.setLayout(form3)           # Widget erhält passende Layout
    form2.setLayout(form4)            # Das Widget erhält das passende Layout
    form5 = qw.QGridLayout()        # Vereinigt beide Widgets in einem Grid
    form5.addWidget(form2, 0, 0)
    form5.addWidget(form, 0, 1)
    mainform.setLayout(form5)           # MainWidget erhält das fertige Layout
    main.setCentralWidget(mainform)     # MainWIndow wird das centrale Widget zugewiesen


app = qw.QApplication(sys.argv)

main = MainWindow()                 # erstellen eines MainWindows
main.setWindowTitle("Sssssnake")
main.resize(800, 600)


display = qw.QLabel()           # Display des SPiels
snake = Snake()                 # anlegen einer Veriable der Klasse Snake
snake.pause = True              # initialisierung des SPiels beim ersten Start
feldbreite = 10
Zoom = 600
chance = 1000000
snake.addNode()

# erstellen der Buttons des Settings
btn = qw.QPushButton("Neustart")
btn.setEnabled(False)
btn.pressed.connect(snake.restart)

e0 = qw.QLabel("Speed:")  # Geschwindigkeitseinstellungen
e1 = qw.QSpinBox()
e1.setMinimum(1)
e1.setMaximum(8)

e2 = qw.QPushButton("Pause")  # Pause Button
e2.clicked.connect(pauseIt)

e3 = qw.QPushButton("Start")  # Start Button
e3.clicked.connect(startIt)

e4 = qw.QLabel("Fruchtwahrscheinlichkeit in %:")
e5 = qw.QSpinBox()
e5.setMinimum(0)
e5.setValue(50)
e5.setMaximum(100)

e6 = qw.QLabel("Spieler Name")
e7 = qw.QLineEdit()

e8 = qw.QLabel("Feldbreite")
e9 = qw.QSpinBox()
e9.setMinimum(10)
e9.setMaximum(30)

e10 = qw.QLabel("Zoom")
e11 = qw.QSpinBox()
e11.setMinimum(1)
e11.setMaximum(3)


formate()               # funktion, welche das Format für das Mainwindow erstellt

menu = main.menuBar()           # erstellen der MenüBar
menu.setNativeMenuBar(False)
m1 = menu.addMenu("Spiel")                  # einfügen von Optionen
m1a = m1.addAction("Neustarten")
m1a.setStatusTip("Startet das Spiel neu")
m1a.triggered.connect(lambda: snake.restart())
m1.addSeparator()
m1b = m1.addAction("Beenden")
m1b.triggered.connect(lambda: main.close())
m1b.setStatusTip("Beendet das Spiel")
stat = main.statusBar()

# Game Timer für das Aktualisieren der Frames
timer = qc.QTimer()
timer.start(0)
timer.setInterval(100)
timer.timeout.connect(snake.moveIt)
timer.timeout.connect(snake.drawSnake)
timer.timeout.connect(menue)

sys.exit(app.exec_())
