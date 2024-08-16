import janggibase
import subprocess
import time


class AI:
    def __init__(self, board: janggibase.Board, color: int,skill: int):
        self.board = board
        self.color = color
        l = ["eh", "he"]
        L = ["EH", "HE"]
        self.process = subprocess.Popen(
            "stockfish",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        self.process.stdin.write("xboard\n")
        self.process.stdin.write("protover 2\n")
        self.process.stdin.write("option EvalFile=janggi-4d3de2fee245.nnue\n")
        self.process.stdin.write("option Use NNUE=1\n")
        self.process.stdin.write("option VariantPath=variants.ini\n")
        self.process.stdin.write(f"option Skill Level={skill}\n")
        self.process.stdin.flush()
        self.process.stdin.write("new\n")
        self.process.stdin.write(
            f"variant janggi_{l[self.board.variant&1]+l[(self.board.variant&2)>>1]+L[(self.board.variant&4)>>2]+L[(self.board.variant&8)>>3]}\n"
        )
        self.process.stdin.flush()

    def getMove(self) -> str:
        self.process.stdin.write(f"setboard {self.board.makeFEN()}\n")
        self.process.stdin.write("go\n")
        self.process.stdin.flush()
        time.sleep(2)
        self.process.stdin.write("?\n")
        self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline()
            if line.startswith("move"):
                return line.split()[1]

    def getFirstMove(self) -> str:
        self.process.stdin.write(f"setboard {self.board.makeFEN()}\n")
        self.process.stdin.write("go\n")
        self.process.stdin.flush()
        time.sleep(0.7)
        self.process.stdin.write("?\n")
        self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline()
            if line.startswith("move"):
                return line.split()[1]

# Skill level 20: Master, 10: hard, 0: Intermediate, -10: Easy, -20: Beginner