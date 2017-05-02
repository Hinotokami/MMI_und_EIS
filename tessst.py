import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

class MainWindow(qw.QMainWindow):
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
            if snake.pause:
                startIt()
            else:
                pauseIt()

color1 = 0xff50B4D8  # blue for snake
color2 = 0xffFFBC46  # orange for food
color3 = 0xffffffff  # white (pause mode)
color4 = 0xff000000  # black (pause mode)
color5 = 0xff2680A1  # dark blue for eaten food
color6 = 0xff2E2E2E  # dark grey (pause mode)

class Snake():
    def __init__(self):
        self.x = 1
        self.y = 1
        self.movex = 1
        self.movey = 0
        self.speedsquare = self.movex**2 + self.movey**2
        self.point = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.eatennode = []
        self.node = []
        self.loose = False
        self.count = 0
        self.pause = True
        self.won = False
        self.eaten = False
        self.borders = False
        self.seconds = 0
        self.steps = 0
        self.foodTime = 0
        self.foodCount = 0
        self.points = 0
        self.speedmodifier = 1
        self.brakerate = 0
        self.speedlimit = 1
        self.interval = 100
        self.i = 0

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
        self.eatennode = []
        self.eaten = False
        self.foodTime = 0
        self.foodCount = 0
        self.points = 0
        self.interval = 100
        self.steps = 0
        self.i = 0
        timer.start()
        secs.start()
        enableAll()

    def drawSnake(self):
        import random

        if not self.loose:
            self.deleatennode()
            btn.setEnabled(False)
            bild = qg.QImage(field_dim, field_dim, qg.QImage.Format_RGB32)
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
                if self.pause:
                    bild.setPixel(self.eatennode[0], self.eatennode[1], color6)
                else:
                    bild.setPixel(self.eatennode[0], self.eatennode[1], color5)
            z = random.randint(0, 10000000)
            if z < chance*self.steps:
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
            secs.stop()
            btn.setEnabled(True)
            if self.won:
                self.wonText()
            else:
                self.lostText()
            self.showText()
            bild = qg.QImage(field_dim, field_dim, qg.QImage.Format_RGB32)
            bild.fill(qc.Qt.white)
            pixmap = qg.QPixmap.fromImage(bild)
            scaledpixmap = pixmap.scaled(Zoom, Zoom, qc.Qt.KeepAspectRatio)
            display.setPixmap(scaledpixmap)
            main.show()

    def addSpeed(self, x, y):
        if self.isvalidmove(x, y):
            self.movex = x
            self.movey = y
        else:
            pass

    def countSecs(self):
        self.seconds += 1

    def isvalidmove(self, x, y):
        if self.movex == x:
            return False
        elif self.movey == y:
            return False
        else:
            return True

    def moveIt(self):
        if not self.pause:
            self.steps += 1
            self.lose()
            x = self.point[0][0] + self.movex
            y = self.point[0][1] + self.movey
            if x > field_dim - 1:
                if self.borders:
                    self.loose = True
                    self.pause = True
                x = 0
            if x < 0:
                if self.borders:
                    self.loose = True
                    self.pause = True
                x = field_dim - 1
            if y < 0:
                if self.borders:
                    self.loose = True
                    self.pause = True
                y = field_dim - 1
            if y > field_dim - 1:
                if self.borders:
                    self.loose = True
                    self.pause = True
                y = 0
            self.point.insert(0, (x, y))
            if not self.eaten:
                self.point.__delitem__(-1)
        else:
            pass

    def speedup(self):
        self.i += 1
        self.interval += 100*((0.5)**self.i)*(self.speedlimit-speedB.value()/2)
        timer.setInterval(self.interval)
        timer.setInterval(self.interval)

    def grow(self):
        self.eaten = True
        self.moveIt()
        self.steps = 0
        self.eaten = False
        amount = self.seconds - self.foodTime
        maxPoints = 100
        self.points += maxPoints
        if amount > 5:
            subs = self.functional(amount)
            self.points -= subs
        self.foodCount += 1
        if self.foodCount == 5:
            self.foodCount = 0
            self.speedup()

    def functional(self, x):
        import math
        y = 3 - (x / 3)
        f = math.exp(y)
        f += 1
        z = 99 / f
        z += 1
        done = int(z)
        return done

    def addNode(self):
        import random
        if len(self.node) == 0:
            x = random.randint(0, field_dim - 1)
            y = random.randint(0, field_dim - 1)
            if not ((x, y) in self.point):
                self.node = [(x, y)]
                self.foodTime = self.seconds

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
        if len(self.point) == 900:
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
                    position = i + 1
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
            message = "%s you made the Highscore at %d. place! Wanna see?" % (
                inStr, position)
        else:
            if self.won:
                inStr = "But"
            else:
                inStr = "And"
            message = "%s didn't make the Highscore... still wanna see?" % inStr

        showMess = qw.QMessageBox.question(display, self.title, message, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                           qw.QMessageBox.Yes)
        if showMess == qw.QMessageBox.Yes:
            highsc = qw.QMessageBox.question(
                display, "Highscores", show, qw.QMessageBox.Ok, qw.QMessageBox.Ok)


def menue():
    global chance, player_name, field_dim, Zoom
    timer.setInterval(1 / speedB.value() * 300)
    chance = foodB.value() * 10000
    player_name = nameB.text()
    field_dim = fieldB.value()
    Zoom = (2 + zoomB.value()) * 200
    snake.borders = checkBox.isChecked()
    snake.speedlimit = maxSpeed.value()

def enablebtn():
    pauseB.setEnabled(True)
    startB.setEnabled(True)

def enableAll():
    speedB.setEnabled(True)
    pauseB.setEnabled(True)
    startB.setEnabled(True)
    foodL.setEnabled(True)
    foodB.setEnabled(True)
    nameL.setEnabled(True)
    nameB.setEnabled(True)
    fieldL.setEnabled(True)
    fieldB.setEnabled(True)
    zoomL.setEnabled(True)
    zoomB.setEnabled(True)
    checkBox.setEnabled(True)
    maxSpeed.setEnabled(True)

def pauseIt():
    snake.pause = True

def startIt():
    snake.pause = False
    speedB.setEnabled(False)
    pauseB.setEnabled(False)
    startB.setEnabled(False)
    foodL.setEnabled(False)
    foodB.setEnabled(False)
    nameB.setEnabled(False)
    fieldB.setEnabled(False)
    zoomB.setEnabled(False)
    checkBox.setEnabled(False)
    maxSpeed.setEnabled(False)
    
    secs.start()
    enablebtn()

def currscore():
    if snake.pause == False:
        scor.setText("Points: {}".format(snake.points))
        playername.setText("Player: {}".format(nameB.text()))

def formate():
    mainform = qw.QWidget()
    form = qw.QWidget()
    form2 = qw.QWidget()
    form4 = qw.QGridLayout()
    form3 = qw.QGridLayout()

    form3.addWidget(nameL, 0, 0)
    form3.addWidget(nameB, 0, 1)
    form3.addWidget(speedL)
    form3.addWidget(speedB)
    form3.addWidget(maxSpeedL)
    form3.addWidget(maxSpeed)
    form3.addWidget(foodL)
    form3.addWidget(foodB)
    form3.addWidget(fieldL)
    form3.addWidget(fieldB)
    form3.addWidget(zoomL)
    form3.addWidget(zoomB)
    form3.addWidget(checkLabel)
    form3.addWidget(checkBox)
    form3.addWidget(pauseB)
    form3.addWidget(startB)
    form3.addWidget(btn)
    
    form4.addWidget(display)
    form.setLayout(form3)
    form2.setLayout(form4)
    form5 = qw.QGridLayout()
    form5.addWidget(form2, 0, 0)
    form5.addWidget(form, 0, 1)
    mainform.setLayout(form5)
    main.setCentralWidget(mainform)

app = qw.QApplication(sys.argv)

main = MainWindow()
main.setWindowTitle("Sssssnake")
main.resize(800, 600)

display = qw.QLabel()
snake = Snake()
snake.pause = True
field_dim = 10
Zoom = 600
chance = 100000
snake.addNode()

btn = qw.QPushButton("Restart")
btn.setEnabled(False)
btn.pressed.connect(snake.restart)

speedL = qw.QLabel("Speed:")
speedB = qw.QSpinBox()
speedB.setMinimum(1)
speedB.setMaximum(8)

pauseB = qw.QPushButton("Pause")
pauseB.clicked.connect(pauseIt)

startB = qw.QPushButton("Start")
startB.clicked.connect(startIt)

foodL = qw.QLabel("Food probability in %:")
foodB = qw.QSpinBox()
foodB.setMinimum(0)
foodB.setValue(50)
foodB.setMaximum(100)

nameL = qw.QLabel("Player name")
nameB = qw.QLineEdit()

fieldL = qw.QLabel("Field dimensions")
fieldB = qw.QSpinBox()
fieldB.setMinimum(10)
fieldB.setMaximum(30)

zoomL = qw.QLabel("Zoom")
zoomB = qw.QSpinBox()
zoomB.setMinimum(1)
zoomB.setMaximum(3)

checkLabel = qw.QLabel("Borders on")
checkBox = qw.QCheckBox()

maxSpeedL = qw.QLabel("Max. speed")
maxSpeed = qw.QSpinBox()
maxSpeed.setMinimum(1)
maxSpeed.setMaximum(8)

def setMax():
    maxSpeed.setMinimum(speedB.value())

def displayHelp():
    helpText = qw.QMessageBox()
    helpText.setWindowTitle("Help! For you! Now!")
    helpText.setText("We have the following key function:\n\tArrow keys for movement\n\tSpace for (un)pause")
    helpText.setStandardButtons(qw.QMessageBox.Ok)
    helpText.setDefaultButton(qw.QMessageBox.Ok)
    helpText.exec_();

formate()
speedB.valueChanged.connect(setMax)

menu = main.menuBar()
menu.setNativeMenuBar(False)
m1 = menu.addMenu("Game")
helper = m1.addAction("Help")
helper.setStatusTip("If you need any help")
helper.triggered.connect(displayHelp)
m1a = m1.addAction("Restart")
m1a.setStatusTip("Restarts the game")
m1a.triggered.connect(snake.restart)
m1.addSeparator()
m1b = m1.addAction("Quit")
m1b.triggered.connect(main.close)
m1b.setStatusTip("Quits the game")
stat = main.statusBar()

playername = qw.QLabel()
stat.addPermanentWidget(playername)
scor = qw.QLabel("Points: {}".format(snake.points))
stat.addPermanentWidget(scor)

timer = qc.QTimer()
timer.start(0)
timer.setInterval(100)
timer.timeout.connect(snake.moveIt)
timer.timeout.connect(snake.drawSnake)
timer.timeout.connect(menue)
timer.timeout.connect(currscore)

secs = qc.QTimer()
secs.setInterval(1000)
secs.timeout.connect(snake.countSecs)

sys.exit(app.exec_())
