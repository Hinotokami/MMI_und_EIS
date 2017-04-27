# I n i t i a l i s i e r u n g wie ü b l i c h
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


color1 = 0xff50B4D8
color2 = 0xffFFBC46
color3 = 0xffffffff
color4 = 0xff000000


class Snake():

    def __init__(self):
        self.x = 1
        self.y = 1
        self.movex = 1
        self. movey = 0
        self.point = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.node = []
        self.loose = False
        self.count = 0
        self.pause = True

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
        enablebtn()

    def drawSnake(self):
        if not self.loose:
            btn.setEnabled(False)
            bild = qg.QImage(30, 30, qg.QImage.Format_RGB32)
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
            self.addNode()
            self.NodeEat()
            if len(self.node) != 0:
                if self.pause:
                    bild.setPixel(self.node[0][0], self.node[0][1], color4)
                else:
                    bild.setPixel(self.node[0][0], self.node[0][1], color2)
            pixmap = qg.QPixmap.fromImage(bild)
            scaledpixmap = pixmap.scaled(600, 600, qc.Qt.KeepAspectRatio)
            display.setPixmap(scaledpixmap)
            display.show()
        else:
            btn.setEnabled(True)
            bild = qg.QImage(30, 30, qg.QImage.Format_RGB32)
            bild.fill(qc.Qt.white)
            display.setText("Verloren")
            pixmap = qg.QPixmap.fromImage(bild)
            scaledpixmap = pixmap.scaled(600, 600, qc.Qt.KeepAspectRatio)
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
            if x > 29:
                x = 0
            if x < 0:
                x = 29
            if y < 0:
                y = 29
            if y > 29:
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
            x = random.randint(0, 29)
            y = random.randint(0, 29)
            self.node = [(x, y)]

    def NodeEat(self):
        if self.point[0] == self.node[0]:
            self.node = []
            self.grow()

    def lose(self):
        for i in self.point[1:]:
            if self.point[0] == i:
                self.loose = True
                self.pause = True


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

app = qw.QApplication(sys.argv)
box = qw.QVBoxLayout()
grid = qw.QGridLayout()
ex = TastenTest()
display = qw.QLabel()
snake = Snake()
snake.pause = True
btn = qw.QPushButton("Neustart")
btn.setEnabled(False)
btn.pressed.connect(snake.restart)


def menue():
    timer.setInterval(1 / e1.value() * 300)


def enablebtn():
    e2.setEnabled(True)
    e3.setEnabled(True)


def pauseIt():
    snake.pause = True


def startIt():
    snake.pause = False
    e1.setEnabled(False)
    e2.setEnabled(False)
    e3.setEnabled(False)
    enablebtn()

e1 = qw.QSpinBox()
e1.setMinimum(1)
e1.setMaximum(8)

e0 = qw.QLabel("Speed:")

e2 = qw.QPushButton("Pause")
e2.clicked.connect(pauseIt)

e3 = qw.QPushButton("Start")
e3.clicked.connect(startIt)


grid.addWidget(e2, 1, 0)
grid.addWidget(e3, 1, 1)
grid.addWidget(e0, 0, 0)
grid.addWidget(e1, 0, 1)
grid.addWidget(btn, 1, 4)
grid.addWidget(display, 0, 4)
ex.setLayout(grid)
ex.setLayout(grid)
timer = qc.QTimer()
timer.start(0)
timer.setInterval(100)
timer.timeout.connect(snake.moveIt)
timer.timeout.connect(snake.drawSnake)
timer.timeout.connect(menue)

sys.exit(app.exec_())
