# I n i t i a l i s i e r u n g wie ü b l i c h
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


color1 = 0xff50B4D8     # blue
color2 = 0xffFFBC46     # orange
color3 = 0xffffffff     # white
color4 = 0xff000000     # black
color5 = 0xff00BFFF    # dark blueh


class Snake():

    def __init__(self):
        self.x = 1
        self.y = 1
        self.movex = 1
        self. movey = 0
        self.point = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.eatennode = []
        self.node = []
        self.loose = False
        self.count = 0
        self.pause = True
        self.won = False

    def addPoint(self):
        last = self.point[-1]
        newx = last[0] + self.movex
        newy = last[1] + self.movey
        self.point += (newx, newy)

    def restart(self):
        self.x = 1
        self.y = 1
        self.movex = 1
        self.movey = 0
        self.point = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.node = []
        self.loose = False
        self.won = False
        self.pause = True
        timer.start()
        enableAll()

    def drawSnake(self):
        import random

        if not self.loose:
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
        else:
            timer.stop()
            btn.setEnabled(True)
            if self.won:
                self.wonText()
            else:
                self.lostText()
            bild = qg.QImage(feldbreite, feldbreite, qg.QImage.Format_RGB32)
            bild.fill(qc.Qt.white)
            pixmap = qg.QPixmap.fromImage(bild)
            scaledpixmap = pixmap.scaled(Zoom, Zoom, qc.Qt.KeepAspectRatio)
            display.setPixmap(scaledpixmap)
            display.show()

    def addSpeed(self, x, y):
        if self.isvalidmove(x, y):
            self.movex = x
            self.movey = y
        else:
            pass

    def isvalidmove(self, x, y):
        if self.movex == x:
            return False
        elif self.movey == y:
            return False
        else:
            return True

    def moveIt(self):
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
            self.point.__delitem__(-1)
        else:
            pass

    def grow(self):
        x = self.point[0][0] + self.movex
        y = self.point[0][1] + self.movey
        self.point.insert(0, (x, y))

    def addNode(self):
        import random
        if len(self.node) == 0:
            x = random.randint(0, feldbreite - 1)
            y = random.randint(0, feldbreite - 1)
            if not((x, y) in self.point):
                self.node = [(x, y)]

    def deleatennode(self):
        if self.eatennode == self.point[-1]:
            self.eatennode = []

    def NodeEat(self):
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
        lostMess = qw.QMessageBox.question(
            display, "Lost", "Sorry, you suck", qw.QMessageBox.Ok, qw.QMessageBox.Ok)

    def wonText(self):
        points = 1000  # change!
        name = "TESTNAMEIAMSOCOOL"  # change!

        path = "highscores.txt"
        pos = False
        data = open(path, 'r+')
        scores = data.readlines()
        playerPoints = []
        playerNames = []
        if len(scores) == 0:
            playerPoints.append(points)
            playerNames.append(name)
            pos = True
        else:
            for i in scores:
                current = i.split()
                playerPoints.append(int(current[0]))
                playerNames.append(current[1])
            for i in range(0, len(playerPoints)):
                if playerPoints[i] <= points:
                    playerPoints.insert(i, points)
                    playerNames.insert(i, name)
                    pos = True
                    break
            if len(playerPoints) > 10:
                playerPoints.pop(len(playerPoints))
                playerNames.pop(len(playerNames))

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
            message = "And you made the Highscore! Wanna see?"
        else:
            message = "You didn't make the Highscore... still wanna see?"
        wonMess = qw.QMessageBox.question(
            display, "You won", message, qw.QMessageBox.Yes | qw.QMessageBox.No, qw. QMessageBox.Yes)
        if wonMess == qw.QMessageBox.Yes:
            highsc = qw.QMessageBox.question(
                display, "Highscores", show, qw.QMessageBox.Ok, qw.QMessageBox.Ok)


class TastenTest(qw.QWidget):
    # e i n f a c h e s Layout

    def __init__(self):
        super().__init__()
        self.show()


# Übe r laden der l e e r e n Standardfunkt ion
    def keyPressEvent(self, e):
        #self.statusBar().showMessage("Taste mit key−code "+str(e.key())+" gedrückt", 1000)
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


def menue():    # verwaltet alle Menue Funktionen
    global chance, player_name, feldbreite, Zoom
    timer.setInterval(1 / e1.value() * 300)       # Geschwindigkeit
    chance = e5.value() * 100000        # Fruchtwahrscheinlichkeit
    player_name = e7.text()  # SPieler Name für den Highscore
    feldbreite = e9.value()
    Zoom = (2 + e11.value()) * 200


def enablebtn():
    e2.setEnabled(True)
    e3.setEnabled(True)
    e4.setEnabled(True)


def enableAll():
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
    timecounter.start()
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

app = qw.QApplication(sys.argv)
main = qw.QMainWindow()
main.setWindowTitle("Sssssnake")
main.resize(800, 600)

ex = TastenTest()
display = qw.QLabel()
snake = Snake()
snake.pause = True

feldbreite = 10
Zoom = 600
chance = 1000000

btn = qw.QPushButton("Neustart")
btn.setEnabled(False)
btn.pressed.connect(snake.restart)

e0 = qw.QLabel("Speed:")        # Geschwindigkeitseinstellungen
e1 = qw.QSpinBox()
e1.setMinimum(1)
e1.setMaximum(8)

e2 = qw.QPushButton("Pause")    # Pause Button
e2.clicked.connect(pauseIt)

e3 = qw.QPushButton("Start")    # Start Button
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
clock = qw.QLabel("Time: ")
snake.addNode()
form = qw.QFormLayout()     # Whole Screen
form2 = qw.QFormLayout()    # Settings Screen


form2.addRow(e6, e7)
form2.addRow(e8, e9)
form2.addRow(e10, e11)
form2.addRow(e0, e1)
form2.addRow(e4, e5)
form2.addRow(e2, e3)
# form2.addRow(HIGHSCORE BUTTON)
form2.addRow(btn, clock)
form.addRow(display, form2)

ex.setLayout(form)
main.setCentralWidget(ex)
menu = main.menuBar()
menu.setNativeMenuBar(False)
m1 = menu.addMenu("Spiel")
m1a = m1.addAction("Neustarten")
m1a.setStatusTip("Startet das Spiel neu")
m1a.triggered.connect(lambda: snake.restart())
m1.addSeparator()
m1b = m1.addAction("Beenden")
m1b.triggered.connect(lambda: main.close())
m1b.setStatusTip("Beendet das Spiel")
stat = main.statusBar()

# Initialize a Qtime object to measure game time
timecounter = qc.QTime()


timer = qc.QTimer()
timer.start(0)
timer.setInterval(100)
timer.timeout.connect(snake.moveIt)
timer.timeout.connect(snake.drawSnake)
timer.timeout.connect(menue)
timer.timeout.connect(lambda: clock.setText(
    # Time is shown in ms by default, so division by 1000 is required
    "Time elapsed since start: {0} s".format(timecounter.elapsed() // 1000)))

sys.exit(app.exec_())
