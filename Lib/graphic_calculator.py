import math
from main import IDIID
# 1D2D Library ^

# Driver code V
if __name__ == "__main__":
    # Color functions
    fg = lambda c: f"\x1b[38;2;{str(c[0])};{str(c[1])};{str(c[2])}m"
    bg = lambda c: f"\x1b[48;2;{str(c[0])};{str(c[1])};{str(c[2])}m"

    # Getting grid size
    y, x = input("Grid size ('y.x'): ").split('.')
    DD = IDIID(int(y), int(x))

    # Generating board with default value of 'False'
    DD.generateBoard(False)

    # getting function
    fun = input("f(x) = ")
    fun = eval(f"lambda x: {fun}")

    # applying function
    values = list()
    valuesRaw = list()
    for x in range(-(DD.sizeX // 2), (DD.sizeX // 2 + 1)):
        try:
            y = round((DD.sizeY // 2) - fun(x))
            yRaw = (DD.sizeY // 2) - fun(x)
        except ZeroDivisionError:  # if we get a 'division by zero', try a little different x, otherwise just throw a normal error
            y = round((DD.sizeY // 2) - fun(x-0.1))
            yRaw = (DD.sizeY // 2) - fun(x-0.1)

        values.append((DD.sizeY // 2) - y)
        valuesRaw.append((DD.sizeY // 2) - yRaw)

        boardPoint = DD.get1D((y, (DD.sizeX // 2) + x))
        if boardPoint in DD.board:
            DD.board[boardPoint] = True

    # printing
    level = 0
    for k, v in DD.board.items():
        if DD.get2D(k)[0] > level:
            level = DD.get2D(k)[0]
            print('\n', end='')

        # default pixel, just some spaces
        p = "  "

        # point
        if v:
            p = fg([255, 0, 0]) + " ■"

        # vertical line
        if DD.get2D(k)[0] == (DD.sizeY // 2) and DD.get2D(k)[1] != (DD.sizeX // 2):
            p = (fg([255, 0, 0]) if v else fg([200, 200, 200])) + "──"

        # horizontal line
        if DD.get2D(k)[1] == (DD.sizeX // 2) and DD.get2D(k)[0] != (DD.sizeY // 2):
            p = (fg([255, 0, 0]) if v else fg([200, 200, 200])) + " │"

        # point '0'
        if DD.get2D(k)[0] == (DD.sizeY // 2) and DD.get2D(k)[1] == (DD.sizeX // 2):
            p = '─' + (fg([255, 0, 0]) if v else fg([200, 200, 200])) + "┼"

        print(bg([43, 43, 43]) + p + "\x1b[0m", end='')

    # end
    print("\x1b[0m" + '\n' + f"values = {values}\n\nraw    = {valuesRaw}")
