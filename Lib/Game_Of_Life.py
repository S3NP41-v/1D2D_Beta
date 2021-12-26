from main import IDIID
from msvcrt import getch, kbhit


class GOL:
    def __init__(self, sizeY: int, sizeX: int):
        self.sizeY = sizeY
        self.sizeX = sizeX
        self.DD = IDIID(self.sizeY, self.sizeX)

        self.DD.generateBoard(False)
        self.board = self.DD.board

    def printBoard(self) -> print:
        fg = lambda c: f"\x1b[38;2;{str(c[0])};{str(c[1])};{str(c[2])}m"
        bg = lambda c: f"\x1b[48;2;{str(c[0])};{str(c[1])};{str(c[2])}m"

        level = 0
        for k, v in self.board.items():
            if self.DD.get2D(k)[0] % 2 == 0:
                continue

            if self.DD.get2D(k)[0] > level:
                level = self.DD.get2D(k)[0]
                print('\x1b[0m\n', end='')

            p = '▀'
            color = (fg([255, 255, 255]) if self.board[k - 1] else fg([0, 0, 0])) + (bg([255, 255, 255]) if self.board[k] else bg([0, 0, 0]))



            print("\x1b[0m" + color + p, end='')
        print("\x1b[0m")


gol = GOL(20, 20)
print(gol.board)
gol.board[0] = True
print(gol.board)


gol.printBoard()





