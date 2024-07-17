"""
    위치 번호
    a b c d e f g h i
  9
  8
  7
  6
  5
  4
  3
  2
  1
  0 
  ->a,b,c,d,e,f,g,h,i ->0,1,2,3,4,5,6,7,8 (10의자리)  
  30~32,40~42,50~52 초궁
  37~39,47~49,57~59 한궁

  초:0, 한:1
-> 궁 위치 (30~32,40~42,50~52)+color*7

궁 내에서 움직임 구현
30,32,50,52에서 41로 이동 가능
41에서 30,32,50,52로 이동 가능

한국장기협회식 표기법
    1 2 3 4 5 6 7 8 9
  1
  2
  3
  4
  5
  6
  7
  8
  9
  0
  ->1~0이 십의자리, 1~9가 일의자리 
"""
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
palace = [[30, 31, 32, 40, 41, 42, 50, 51, 52], [37, 38, 39, 47, 48, 49, 57, 58, 59]]
palaceDiagonal = [[30, 32, 50, 52], [37, 39, 57, 59]]
palaceCenter = [41, 48]


class Piece:
    def __init__(self, location: int, color: int, board: "Board"):
        self.location = location
        self.color = color
        self.palace = palace[color]
        self.board = board

    @staticmethod
    def MoveToUCI(start: int, dest: int) -> str:
        startstr = alphabet[start // 10] + str(start % 10)
        deststr = alphabet[dest // 10] + str(dest % 10)
        if startstr == deststr:
            return "@@@@"
        return startstr + deststr

    @staticmethod
    def UCIToMove(uci: str) -> tuple[int, int]:
        if uci == "@@@@":
            return (0, 0)
        start = uci[:2]
        dest = uci[2:]
        startint = alphabet.index(start[0]) * 10 + int(start[1])
        destint = alphabet.index(dest[0]) * 10 + int(dest[1])
        return (startint, destint)

    @staticmethod
    def moveToNotation(start: int, dest: int) -> str:
        if start == 0 and dest == 0:
            return "수 쉼"
        s0 = start // 10
        s1 = start % 10
        d0 = dest // 10
        d1 = dest % 10
        s0 += 1
        d0 += 1
        s1 = (10 - s1) % 10
        d1 = (10 - d1) % 10
        return f"{s1}{s0}{d1}{d0}"

    def isValidMove(self, dest: int) -> bool:
        if (
            self.isAttacking(dest)
            and self.board.pieceColor(dest) != self.color
            and not self.board.gameOver
        ):
            tempBoard = Board(0, self.board.makeFEN())
            tempBoard.movePiece(self.location, dest)
            if not tempBoard.isJanggoon(self.color):
                return True
        return False

    def getValidMoves(self) -> list[int]:
        moves = []
        for dest in range(81):
            if self.isValidMove(dest):
                moves.append(dest)
        return moves

    def isAttacking(self, dest: int) -> bool:
        return True

    def getAttackingSquares(self) -> list[int]:
        moves = []
        for dest in range(90):
            if self.isAttacking(dest):
                moves.append(dest)
        return moves

    def __str__(self) -> str:
        return (
            self.__class__.__name__[0]
            if self.color == 0
            else self.__class__.__name__[0].lower()
        )


class SlidingPiece(Piece):
    def palaceMove(self, start: int, dest: int) -> bool:
        """
        궁 내부에서 움직임(대각선 포함)을 정의합니다. 이는 차,왕,사,병에서 활용됩니다.
        궁 내부에서 궁 내부로, 가능한 움직임이라면 True를 반환합니다.
        중간에 기물이 있는지 등은 검사하지 않습니다.
        """
        if start not in palace[0] + palace[1] or dest not in palace[0] + palace[1]:
            return False  # 궁 내부의 움직임이 아님

        for i in range(2):
            if start in palaceDiagonal[i] and dest == palaceCenter[i]:  # 대각선->중심
                return True
            elif start == palaceCenter[i] and dest in palaceDiagonal[i]:  # 중심->대각선
                return True
            elif start in palace[i] and dest in palace[i]:  # 일반적인 직선 움직임
                if dest - start in [-10, -1, 1, 10]:
                    return True
            if (
                (isinstance(self, Chariot) or isinstance(self, Cannon))
                and start in palaceDiagonal[i]
                and dest in palaceDiagonal[i]
            ):  # 차,포의 움직임
                if dest - start in [-18, -22, 22, 18]:
                    return True

        return False


class Guard(SlidingPiece):
    def isAttacking(self, dest: int) -> bool:
        if self.palaceMove(self.location, dest):
            if self.board.pieceColor(dest) != self.color:
                return True
        return False

    def __str__(self) -> str:
        return "A" if self.color == 0 else "a"


class King(Guard):
    def __str__(self) -> str:
        return "K" if self.color == 0 else "k"


class Soldier(SlidingPiece):
    def isAttacking(self, dest: int) -> bool:
        backDir = -1 + 2 * self.color
        if [dest % 10 - self.location % 10, dest // 10 - self.location // 10] not in [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1],
        ] and not self.palaceMove(self.location, dest):
            return False
        if (dest % 10) - (self.location % 10) == backDir:
            return False
        return True

    def __str__(self) -> str:
        return "P" if self.color == 0 else "p"


class Chariot(SlidingPiece):
    def isAttacking(self, dest: int) -> bool:
        if (
            (self.location // 10) == (dest // 10)
            or (self.location % 10) == (dest % 10)
            or self.palaceMove(self.location, dest)
        ):
            if (
                self.board.piecesBetween(self.location, dest) == 0
                and self.board.pieceColor(dest) != self.color
            ):
                return True
        return False

    def __str__(self) -> str:
        return "R" if self.color == 0 else "r"


class Cannon(SlidingPiece):
    def isAttacking(self, dest: int) -> bool:
        if (
            (self.location // 10) == (dest // 10)
            or (self.location % 10) == (dest % 10)
            or self.palaceMove(self.location, dest)
        ):
            if (
                self.board.piecesBetween(self.location, dest) == 1
                and self.board.pieceColor(dest) != self.color
            ):
                if self.location // 10 == dest // 10:
                    dir = 1 if dest > self.location else -1
                    for i in range(self.location + dir, dest + dir, dir):
                        if isinstance(self.board.boardState[i], Cannon):
                            return False
                elif self.location % 10 == dest % 10:
                    dir = 10 if dest > self.location else -10
                    for i in range(self.location + dir, dest + dir, dir):
                        if isinstance(self.board.boardState[i], Cannon):
                            return False
                else:
                    if (
                        not isinstance(
                            self.board.boardState[(self.location + dest) // 2], Cannon
                        )
                    ) and (not isinstance(self.board.boardState[dest], Cannon)):
                        return True
                    else:
                        return False
                return True
        return False


class Horse(Piece):
    def isAttacking(self, dest: int) -> bool:
        if [dest % 10 - self.location % 10, dest // 10 - self.location // 10] not in [
            [2, 1],
            [2, -1],
            [1, 2],
            [1, -2],
            [-2, 1],
            [-2, -1],
            [-1, 2],
            [-1, -2],
        ]:
            return False
        if (
            self.board.piecesBetween(self.location, dest) == 0
            and self.board.pieceColor(dest) != self.color
        ):
            return True
        return False


class Elephant(Piece):
    def isAttacking(self, dest: int) -> bool:
        if [dest % 10 - self.location % 10, dest // 10 - self.location // 10] not in [
            [3, 2],
            [3, -2],
            [2, 3],
            [2, -3],
            [-3, 2],
            [-3, -2],
            [-2, 3],
            [-2, -3],
        ]:
            return False
        if (
            self.board.piecesBetween(self.location, dest) == 0
            and self.board.pieceColor(dest) != self.color
        ):
            return True
        return False


class Board:
    def __init__(self, variant: int, fen: str = ""):
        self.boardState: list = [False for _ in range(90)]
        self.pieces: list = [[] for _ in range(2)]
        self.kings: list = [None, None]
        self.turn = 0
        self.variant = variant
        self.wasBikjang: bool = False
        self.gameRecord: list = []
        self.boardRecord: list = []
        self.gameOver = 0
        l = ["eh", "he"]
        L = ["EH", "HE"]
        if not fen:
            fen = f"r{l[variant&1]}a1a{l[(variant&2)>>1]}r/4k4/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/4K4/R{L[(variant&4)>>2]}A1A{L[(variant&8)>>3]}R w"
        fen_l = fen.split()
        fen_list = fen_l[0].split("/")
        for i in range(10):
            j = 0
            for p in fen_list[i]:
                if p.isdecimal():
                    j += int(p) - 1
                elif p == "r":
                    self.boardState[10 * j + 9 - i] = Chariot(10 * j + 9 - i, 1, self)
                    self.pieces[1].append(self.boardState[10 * j + 9 - i])
                elif p == "e":
                    self.boardState[10 * j + 9 - i] = Elephant(10 * j + 9 - i, 1, self)
                    self.pieces[1].append(self.boardState[10 * j + 9 - i])
                elif p == "h":
                    self.boardState[10 * j + 9 - i] = Horse(10 * j + 9 - i, 1, self)
                    self.pieces[1].append(self.boardState[10 * j + 9 - i])
                elif p == "a":
                    self.boardState[10 * j + 9 - i] = Guard(10 * j + 9 - i, 1, self)
                    self.pieces[1].append(self.boardState[10 * j + 9 - i])
                elif p == "k":
                    self.boardState[10 * j + 9 - i] = King(10 * j + 9 - i, 1, self)
                    self.pieces[1].append(self.boardState[10 * j + 9 - i])
                    self.kings[1] = self.boardState[10 * j + 9 - i]
                elif p == "p":
                    self.boardState[10 * j + 9 - i] = Soldier(10 * j + 9 - i, 1, self)
                    self.pieces[1].append(self.boardState[10 * j + 9 - i])
                elif p == "c":
                    self.boardState[10 * j + 9 - i] = Cannon(10 * j + 9 - i, 1, self)
                    self.pieces[1].append(self.boardState[10 * j + 9 - i])

                elif p == "R":
                    self.boardState[10 * j + 9 - i] = Chariot(10 * j + 9 - i, 0, self)
                    self.pieces[0].append(self.boardState[10 * j + 9 - i])
                elif p == "E":
                    self.boardState[10 * j + 9 - i] = Elephant(10 * j + 9 - i, 0, self)
                    self.pieces[0].append(self.boardState[10 * j + 9 - i])
                elif p == "H":
                    self.boardState[10 * j + 9 - i] = Horse(10 * j + 9 - i, 0, self)
                    self.pieces[0].append(self.boardState[10 * j + 9 - i])
                elif p == "A":
                    self.boardState[10 * j + 9 - i] = Guard(10 * j + 9 - i, 0, self)
                    self.pieces[0].append(self.boardState[10 * j + 9 - i])
                elif p == "K":
                    self.boardState[10 * j + 9 - i] = King(10 * j + 9 - i, 0, self)
                    self.pieces[0].append(self.boardState[10 * j + 9 - i])
                    self.kings[0] = self.boardState[10 * j + 9 - i]
                elif p == "P":
                    self.boardState[10 * j + 9 - i] = Soldier(10 * j + 9 - i, 0, self)
                    self.pieces[0].append(self.boardState[10 * j + 9 - i])
                elif p == "C":
                    self.boardState[10 * j + 9 - i] = Cannon(10 * j + 9 - i, 0, self)
                    self.pieces[0].append(self.boardState[10 * j + 9 - i])
                j += 1
        self.turn = 0 if fen_l[1] == "w" else 1
        self.boardRecord.append(self.makeFEN())

    def piecesBetween(self, start: int, dest: int) -> int:
        dx = dest // 10 - start // 10
        dy = dest % 10 - start % 10
        cnt = 0
        if not dx:
            for i in range(min(start, dest) + 1, max(start, dest), 1):
                if self.boardState[i]:
                    cnt += 1
        elif not dy:
            for i in range(min(start, dest) + 10, max(start, dest), 10):
                if self.boardState[i]:
                    cnt += 1
        else:
            dirx = 1 if dx > 0 else -1
            diry = 1 if dy > 0 else -1
            if abs(dx) > abs(dy):
                cnt += 1 if self.boardState[start + 10 * dirx] else 0
                dx -= dirx
                start += 10 * dirx
            elif abs(dx) < abs(dy):
                cnt += 1 if self.boardState[start + diry] else 0
                dy -= diry
                start += diry
            for i in range(1, abs(dx)):
                cnt += 1 if self.boardState[start + i * diry + 10 * i * dirx] else 0

        return cnt

    def pieceColor(self, location: int) -> int:
        """해당 위치의 기물 색을 반환합니다.

        Args:
            location (int): 말이 무슨 색인지 알고싶은 위치

        Returns:
            int: 기물이 없다면 -1, 초이면 0, 한이면 1
        """
        if self.boardState[location]:
            return self.boardState[location].color
        else:
            return -1

    def isJanggoon(self, color):
        attackingSquares = set()
        for piece in self.pieces[1 - color]:
            attackingSquares.update(piece.getAttackingSquares())
        if self.kings[color].location in attackingSquares:
            return True
        else:
            return False

    def isBikjang(self):
        if (
            self.wasBikjang
            and (
                self.kings[0].location // 10 == self.kings[1].location // 10
                or self.kings[0].location % 10 == self.kings[1].location % 10
            )
            and self.piecesBetween(self.kings[0].location, self.kings[1].location) == 0
        ):
            return True
        return False

    def showBoard(self):
        for i in range(9, -1, -1):
            for j in range(9):
                if self.boardState[j * 10 + i]:
                    print(f"{self.boardState[j*10+i]}", end=" ")
                else:
                    print("  ", end="")
            print()

    def makeFEN(self) -> str:
        fen = ""
        for i in range(9, -1, -1):
            blank = 0
            for j in range(9):
                if not self.boardState[i + j * 10]:
                    blank += 1
                else:
                    if blank:
                        fen += str(blank)
                        blank = 0
                    if self.pieceColor(i + j * 10):
                        fen += str(self.boardState[i + j * 10]).lower()
                    else:
                        fen += str(self.boardState[i + j * 10])
            if blank:
                fen += str(blank)
            fen += "/"
        fen += " " + ("b" if self.turn else "w")
        return fen

    def movePiece(self, start: int, dest: int) -> bool:
        if self.boardState[start]:
            if self.boardState[dest]:
                for i in range(len(self.pieces[self.boardState[dest].color])):
                    if (
                        self.pieces[self.boardState[dest].color][i]
                        is self.boardState[dest]
                    ):
                        del self.pieces[self.boardState[dest].color][i]
                        break
            self.boardState[dest] = self.boardState[start]
            self.boardState[start] = False
            self.boardState[dest].location = dest
            self.turn = 1 - self.turn
            return True
        return False

    def move(self, start: int, dest: int) -> int:
        if self.gameOver:
            return 0
        if start == 0 and dest == 0:
            if not self.isJanggoon(self.turn):
                if (
                    self.kings[0].location // 10 == self.kings[1].location // 10
                    or self.kings[0].location % 10 == self.kings[1].location % 10
                ) and self.piecesBetween(
                    self.kings[0].location, self.kings[1].location
                ) == 0:
                    self.wasBikjang = True
                else:
                    self.wasBikjang = False
                self.turn = 1 - self.turn
                self.gameRecord.append("@@@@")
                self.boardRecord.append(self.makeFEN())
                if self.isGameOver(self.turn):
                    self.gameRecord.append(
                        "1/2-1/2"
                        if self.isGameOver(self.turn) == "무승부"
                        else f"{self.turn}-{1-self.turn}"
                    )
                    return -1
                return 1
            else:
                print("장군일 때는 수를 쉴 수 없습니다.")
                return 0

        if self.boardState[start]:
            if self.boardState[start].isValidMove(dest):
                if (
                    self.kings[0].location // 10 == self.kings[1].location // 10
                    or self.kings[0].location % 10 == self.kings[1].location % 10
                ) and self.piecesBetween(
                    self.kings[0].location, self.kings[1].location
                ) == 0:
                    self.wasBikjang = True
                else:
                    self.wasBikjang = False
                if self.boardState[dest]:
                    for i in range(len(self.pieces[self.boardState[dest].color])):
                        if (
                            self.pieces[self.boardState[dest].color][i]
                            is self.boardState[dest]
                        ):
                            del self.pieces[self.boardState[dest].color][i]
                            break
                self.boardState[dest] = self.boardState[start]
                self.boardState[dest].location = dest
                self.boardState[start] = False
                self.turn = 1 - self.turn
                self.gameRecord.append(f"{start:0>2}{dest:0>2}")
                self.boardRecord.append(self.makeFEN())
                if self.isGameOver(self.turn):
                    self.gameRecord.append(
                        "1/2-1/2"
                        if self.isGameOver(self.turn) == "무승부"
                        else f"{self.turn}-{1-self.turn}"
                    )
                    return -1
                return 1
        print(f"{start,dest} is an INVALID MOVE!")
        return 0

    def isGameOver(self, color: int) -> str:
        if self.isJanggoon(color):
            checkmate = True
            for i in self.pieces[color]:
                if len(i.getValidMoves()):
                    checkmate = False
                    break
            if checkmate:
                self.gameOver = 1
                return f"{['한','초'][color]} 승"
            else:
                return ""
        if self.gameOver == 1:
            return f"{['한','초'][self.turn]} 승"
        if self.isBikjang() or self.boardRecord.count(self.makeFEN()) >= 3:
            self.gameOver = 2
            return "무승부"
        else:
            return ""

    def resign(self) -> str:
        if not self.gameOver:
            self.gameRecord.append(f"{self.turn}-{1-self.turn}")
            self.gameOver = 1
            return f'{["한","초"][self.turn]} 승'
        else:
            return ""


if __name__ == "__main__":
    B = Board(5)
