import curses

KEY_ENTER = 10

class ClassWin:
    def __init__(self):
        self.createWin()
    def refresh(self):
        self.win.refresh()
    def focus(self):
        self.isFocus = True
    def defocus(self):
        self.isFocus = False
    def getFocus(self):
        return self.isFocus

class MainWin(ClassWin):
    def __init__(self):
        self.win = stdscr
        self.content = ContentWin()
        self.guide = GuideWin()
        self.menuBar = MenuBar()
        self.drawMenu()

    def startMainLoop(self):
        self.inEventLoop = True
        while self.inEventLoop:
            c = stdscr.getch()
            self.inputParser(c)

    def drawMenu(self):
        self.focus()
        begin_x = 0
        begin_y = 0
        width = stdscr.getmaxyx()[1]
        height = 3
        menubar = curses.newwin(height, width, begin_y, begin_x)
        menubar.border()
        menubar.move(1,1)
        for i,w in enumerate(self.menuBar.items):
            if i==self.menuBar.index:
                menubar.addstr(w,curses.A_STANDOUT)
                self.guide.update(self.menuBar.getCurrentItemGuide())
            else:
                menubar.addstr(w)
            menubar.addstr(" | ")
        menubar.addstr(1,menubar.getmaxyx()[1]-10,"|")
        if self.menuBar.index == len(self.menuBar.items):
            menubar.addstr(1,menubar.getmaxyx()[1]-9," [Q]uit ", curses.A_STANDOUT)
            self.guide.update("Quit KeeTerm")
        else:
            menubar.addstr(1,menubar.getmaxyx()[1]-9," [Q]uit ")
        menubar.refresh()

    def inputParser(self, c):
        if self.isFocus:
            if c==KEY_ENTER:
                self.executeParser(self.menuBar.index)
            elif c==curses.KEY_RIGHT:
                self.menuBar.moveIndexRight()
                self.drawMenu()
            elif c==curses.KEY_LEFT:
                self.menuBar.moveIndexLeft()
                self.drawMenu()
            elif c==ord("q"):
                self.inEventLoop = False
            else:
                self.menuBar.keyBoardInput(c)

    def executeParser(self,index):
        if index==len(self.menuBar.items):
            self.inEventLoop = False
        else:
            self.menuBar.cursorInput(index)

class MenuBar:
    def __init__(self):
        self.useFileMenu()
        self.index = 0
    def setIndex(self,index):
        self.index = index
    def moveIndexRight(self):
        self.index = self.index+1
        if self.index > len(self.items):
            self.index = 0
    def moveIndexLeft(self):
        self.index = self.index-1
        if self.index < 0:
            self.index = len(self.items)
    def getCurrentItemGuide(self):
        return self.itemGuides[self.index]
    def useFileMenu(self):
        self.items = ["[O]pen","[S]ave","[C]lose","[N]ew"]
        self.itemGuides = ["Open a KeePass database",
                           "Save the current KeePass database",
                           "Close the current KeePass database",
                           "Create a new KeePass database"]
    def cursorInput(self, index):
        stdscr.addstr(10,0,str(index))
    def keyBoardInput(self, c):
        stdscr.addstr(10,0,str(c))

class GuideWin(ClassWin):
    def createWin(self):
        begin_x = 0
        begin_y = stdscr.getmaxyx()[0]-5
        width = stdscr.getmaxyx()[1]
        height = 5
        self.win = curses.newwin(height, width, begin_y, begin_x)
        self.win.border()
        self.win.refresh()
        self.usableWidth = width-2
        self.usableHeight = height-2
    def update(self,text):
        self.win.clear()
        self.win.border()
        line1 = text[:self.usableWidth]
        self.win.move(1,1)
        self.win.addstr(line1)
        self.refresh()

class ContentWin(ClassWin):
    def __init__(self):
        begin_x = 0
        begin_y = 3
        width = stdscr.getmaxyx()[1]
        height = stdscr.getmaxyx()[0]-8
        self.win = curses.newwin(height, width, begin_y, begin_x)
        self.win.refresh()

def main(stdscr):
    mainWin = MainWin()
    mainWin.startMainLoop()

stdscr = curses.initscr()
curses.wrapper(main)
