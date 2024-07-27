import flet as ft
import janggibase
import flet.canvas as cv


class janggiPiece(ft.GestureDetector):
    def __init__(self, piece: janggibase.Piece, board: "replayBoard"):
        super().__init__()
        self.mouse_cursor = ft.MouseCursor.BASIC
        self.drag_interval = 5
        self.on_pan_start = None
        self.on_pan_update = None
        self.on_pan_end = None
        self.left = 40 * (piece.location // 10)
        self.top = 40 * (9 - piece.location % 10)
        self.content = ft.Container(
            width=40,
            height=40,
            border_radius=ft.border_radius.all(5),
            content=ft.Image(f"img/{str(piece).upper()}{piece.color}.png"),
        )
        self.board = board
        self.piece = piece
        self.slot = board.slots[piece.location]
        self.slot.ontop = self
        self.visible = True

    def place(self, slot):
        self.slot.ontop = None
        self.top = slot.top
        self.left = slot.left
        if slot.ontop:
            self.board.controls.remove(slot.ontop)
            self.board.piecelist.remove(slot.ontop)
        self.board.update()
        slot.ontop = self
        self.slot = slot


class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.ontop = None
        self.width = 40
        self.height = 40
        self.left = left
        self.top = top
        self.opacity = 0.8


class replayBoard(ft.Stack):
    def __init__(self, variant, record):
        super().__init__()
        cp = cv.Canvas(
            [
                cv.Path(
                    [
                        cv.Path.MoveTo(20, 20),
                        cv.Path.LineTo(20, 380),
                        cv.Path.MoveTo(60, 20),
                        cv.Path.LineTo(60, 380),
                        cv.Path.MoveTo(100, 20),
                        cv.Path.LineTo(100, 380),
                        cv.Path.MoveTo(140, 20),
                        cv.Path.LineTo(140, 380),
                        cv.Path.MoveTo(180, 20),
                        cv.Path.LineTo(180, 380),
                        cv.Path.MoveTo(220, 20),
                        cv.Path.LineTo(220, 380),
                        cv.Path.MoveTo(260, 20),
                        cv.Path.LineTo(260, 380),
                        cv.Path.MoveTo(300, 20),
                        cv.Path.LineTo(300, 380),
                        cv.Path.MoveTo(340, 20),
                        cv.Path.LineTo(340, 380),
                        cv.Path.MoveTo(20, 20),
                        cv.Path.LineTo(340, 20),
                        cv.Path.MoveTo(20, 60),
                        cv.Path.LineTo(340, 60),
                        cv.Path.MoveTo(20, 100),
                        cv.Path.LineTo(340, 100),
                        cv.Path.MoveTo(20, 140),
                        cv.Path.LineTo(340, 140),
                        cv.Path.MoveTo(20, 180),
                        cv.Path.LineTo(340, 180),
                        cv.Path.MoveTo(20, 220),
                        cv.Path.LineTo(340, 220),
                        cv.Path.MoveTo(20, 260),
                        cv.Path.LineTo(340, 260),
                        cv.Path.MoveTo(20, 300),
                        cv.Path.LineTo(340, 300),
                        cv.Path.MoveTo(20, 340),
                        cv.Path.LineTo(340, 340),
                        cv.Path.MoveTo(20, 380),
                        cv.Path.LineTo(340, 380),
                        cv.Path.MoveTo(140, 20),
                        cv.Path.LineTo(220, 100),
                        cv.Path.MoveTo(220, 20),
                        cv.Path.LineTo(140, 100),
                        cv.Path.MoveTo(140, 300),
                        cv.Path.LineTo(220, 380),
                        cv.Path.MoveTo(220, 300),
                        cv.Path.LineTo(140, 380),
                    ],
                    paint=ft.Paint(
                        color="white",
                        stroke_width=2,
                        style=ft.PaintingStyle.STROKE,
                    ),
                ),
            ],
            width=float("inf"),
            expand=True,
        )
        self.gameRecord = record.split()
        self.variant = variant
        self.board = janggibase.Board(self.variant)
        self.fenRecord = [self.board.makeFEN()]
        self.slots = []
        self.controls = [cp]
        self.width = 360
        self.height = 400
        self.move_num = 0
        for i in range(90):
            self.slots.append(Slot(40 * (9 - i % 10), 40 * (i // 10)))
        self.controls.extend(self.slots)
        self.piecelist = []
        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece, self))
        self.controls.extend(self.piecelist)
        self.moveNotation = []

        for i in range(len(self.gameRecord) - 1):
            movingPiece = ""
            if self.gameRecord[i] == "@@@@":
                move = [0, 0]
            else:
                move = [int(self.gameRecord[i][:2]), int(self.gameRecord[i][2:])]
                movingPiece = self.board.boardState[move[0]]
            if isinstance(movingPiece, janggibase.Cannon):
                movingPiece = "포"
            elif isinstance(movingPiece, janggibase.Chariot):
                movingPiece = "차"
            elif isinstance(movingPiece, janggibase.Elephant):
                movingPiece = "상"
            elif isinstance(movingPiece, janggibase.Guard):
                movingPiece = "사"
            elif isinstance(movingPiece, janggibase.Horse):
                movingPiece = "마"
            elif isinstance(movingPiece, janggibase.King):
                movingPiece = "궁"
            elif isinstance(movingPiece, janggibase.Soldier):
                if movingPiece.color:
                    movingPiece = "병"
                else:
                    movingPiece = "졸"
            else:
                movingPiece = ""
            notation = janggibase.Piece.moveToNotation(*move)
            self.moveNotation.append(notation[:2] + movingPiece + notation[2:])
            self.board.move(*move)
            self.fenRecord.append(self.board.makeFEN())
        self.moveNotation.append(self.gameRecord[-1])
        self.board = janggibase.Board(self.variant)

    def reset(self, board: janggibase.Board):
        cp = cv.Canvas(
            [
                cv.Path(
                    [
                        cv.Path.MoveTo(20, 20),
                        cv.Path.LineTo(20, 380),
                        cv.Path.MoveTo(60, 20),
                        cv.Path.LineTo(60, 380),
                        cv.Path.MoveTo(100, 20),
                        cv.Path.LineTo(100, 380),
                        cv.Path.MoveTo(140, 20),
                        cv.Path.LineTo(140, 380),
                        cv.Path.MoveTo(180, 20),
                        cv.Path.LineTo(180, 380),
                        cv.Path.MoveTo(220, 20),
                        cv.Path.LineTo(220, 380),
                        cv.Path.MoveTo(260, 20),
                        cv.Path.LineTo(260, 380),
                        cv.Path.MoveTo(300, 20),
                        cv.Path.LineTo(300, 380),
                        cv.Path.MoveTo(340, 20),
                        cv.Path.LineTo(340, 380),
                        cv.Path.MoveTo(20, 20),
                        cv.Path.LineTo(340, 20),
                        cv.Path.MoveTo(20, 60),
                        cv.Path.LineTo(340, 60),
                        cv.Path.MoveTo(20, 100),
                        cv.Path.LineTo(340, 100),
                        cv.Path.MoveTo(20, 140),
                        cv.Path.LineTo(340, 140),
                        cv.Path.MoveTo(20, 180),
                        cv.Path.LineTo(340, 180),
                        cv.Path.MoveTo(20, 220),
                        cv.Path.LineTo(340, 220),
                        cv.Path.MoveTo(20, 260),
                        cv.Path.LineTo(340, 260),
                        cv.Path.MoveTo(20, 300),
                        cv.Path.LineTo(340, 300),
                        cv.Path.MoveTo(20, 340),
                        cv.Path.LineTo(340, 340),
                        cv.Path.MoveTo(20, 380),
                        cv.Path.LineTo(340, 380),
                        cv.Path.MoveTo(140, 20),
                        cv.Path.LineTo(220, 100),
                        cv.Path.MoveTo(220, 20),
                        cv.Path.LineTo(140, 100),
                        cv.Path.MoveTo(140, 300),
                        cv.Path.LineTo(220, 380),
                        cv.Path.MoveTo(220, 300),
                        cv.Path.LineTo(140, 380),
                    ],
                    paint=ft.Paint(
                        color="white",
                        stroke_width=2,
                        style=ft.PaintingStyle.STROKE,
                    ),
                ),
            ],
            width=float("inf"),
            expand=True,
        )
        self.controls = [cp]
        self.slots = []
        for i in range(90):
            self.slots.append(Slot(40 * (9 - i % 10), 40 * (i // 10)))
        self.controls.extend(self.slots)
        self.piecelist = []

        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece, self))
        self.controls.extend(self.piecelist)

    def move(self, e):
        if self.move_num < len(self.gameRecord) - 1:
            self.move_num += 1
            self.board = janggibase.Board(self.variant, self.fenRecord[self.move_num])
            self.reset(self.board)
            self.update()

    def undo_move(self, e):
        if self.move_num:
            self.move_num -= 1
            self.board = janggibase.Board(self.variant, self.fenRecord[self.move_num])
            self.reset(self.board)
            self.update()

    def set_move(self, move_num):
        self.move_num = move_num + 1
        self.board = janggibase.Board(self.variant, self.fenRecord[self.move_num])
        self.reset(self.board)
        self.update()


if __name__ == "__main__":
    import time
    def main(page):
        page.add(replayBoard(15,'8373 1927 @@@@ 7956 7383 4636 8373 1747 4353 2946 0-1'))
        for i in range(10):
            time.sleep(0.5)
            page.controls[0].move(None)
        for i in range(5):
            time.sleep(0.5)
            page.controls[0].undo_move(None)
        time.sleep(0.5)
        page.controls[0].set_move(8)


    ft.app(target=main)
