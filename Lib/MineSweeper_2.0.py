from main import IDIID
from random import randint
from msvcrt import getch
import time


class MS2:
    def __init__(self, sizeY: int, sizeX: int):
        self.sizeY = sizeY
        self.sizeX = sizeX

        self.DD = IDIID(sizeY, sizeX)
        self.DD.generateBoard({'mine': False, 'flagged': False, 'revealed': False})
        self.board = self.DD.board

    def scatterMines(self, mines: int) -> None:
        c = 0
        while c < mines:
            rPos = randint(0, (self.sizeX * self.sizeY) - 1)
            if not self.board[rPos]['mine']:
                c += 1
                self.board[rPos]['mine'] = True

    def surroundingMines(self, n: int) -> list:
        surrounding = list()
        for i in self.DD.getSurrounding(n):
            if self.board[i]['mine']:
                surrounding.append(i)

        return surrounding

    def printBoard(self, cursor: int, xray=False) -> print:
        fg = lambda c: f"\x1b[38;2;{str(c[0])};{str(c[1])};{str(c[2])}m"
        bg = lambda c: f"\x1b[48;2;{str(c[0])};{str(c[1])};{str(c[2])}m"
        colors = [[227, 234, 148], [255, 242, 0], [14, 209, 69], [196, 255, 14], [255, 127, 39], [236, 28, 36],
                  [255, 174, 200], [255, 202, 24], [136, 0, 27]]
        level = 0
        print(f"{fg([200, 200, 150])}{bg([0, 0, 0])}")
        for k, v in self.board.items():
            if self.DD.get2D(k)[0] > level:
                level = self.DD.get2D(k)[0]
                print('\n', end='')

            p = " □"
            if v['flagged']:
                p = fg([50, 50, 200]) + f" ⚐"

            elif v['revealed']:
                c = len(self.surroundingMines(k))
                p = fg(colors[c]) + f" {c}"

            if xray:
                c = len(self.surroundingMines(k))
                p = fg(colors[c]) + f" {c}"
                if self.board[k]["mine"]:
                    p = bg([255, 10, 10]) + p


            print((bg([110, 110, 0]) if cursor == k and not xray else '') + p + "\x1b[0m" + bg([0, 0, 0]), end='')
        print('\n')

    def touchingZeros(self, n: list(), skip=list(), first=True) -> list:
        zeros = list()
        isZero = lambda x: not self.surroundingMines(x)

        if first:
            if isZero(n[0]):
                zeros.append(n[0])
            else:
                return []

        for i in n:
            for i2 in self.DD.getSurrounding(i):
                if i2 in skip:
                    continue

                if isZero(i2):
                    zeros.append(i2)
                    skip.append(i2)

        if zeros:
            return zeros + self.touchingZeros(zeros, skip, first=False)
        else:
            return []

if __name__ == "__main__":
    # sub-menus
        # settings
    global boardSize, mineCount
    boardSize = (9, 9)
    mineCount = 10

    def start(mineCount, boardSize):
        print("\x1b[0;0H\x1b[J")
        ms = MS2(boardSize[0], boardSize[1])

        time_start = time.time()
        ms.scatterMines(mineCount)


        cursor = 0
        # main loop
        while True:
            # printing
            print("\x1b[0;0H")
            print("use arrow keys to move, space to check selected, and 'f' to flag selected")
            ms.printBoard(cursor)


            # input
            inpt = getch()

            # input check
            # Ctlr + C
            if inpt == b"\x03":
                print("\x1b[0m\x1b[0;0H\x1b[J")
                exit()

            if inpt == b'\x1b':
                return

            # special
            if inpt == b'\xe0':
                inpt = getch()

                # Up
                if inpt == b'H':
                    if cursor - ms.sizeX >= 0:
                        cursor -= ms.sizeX

                # Right
                elif inpt == b'M':
                    if cursor + 1 <= (ms.sizeX * ms.sizeY) - 1:
                        cursor += 1

                # Down
                elif inpt == b'P':
                    if cursor + ms.sizeX <= (ms.sizeX * ms.sizeY) - 1:
                        cursor += ms.sizeX

                # Left
                elif inpt == b'K':
                    if cursor - 1 >= 0:
                        cursor -= 1

            # normal keyboard
            if inpt == b' ':
                if not ms.board[cursor]["flagged"] or ms.board[cursor]["revealed"]:
                    if ms.board[cursor]["mine"]:
                        time_end = time.time()
                        print("\x1b[0;0H\x1b[J")
                        ms.printBoard(cursor, xray=True)
                        print(f"\t\t\tGame Over!\n\t\ttime: {str(time_end - time_start)[0:4]}\n\n\t\tPress anything to return to main menu")
                        # just a second delay in case of accidental input
                        time.sleep(1)
                        getch()
                        return

                    if not ms.surroundingMines(cursor):
                        for i in ms.touchingZeros([cursor]):
                            for i2 in ms.DD.getSurrounding(i):
                                ms.board[i2]["revealed"] = True
                    else:
                        ms.board[cursor]["revealed"] = True

                    # checking for win
                    if all(list(map(lambda x: x["revealed"] or x["mine"], ms.board.values()))):
                        # won
                        time_end = time.time()
                        print("\x1b[0;0H\x1b[J")
                        ms.printBoard(cursor, xray=True)
                        print(f"\t\t\tCongratulations!\n\t\ttime: {str(time_end - time_start)[0:4]}\n\n\t\tPress anything to return to main menu")
                        # just a second delay in case of accidental input
                        time.sleep(1)
                        getch()
                        return

            elif inpt == b'f':
                # flag/un-flag position
                if not ms.board[cursor]["revealed"]:
                    ms.board[cursor]["flagged"] = not ms.board[cursor]["flagged"]

    def settings():
        global boardSize, mineCount
        subCursor = 0
        print("\x1b[0;0H\x1b[J")
        while True:
            print("\x1b[J\x1b[0;0H")
            print("Choose settings, inputs have to be inside a specific range\nfor example you cant have more mines than spaces\nor you cant have negative or zero spaces\n")
            for k, v in enumerate(["[  Board Size  ]", "[  Mine Count  ]", "[  Save & Exit ]"]):
                if subCursor == k:
                    print(fg([250, 250, 0]) + v + fg([255, 255, 240]))
                else:
                    print(v)

            inpt = getch()
            # special
            if inpt == b'\xe0':
                inpt = getch()

                # Up
                if inpt == b'H':
                    if subCursor <= 0:
                        subCursor = 2
                    else:
                        subCursor -= 1

                # Right, but i will use it as down
                elif inpt == b'M':
                    if subCursor >= 2:
                        subCursor = 0
                    else:
                        subCursor += 1

                # Down
                elif inpt == b'P':
                    if subCursor >= 2:
                        subCursor = 0
                    else:
                        subCursor += 1

                # Left, but i will use it as up
                elif inpt == b'K':
                    if subCursor <= 0:
                        subCursor = 2
                    else:
                        subCursor -= 1

            if inpt == b'\x03':
                print("\x1b[0m\x1b[0;0H\x1b[J\x1b[?25h")
                exit()

            if inpt == b'\x1b':
                return

            if inpt == b' ':
                if subCursor == 0:
                    while True:
                        try:
                            y = int(input("y: int = "))
                            if y < 1:
                                raise
                        except:
                            print("expected a positive int")
                            pass

                        else:
                            break

                    while True:
                        try:
                            x = int(input("x: int = "))
                            if y < 1:
                                raise
                        except:
                            print("expected a positive int")
                            pass

                        else:
                            break
                    boardSize = (y, x)

                elif subCursor == 1:
                    while True:
                        try:
                            mineCount = int(input("number of mines: int = "))
                            if boardSize[0] * boardSize[1] <= mineCount < 1:
                                raise
                        except:
                            print("expected a positive int, smaller than the number of valid positions on board")
                            pass

                        else:
                            break

                elif subCursor == 2:
                    return

    def about():
        print("\x1b[0;0H\x1b[J")
        while True:
            print("\x1b[0;0H")
            print("""
            \r--Escape to return--
            \r
            \rInspired by the minesweeper, created using 1D2D library and ANSI codes
            \rMade by S3NP41#8357, design help by F-32#6164 (discord tags)
            \rGithub Page: https://github.com/S3NP41-v/1D2D_Beta
            \rANSI codes cheat sheet help: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
            """)

            inpt = getch()
            if inpt == b'\x03':
                print("\x1b[0m\x1b[0;0H\x1b[J\x1b[?25h")
                exit()

            if inpt == b'\x1b':
                return

    # Color functions
    fg = lambda c: f"\x1b[38;2;{str(c[0])};{str(c[1])};{str(c[2])}m"
    bg = lambda c: f"\x1b[48;2;{str(c[0])};{str(c[1])};{str(c[2])}m"

    # Main Menu:

    # menu cursor
    # it will keep the option we are selecting
    menuCursor = 0

    # main loop
    while True:
        print(f"{fg([255, 255, 240])}{bg([0, 0, 0])}")
        print("\x1b[?25l\x1b[0;0H\x1b[J")
        # splash art
        print(f"""\r|  \     /  \|  \                     /      \ |  \                                                    
                  \r| $$\   /  $$ \$$ _______    ______  |  $$$$$$\| $$  ______    ______   _______    ______    ______    
                  \r| $$$\ /  $$$|  \|       \  /      \ | $$   \$$| $$ /      \  |      \ |       \  /      \  /      \   
                  \r| $$$$\  $$$$| $$| $$$$$$$\|  $$$$$$\| $$      | $$|  $$$$$$\  \$$$$$$\| $$$$$$$\|  $$$$$$\|  $$$$$$\  
                  \r| $$\$$ $$ $$| $$| $$  | $$| $$    $$| $$   __ | $$| $$    $$ /      $$| $$  | $$| $$    $$| $$   \$$  
                  \r| $$ \$$$| $$| $$| $$  | $$| $$$$$$$$| $$__/  \| $$| $$$$$$$$|  $$$$$$$| $$  | $$| $$$$$$$$| $$        
                  \r| $$  \$ | $$| $$| $$  | $$ \$$     \ \$$    $$| $$ \$$     \ \$$    $$| $$  | $$ \$$     \| $$        
                  \r \$$      \$$ \$$ \$$   \$$  \$$$$$$$  \$$$$$$  \$$  \$$$$$$$  \$$$$$$$ \$$   \$$  \$$$$$$$ \$$        
                  \r\nuse arrow keys to select, space to confirm, escape to return
                  \rCurrent Settings:: board size: {boardSize}, mine count: {mineCount}\n""")

        print("\x1b[13;0H")
        for k, v in enumerate(["[    Start   ]", "[   Settings ]", "[    About   ]", "[    Exit    ]"]):
            if menuCursor == k:
                print(fg([250, 250, 0]) + v + fg([255, 255, 240]))
            else:
                print(v)

        inpt = getch()

        # input check
        # Ctlr + C
        if inpt == b"\x03":
            print("\x1b[0m\x1b[0;0H\x1b[J")
            exit()

        # special
        if inpt == b'\xe0':
            inpt = getch()

            # Up
            if inpt == b'H':
                if menuCursor <= 0:
                    menuCursor = 3
                else:
                    menuCursor -= 1

            # Right, but i will use it as down
            elif inpt == b'M':
                if menuCursor >= 3:
                    menuCursor = 0
                else:
                    menuCursor += 1

            # Down
            elif inpt == b'P':
                if menuCursor >= 3:
                    menuCursor = 0
                else:
                    menuCursor += 1

            # Left, but i will use it as up
            elif inpt == b'K':
                if menuCursor <= 0:
                    menuCursor = 3
                else:
                    menuCursor -= 1

        if inpt == b' ':
            if menuCursor == 0:
                # start game
                start(mineCount, boardSize)

            elif menuCursor == 1:
                # open setting sub-menu
                settings()

            elif menuCursor == 2:
                # open about sub-menu
                about()

            elif menuCursor == 3:
                # exit cleanly
                print("\x1b[0m\x1b[0;0H\x1b[J\x1b[?25h")
                exit()
