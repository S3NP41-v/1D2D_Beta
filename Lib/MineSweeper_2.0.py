from main import IDIID
from random import randint
from msvcrt import getch
import time


class MS2:
    def __init__(self, sizeY: int, sizeX: int):
        self.sizeY = sizeY
        self.sizeX = sizeX

        self.DD = IDIID(sizeY, sizeX)
        self.DD.generateBoard({'mine': False, 'flagged': False})
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


if __name__ == "__main__":
    # sub-menus
        # settings
    global boardSize, mineCount
    boardSize = (9, 9)
    mineCount = 10

    def start(mineCount, boardSize):
        # TODO: play the actual game
        pass

    def settings():
        global boardSize, mineCount
        subCursor = 0
        print("\x1b[0;0H\x1b[J")
        while True:
            print("\x1b[0;0H")
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
            \rGithub Page: https://github.com/S3NP41-v/1D2D_Beta/tree/c68b2fe7fd4284bded0d8bbfb484c2f9c33ed119/Lib
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
            # todo: interact with the selected
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
