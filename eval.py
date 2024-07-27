import subprocess
import time
import janggibase

def get_eval(FEN):
    l = ["eh", "he"]
    L = ["EH", "HE"]
    b=janggibase.Board(0,FEN)
    if (b.kings[0].location // 10 == b.kings[1].location // 10 or b.kings[0].location % 10 == b.kings[1].location % 10)and b.piecesBetween(b.kings[0].location, b.kings[1].location) == 0:
        return '빅장'
    process = subprocess.Popen(
        "stockfish",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    process.stdin.write("xboard\n")
    process.stdin.write("protover 2\n")
    process.stdin.write("option EvalFile=janggi-4d3de2fee245.nnue\n")
    process.stdin.write("option Use NNUE=1\n")
    process.stdin.write("option UCI_AnalyseMode=0\n")
    process.stdin.write("new\n")
    process.stdin.write(f"variant janggi\n")
    process.stdin.write(f"setboard {FEN}\n")
    time.sleep(0.5)
    matein = 0
    check = False
    while matein < 12 or check:
        process.stdin.write("go\n")
        process.stdin.flush()
        matein += 1
        time.sleep(0.2)
        process.stdin.write("?\n")
        process.stdin.write("eval\n")
        process.stdin.flush()
        while True:
            line = process.stdout.readline()
            if (
                line.startswith("1-0")
                or line.startswith("0-1")
                or line.startswith("1/2-1/2")
            ):
                if line.startswith("1-0"):
                    if matein // 2:
                        return "M" + str(matein // 2)
                    else:
                        return "1-0"
                elif line.startswith("0-1"):
                    if matein // 2:
                        return "M-" + str(matein // 2)
                    else:
                        return "0-1"
                else:
                    return "0.00"
            elif line.startswith("Final evaluation"):
                if matein >= 9:
                    loc = line.find("+") if line.find("+") != -1 else line.find("-")
                    if loc == -1:
                        check = True
                        break
                    return line[loc : loc + 5]
                else:
                    break


if __name__ == "__main__":
    #print(get_eval("6R2/9/1chk3R1/1pp1pepp1/9/9/1PP1P1PP1/1C5C1/4K4/1EHA1AEH1/ b")) #M3
    print(get_eval("rhea1aehr/4k4/1c5c1/p1p2pp1p/9/9/P1P2P1PP/1C5C1/4K4/REHA1AEHR/ b"))
