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
        self.won = False
        self.score = 0
        self.player_name = "Jörg"

    def addPoint(self):
        last = self.point[-1]
        newx = last[0] + self.movex
        newy = last[1] + self.movey
        self.point += (newx, newy)

    def reset(self):
        self.x = 1
        self.y = 1
        self.movex = 1
        self.movey = 0
        self.point = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.node = []
        self.loose = False
        self.won = False
        enablebtn()

    def drawSnake(self, ui):
        if not self.loose:
            ui.buttons["restart"].disable()
            #            ui.btn.setEnabled(False)
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
            ui.display.setPixmap(scaledpixmap)
            ui.display.show()
        else:
            timer.stop()
            ui.buttons["restart"].enable()
            if self.won:
                self.wonText()
            else:
                self.lostText()
            bild = qg.QImage(30, 30, qg.QImage.Format_RGB32)
            bild.fill(qc.Qt.white)
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
        "Let snake grow if it eats something and increase score."
        if self.point[0] == self.node[0]:
            self.node = []
            self.grow()
            self.score += 10  # So far it is assumed that all food has the same value

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
        points = self.score  # change!
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
        # self.statusBar().showMessage("Taste mit key−code "+str(e.key())+"
        # gedrückt", 1000)
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


class game_control_button():

    def __init__(self, label, function, xpos, ypos, enabled=True):
        """
        Initialize a button with specified label, function on click and
        position data.

        """
        self.label = label
        self.function = function
        self.x = xpos
        self.y = ypos
        self.btn = qw.QPushButton(label)
        self.btn.clicked.connect(function)
        self.btn.setEnabled(enabled)

    def draw_to(self, Grid):
        "Takes an object of type QGridLayout and adds the widget to it."
        Grid.addWidget(self.btn, self.x, self.y)

    def disable(self):
        """Set enabled attribute to false."""
        self.btn.setEnabled(False)

    def enable(self):
        """Set enabled attribute to True"""
        self.btn.setEnabled(True)


class speed_tuner():

    def __init__(self, xpos, ypos, lowerbound=1, upperbound=8):
        """
        Initialize a speed tuner consisting of a QSpinBox and a Label
        """
        self.e1 = qw.QSpinBox()
        self.e1.setMinimum(lowerbound)
        self.e1.setMaximum(upperbound)
        self.e0 = qw.QLabel("Speed:")
        self.x = xpos
        self.y = ypos

    def draw_to(self, Grid):
        "Takes an object of type QGridLayout and adds the widget to it."
        Grid.addWidget(self.e1, self.x, self.y)
        Grid.addWidget(self.e0, self.x + 1, self.y + 1)

    def get_value(self):
        return self.e1.value()


class display(qw.QLabel):

    def __init__(self, xpos, ypos):
        """

        """
        super().__init__()
        self.x = xpos
        self.y = ypos

    def draw_to(self, Grid):
        Grid.addWidget(self, self.x, self.y)


class bellsandwhistles():

    def __init__(self, snake):
        """

        """

        self.app = qw.QApplication(sys.argv)
        self.ex = TastenTest()
        self.box = qw.QVBoxLayout()
        self.grid = qw.QGridLayout()
        self.buttons = {"pause": game_control_button("Pause", self.pauseIt, 1, 0),
                        "start": game_control_button("Start", self.startIt, 1, 0),
                        "restart":  game_control_button("Neustart", snake.reset, 0, 0, enabled=False)}
        for name, obj in self.buttons.items():
            obj.draw_to(self.grid)
        # Initialize a Qtime object to measure game time
        self.timecounter = qc.QTime()
        # Initialize a widget saying "Time"
        self.clock = qw.QLabel("Time: ")
        # Initialize a widget saying "Score"
        self.score = qw.QLabel("Score: ")
        # Initialize a widget saying "Player"
        self.player = qw.QLabel("Player: ")
        # Initialize a switch to regulate game speed
        self.speedtuner = speed_tuner(1, 1)
        self.speedtuner.draw_to(self.grid)
        self.display = display(0, 4)
        self.display.draw_to(self.grid)
        self.ex.setLayout(self.grid)

        snake.player_name = qw.QInputDialog.getText(self.display,
                                                    "What is your name, Ma'am/Sir?", "", qw.QLineEdit.Normal, "")[0]

    def pauseIt(self):
        snake.pause = True

    def startIt(self):
        """Starts the game
        Starts the timecounter
        """
        for name, button in self.buttons.items():
            button.disable()
            self.timecounter.start()


def menue():
    """Purpose not clear"""
    timer.setInterval(1 / UI.speedtuner.get_value() * 300)


snake = Snake()
UI = bellsandwhistles(snake)

UI.pauseIt()

timer = qc.QTimer()
timer.start(0)
timer.setInterval(100)
timer.timeout.connect(snake.moveIt)
timer.timeout.connect(lambda: snake.drawSnake(UI))
timer.timeout.connect(lambda: UI.score.setText(
    "Current score: " + str(snake.score)))
timer.timeout.connect(lambda: UI.clock.setText(
    # Time is shown in ms by default, so division by 1000 is required
    "Time elapsed since start: {0} s".format(UI.timecounter.elapsed() // 1000)))
timer.timeout.connect(lambda: UI.player.setText(
    "Player: " + snake.player_name))
timer.timeout.connect(menue)

sys.exit(UI.app.exec_())
