# all over todo: makeMenu, makeToolBar: buttons, values, layout/interface
#				lost/won: message output, file manipulation
#				moveGame: finishes (try-outs)

import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import GtCore as qc
from random import randint


class Field():
    # field is initialized as background
    # rgb codes to color value

    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.isBack()

    def isBack(self):
        self.kind = 0
        self.color = qg.qRgb(0, 0, 0)
        self.colorGray = qg.qRgb(0, 0, 0)

    def isSnake(self):
        self.kind = 1
        self.color = qg.qRgb(80, 180, 216)
        self.colorGray = qg.qRgb(216, 216, 216)

    def isEaten(self):
        self.kind = 2
        self.color = qg.qRgb(45, 144, 181)
        self.colorGray = qg.qRgb(169, 169, 169)

    def isFood(self):
        self.kind = 3
        self.color = qg.qRgb(255, 188, 70)
        self.colorGray = qg.qRgb(242, 242, 242)


class FrameW(qw.QWidget):

    def start():
        app = qw.QApplication(sys.argv)
        FrameW()  # own constructor
        sys.exit(app.exec_())

    def __init__(self):
        super().__init__()
        self.buildWindow()

    def buildWindow(self):
        # standard values
        self.resetValues()

        self.main = qw.QMainWindow()
        self.main.resize(self.windowWidth, self.windowHeight)
        self.main.setWindowTitle("Snake")
        self.mainWindow = qw.QWidget()
        self.mainWindow.resize(self.windowWidth, self.windowHeight)
        self.main.setCentralWidget(self.mainWindow)

        # make the framework
        self.makePicture()
        self.makeMenu()
        self.makeToolBar()

        # sets all key events in action
        self.main.keyPressEvent = self.fn

        # when done, show it
        self.main.show()

    def fn(self, e):
        # won't react if the game is finished
        if(self.isGame == 0):
            return 0
        # pausing/restarting game
        if(e.key() == qc.Qt.Key_Space):
            if(self.on == 0):
                self.startGame()
            else:
                self.pauseGame()
        elif self.on == 0:
            return 0
        # changing directon
        if e.key() == qc.Qt.Key_Left:
            self.direction = 0
        elif e.key() == qc.Qt.Key_Right:
            self.direction = 1
        elif e.key() == qc.Qt.Key_Up:
            self.direction = 2
        elif e.key() == qc.Qt.Key_Down:
            self.direction = 3

    def doTimers(self):
        # updates picture, updates game
        self.timer = qw.QTimer()
        self.timer.timeout.connect(self.updatePicture())
        self.gameTimer = qw.QTimer()
        self.gameTimer.timeout.connect(self.moveGame())
        self.realTime = qw.QTimer()
        self.realTime.timeout.connect(self.countTime())

    def makePicture(self):
        # put picture as pixmap in picture frame label
        self.picture = qg.QImage(
            self.pictureWidth, self.pictureHeight, qg.QImage.Format_RGB32)
        self.picL = qw.QLabel(self.mainWindow)
        self.picL.resize(self.pictureWidth, self.pictureHeight)

    def makeMenu(self):  # not done: buttons and positions
        # rudimentary assignment of labels for menu
        # reading input from user, changes window accordingly, error message for boundaries
        # todo: read values, position buttons, etc
        # resize main Window
        # self.countTime() = speedFactor*1000
        fieldMin = 10
        fieldMax = 30
        zoomMin = 2
        zoomMax = 5
        speedMin = 1
        speedMax = 5
        speedUpMin = 1
        speedUpMax = 5
        foodMin = 10
        foodMax = 80

        self.menuL = qw.QLabel(self.mainWindow)
        self.menuL.resize(self.menuWidth, self.menuHeight)
        self.frameIn = qw.QLabel(self.menuL)  # frame or no frame

        self.playerName = qg.QLineEdit(self.menuL)
        self.playerName.setPlaceholderText(self.player)

        size, ok = qg.QInputDialog.getInt(
            self, 'field', 'width', value=self.pictureWidth / self.zoom, min=fieldMin, max=fieldMax, step=1)
        if ok:
            self.pictureWidth = size * self.zoom
        size, ok = qg.QInputDialog.getInt(
            self, 'field', 'height', value=self.pictureHeight / self.zoom, min=fieldMin, max=fieldMax, step=1)
        if ok:
            self.pictureHeight = size * self.zoom
        size, ok = qg.QInputDialog.getInt(
            self, 'field', 'zoom', value=self.zoom, min=zoomMin, max=zoomMax, step=1)  # pixel per field element
        if ok:
            self.zoom = size
        size, ok = qg.QInputDialog.getInt(
            self, 'snake', 'speed', value=self.speed, min=speedMin, max=speedMax, step=1)  # start speed
        if ok:
            self.speed = size
        size, ok = qg.QInputDialog.getInt(self, 'snake', 'speed', value=self.speedUp,
                                          min=speedUpMin, max=speedUpMax, step=1)  # per food eaten/amount before speedup
        if ok:
            self.speedUp = size
        size, ok = qg.QInputDialog.getInt(
            self, 'snake', 'food', value=self.food, min=foodMin, max=foodMax, step=1)  # food probability in percent
        if ok:
            self.food = size

        self.frameOn = qg.QCheckBox(self.frameIn)
        self.frameOff = qg.QCheckBox(self.frameIn)
        if(self.borders == 0):
            self.frameOn.setChecked(False)
            self.frameOff.setChecked(True)
        else:
            self.frameOn.setChecked(True)
            self.frameOff.setChecked(False)
        self.frameOn.stateChanged.connect(self.changeBorders)

        self.reset = qg.QPushButton(self.menuL)  # resets to standard values
        self.reset.clicked.connect(self.resetValues)
        self.oK = qg.QPushButton(self.menuL)  # read values, change stuff
        self.ok.clicked.connect(self.makeGame)
        self.highScore = qg.QPushButton(self.menuL)  # shows highscore list
        self.highScore.clicked.connect(self.showHighScores)

    def makeToolBar(self):  # not done: display
        # menu bar: shows current points and game time, if game is running, etc.
        # does it update by itself?
        self.toolL = qw.QLabel(self.mainWindow)
        self.start = qg.PushButton(self.toolL)
        self.stop = qg.PushButton(self.toolL)
        self.start.clicked.connect(startGame)
        self.stop.clicked.connect(terminateGame)
        self.pointsL = qw.QLabel(self.toolL)
        self.pointsL.setText(self.points)
        self.timeL = qw.QLabel(self.toolL)
        self.timeL.setText(self.sec)
        self.onL = qw.QLabel(self.toolL)
        if(self.on == 0):
            self.onL.setText("paused...")
        else:
            self.onL.setText("running")

    def countTime(self):
        # game Time; could be done via self.timer -> add 0.1?
        self.sec += 1

    def updatePicture(self):
        self.setFields()
        for i in range(0, pictureWidth):
            for j in range(0, pictureHeight):
                # check in which field the pixel is, color accordingly
                posX = i % self.zoom
                posY = j % self.zoom
                if(self.on == 0):
                    cC = self.fields[posX][posY].colorGray
                else:
                    cC = self.fields[posX][posY].color
                self.picture.setPixel(i, j, cC)

        # has to be done every time
        self.picMap = qg.QPixmap(qg.QPixmap.fromImage(self.picture))
        self.picMap.scaled(picL.size(), Qt.KeepAspectRatio)
        self.picL.setPixmap(picMap)

    def setFields(self):
        # assign colors to fields depending on attributes
        for i in self.backGround:
            i.isBack()
        for i in self.snake:
            i.isSnake()
        for i in self.eaten:
            i.isEaten()
        self.food = isFood()

    def makeGame(self):
        # fields are saved in array (index from position in picture)
        self.fields = []
        self.backGround = []
        for i in range(0, self.fieldWidth):
            temp = []
            for j in range(0, self.fieldHeight):
                field = Field(i, j)
                field.kind = 0
                temp.append(field)
            self.fields.append(temp)
            self.backGround.append(temp)

        # initial snake is four fields long and sits about in the middle
        self.snake = []
        initX = (self.fieldWidth / 2) - 2
        initY = self.fieldHeight / 2
        temp = self.fields[initX][initY]
        self.snake.append(temp)
        temp = self.fields[initX + 1][initY]
        self.snake.append(temp)
        temp = self.fields[initX + 2][initY]
        self.snake.append(temp)
        temp = self.fields[initX + 3][initY]
        self.snake.append(temp)
        self.update()

        # no food eaten at the start
        self.eaten = []
        temp = []
        self.eaten.append(temp)

        # no food available at the start
        self.food = null

        # game points, timer, pause
        self.points = 0
        self.sec = 0
        self.on = 0
        self.isGame = 0
        self.foodCount = 0

        # initialize timers
        self.doTimers()
        self.startGame()

    def startGame(self):
        # starts all game processes needed
        self.timer.start(100)
        self.gameTimer.start(self.speed)
        self.realTime.start(1000)
        self.on = 1
        self.isGame = 1
        self.won = 0

    def pauseGame(self):
        self.timer.stop()
        self.gameTimer.stop()
        self.realTime.stop()
        self.on = 0
        self.updatePicture()

    def terminateGame(self):
        # stops all game processes, game over / won -> depends on this.won
        self.pauseGame()
        self.isGame = 0  # access to menu etc. by this variable
        if self.won == 0:
            self.lost()
        else:
            self.won()

    def lost(self):  # not done: display message for lost game -> close window / play again
        lostMess = qg.QMessageBox()
        lostMess.setTitle("You have lost the game")
        lostMess.setText("Sorry! You have lost")
        # ok button
        # play again button -> make game
        lostMess.setStandardButton(QMessageBox.Ok)
        lostMess.exec_()

    def won(self):  # not done: file manpipulation
        # string.split() -> split by spaces
        # highscore file: "points player"
        # display 'message' in dialogBox with OK button and Show Highscore
        # option -> show stuff (should still be saved)
        path = 'highscores.txt'  # read current highscores of form: "Place. points by player"
        position = 0
        with open(path, 'r') as data:
            scores = data.readLines()
        if scores.size() == 0:
            rank = {1}
            playerPoints = {self.points}
            playerNames = {self.player}
        else:
                # string split? get the points and names -> playerPoints[] ->
                # playerNames[]
            if rank.size() < 10:  # no competition
                rank.append(positions.size())
            else:  # pop last entry of position only when entry is 11, else, keep all -> combine independant of size of current ranks
                check = playerPoints[0]
                i = 0
            while self.points < check:
                i += 1
                check = playerPoints[i]
                position = i + 1
                playerPoints.insert(i, self.points)
                playerNames.insert(i, self.player)
                playerPoints.pop(playerPoints.size())
                playerNames.pop(playerNames.size())
                # wipe data
                for i in range(0, rank.size()):
                    string = "%d. %dp by %s" % (
                        rank[i], playerPoints[i], playerNames[i])
            # print string to data
        # save and close data
        wonMess = qg.QMessageBox()
        wonMess.setTitle("You have won the game!")
        wonMess.setText(message)
        QPushButton * highButton
        if position == 11:
            message = "Sorry! You didn't make the top ten."
        else:
            message = "Congrats! You made the top ten at rank %d!" % position
            highButton = wonMess.addButton(
                tr("View Highscores"), QMessageBox.ActionRole)
        QPushButton * okButton = wonMess.addButton(QMessageBox.Ok)
        wonMess.exec_()
        if wonMess.clickedButton() == highButton:
            showHighScores()

    def showHighScores(self):  # not done: do stuff

    def changeBorders(self):
        if self.borders == 0:
            self.borders = 1
        else:
            self.borders = 0

    def resetValues(self):  # not done
        self.player = "Username"
        self.zoom = 2
        self.speed = 2
        self.speedUp = 2
        self.borders = 0
        self.food = 20
        self.windowWidth = 600
        self.windowHeight = 300
        self.pictureWidth = 300
        self.pictureHeight = 300
        self.menuWidth = 300
        self.menuHeight = 300

    def moveGame(self):  # not done: questions, optimization; have to try out!!
        # I guess we start with (0,0) as the bottom left corner; if not, values will have to be altered
        # borders on, meets: terminates game; optional: bounce? clockwise or
        # counterclockwise? what else?
        if(self.backGround.size() == 0):
            self.won = 1
            self.terminateGame()
            return 0
        self.foodCount += 1
        head = self.snake[0]
        nextX = head.x
        nextY = head.y

        # optimize; mod fieldWidth/Height?
        if(self.direction == 0):  # left
            if(head.x != 0):
                nextX -= 1
            else if(self.borders == 0):
                nextX = self.fieldWidth - 1
            else:
                self.terminateGame()
                return 0
        else if(self.direction == 1):  # right
            if(head.x != self.fieldWidth - 1):
                nextX += 1
            else if(self.borders == 0):
                nextX = 0
            else:
                self.terminateGame()
                return 0
        else if(self.direction == 2):  # up
            if(head.y != 0):
                nextY -= 1
            else if(self.borders == 0):
                nextY = self.fieldHeight - 1
            else:
                self.terminateGame()
                return 0
        else if(self.direction == 3):  # down
            if(head.y != self.fieldHeight - 1):
                nextY += 1
            else if(self.borders == 0):
                nextY = 0
            else:
                self.terminateGame()
                return 0

        # part of snake: bad
        nextHead = fields[nextX][nextY]
        if(nextHead.kind == 1 or nextHead.kind == 2):
            self.terminateGame()
            return 0

        # add field to snake, remove from background
        i = self.snake.size()
        saved = self.snake[i - 1]
        self.snake.append(saved)
        while i > 1:
            i -= 1
            self.snake[i] = self.snake[i - 1]
        self.snake[0] = nextHead
        self.backGround.remove(nextHead)
        if(self.snake[0].kind == 3):
            self.eaten.append(self.snake[0])
            food = null
        else:  # adjust arrays
            if(self.snake[i].kind == 2):
                for i in range(0, self.eaten.size()):
                    self.eaten[i] = self.eaten[i + 1]
                self.eaten.pop(self.eaten.size() - 1)
            self.backGround.append[self.snake[i]]
            self.snake.pop(i)

        # propability for food to appear, random position that must be
        # background
        foodValue = randint(0, 100)
        foodValue /= self.foodCount
        foodValue *= self.speed
        if(foodValue < self.food):
            self.foodCount = 0
            setR = False
            while !setR:
                randX = randint(0, self.fieldWidth)
                randY = randint(0, self.fieldWidth)
                if(fields[randX][randY].kind == 0):
                    setR = true

        food = fields[randX][randY]

    def update(self):
        # makes sure everything is aligned properly
        for i in self.backGround:
            i.isBack()
        for i in self.snake:
            i.isSnake()
        for i in self.eaten:
            i.isEaten()
        self.food.isFood()

if __name__ == '__main__':
    FrameW.start()
