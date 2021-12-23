

class IDIID:
    def __init__(self, sizeY: int, sizeX: int):
        """
        :param sizeY: height
        :param sizeX: width
        """
        self.board = dict()
        self.sizeY = sizeY
        self.sizeX = sizeX

    def generateBoard(self, defaultObject) -> None:
        """
        :param defaultObject: default object given to all positions
        :return: None
        """
        assert self.sizeX * self.sizeY > 0, "sizeY * sizeX has to be more than 0"

        if type(defaultObject) in [list, dict, set]:
            self.board = {i: defaultObject.copy() for i in range(self.sizeY * self.sizeX)}
        else:
            self.board = {i: defaultObject for i in range(self.sizeY * self.sizeX)}

    def get2D(self, pos: int) -> tuple:
        """
        :param pos: a 1D coordinate
        :return: a 2D coordinate
        """
        y = pos // self.sizeX
        x = pos - (y * self.sizeX)
        return y, x

    def get1D(self, pos: tuple) -> int:
        """
        :param pos: a 2D coordinate (y, x)
        :return: a 1D coordinate
        """
        y, x = pos
        n = x + (y * self.sizeX)
        return n

    def getSurrounding(self, n: int, size=1, warp=False):
        """
        :param n: 1D coordinate; point of origin
        :param size: size of ring; 1 = 3x3, 2 = 5x5 etc
        :param warp: ignore borders
        :return: surrounding positions
        """

        start_pos = n - (size * self.sizeX) - (size * 1)
        size = 2 * (size + 1) - 1
        ring = [list(range(start_pos + (i * self.sizeX), start_pos + size + (i * self.sizeX))) for i in range(size)]
        if not warp:
            _min = (self.sizeX * self.sizeY) - 1
            _max = 0

            # getting max and low
            for seg in ring[::-1]:
                for n in seg:
                    if 0 <= n < _min:
                        _min = n
                    if (self.sizeX * self.sizeY) - 1 >= n > _max:
                        _max = n

            _ring = set()
            for seg in ring:
                for n in seg:
                    # if the x of n is in the square
                    if self.get2D(_min)[1] <= self.get2D(n)[1] <= self.get2D(_max)[1]:
                        # if the y of n is in the square
                        if self.get2D(_min)[0] <= self.get2D(n)[0] <= self.get2D(_max)[0]:
                            _ring.add(n)
            ring = list(_ring)

        return ring

    def getLine(self, a, b) -> list:
        """
        TODO this is just the early implementation
        :param a: point a
        :param b: point b
        :return: list of points; a through b
        """
        line = list()
        a2D = self.get2D(a)
        b2D = self.get2D(b)
        while True:
            line.append(self.get1D(a2D))
            line.append(self.get1D(b2D))

            if a2D[0] < b2D[0]:
                a2D = (a2D[0] + 1, a2D[1])
            elif a2D[0] > b2D[0]:
                a2D = (a2D[0] - 1, a2D[1])

            if a2D[1] < b2D[1]:
                a2D = (a2D[0], a2D[1] + 1)
            elif a2D[1] > b2D[1]:
                a2D = (a2D[0], a2D[1] - 1)

            if a2D == b2D:
                line.append(self.get1D(a2D))
                break

            if b2D[0] < a2D[0]:
                b2D = (b2D[0] + 1, b2D[1])
            elif b2D[0] > a2D[0]:
                b2D = (b2D[0] - 1, b2D[1])

            if b2D[1] < a2D[1]:
                b2D = (b2D[0], b2D[1] + 1)
            elif b2D[1] > a2D[1]:
                b2D = (b2D[0], b2D[1] - 1)

            if a2D == b2D:
                line.append(self.get1D(b2D))
                break

        return line