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
    boardSize = (9, 9)
    mineCount = 10

    def start(mineCount, boardSize):
        pass

    def settings():
        subCursor = 0
        while True:
            for k, v in enumerate(["[  Board Size  ]", "[  Mine Count  ]", "[  Exit  ]"]):
                if subCursor == k:
                    print(fg([250, 250, 200]) + v + fg([255, 255, 240]))
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
                print("\x1b[0m\x1b[0;0H\x1b[J")
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

                elif subCursor == 3:
                    return

    def about():
        inpt = getch()
        if inpt == b'\x03':
            print("\x1b[0m\x1b[0;0H\x1b[J")
            exit()

        if inpt == b'\x1b':
            return

        print("""
        \rInspired by the minesweeper, created using 1D2D library 
        \rMade by S3NP41#8357, design help by F-32#6164 (discord tags)
        \rGithub Page: https://gist.github.com/S3NP41-v/bbeaa394b957465ea845e7f8878ef678
        """)







        pass



    # Color functions
    fg = lambda c: f"\x1b[38;2;{str(c[0])};{str(c[1])};{str(c[2])}m"
    bg = lambda c: f"\x1b[48;2;{str(c[0])};{str(c[1])};{str(c[2])}m"

    # Main Menu:

    # splash art
    print("\x1b[0;0H\x1b[J")
    print(f"""\r{fg([255, 255, 240])}{bg([0, 0, 0])}\r|  \     /  \|  \                     /      \ |  \                                                    
              \r| $$\   /  $$ \$$ _______    ______  |  $$$$$$\| $$  ______    ______   _______    ______    ______    
              \r| $$$\ /  $$$|  \|       \  /      \ | $$   \$$| $$ /      \  |      \ |       \  /      \  /      \   
              \r| $$$$\  $$$$| $$| $$$$$$$\|  $$$$$$\| $$      | $$|  $$$$$$\  \$$$$$$\| $$$$$$$\|  $$$$$$\|  $$$$$$\  
              \r| $$\$$ $$ $$| $$| $$  | $$| $$    $$| $$   __ | $$| $$    $$ /      $$| $$  | $$| $$    $$| $$   \$$  
              \r| $$ \$$$| $$| $$| $$  | $$| $$$$$$$$| $$__/  \| $$| $$$$$$$$|  $$$$$$$| $$  | $$| $$$$$$$$| $$        
              \r| $$  \$ | $$| $$| $$  | $$ \$$     \ \$$    $$| $$ \$$     \ \$$    $$| $$  | $$ \$$     \| $$        
              \r \$$      \$$ \$$ \$$   \$$  \$$$$$$$  \$$$$$$  \$$  \$$$$$$$  \$$$$$$$ \$$   \$$  \$$$$$$$ \$$        \n\nuse arrow keys to select space to confirm, escape to return""")

    # menu cursor
    # it will keep the option we are selecting
    menuCursor = 0

    # main loop
    while True:
        print("\x1b[12;0H")
        for k, v in enumerate(["[  Start  ]", "[  Settings  ]", "[  About  ]", "[  Exit  ]"]):
            if menuCursor == k:
                print(fg([250, 250, 200]) + v + fg([255, 255, 240]))
            else:
                print(v)

        inpt = getch()

        # input check
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
            pass

        if inpt == b'\x1b':
            # todo: return to previous
            pass
