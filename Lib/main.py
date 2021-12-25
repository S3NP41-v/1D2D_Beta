

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

    def getSurrounding(self, n: int, size=1, warp=False) -> list:
        """
        :param n: 1D coordinate; point of origin
        :param size: size of ring; 1 = 3x3, 2 = 5x5 etc
        :param warp: ignore borders
        :return: surrounding positions
        """
        if n not in self.board:
            raise Exception("Position outside of board!")

        if size < 1:
            raise Exception("Size cannot be smaller than 1!")

        n2D = self.get2D(n)
        # getting coordinates
        smallest = (n2D[0] - (1 * size), n2D[1] - (1 * size))
        largest = (n2D[0] + (1 * size), n2D[1] + (1 * size))
        print(f"pre check:\n\tsmallest: {smallest, self.get1D(smallest)}\n\tlargest: {largest, self.get1D(largest)}")


        # correcting
        if not warp:
            # checking smallest
            while self.get1D(smallest) not in self.board:
                if self.get1D((smallest[0], smallest[1] + 1)) in self.board:
                    smallest = (smallest[0], smallest[1] + 1)
                    break

                elif self.get1D((smallest[0] + 1, smallest[1])) in self.board:
                    smallest = (smallest[0] + 1, smallest[1])
                    break
                
                else:
                    smallest = (smallest[0] + 1, smallest[1] + 1)

            # checking largest
            while self.get1D(largest) not in self.board:
                if self.get1D((largest[0], largest[1] - 1)) in self.board:
                    largest = (largest[0], largest[1] - 1)
                    break

                elif self.get1D((largest[0] - 1, largest[1])) in self.board:
                    largest = (largest[0] - 1, largest[1])
                    break

                else:
                    largest = (largest[0] - 1, largest[1] - 1)

        ring = []
        for i in range(self.get1D(smallest), self.get1D(largest) + 1):
            i2D = self.get2D(i)
            print(f"checking i: {i}\ti2D: {i2D}\t\tagainst: {smallest}\t{largest}")


            # 0 >= 0 and 0 >= 0
            if i2D[0] >= smallest[0] and i2D[1] >= smallest[1]:  # if is in smallest range
                print(f"passed {i}\t{i2D}")


                if i2D[0] <= largest[0] and i2D[1] <= largest[1]:  # if is in largest range
                    ring.append(i)

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
