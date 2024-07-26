import flet as ft
from janggiplayer import AI
import flet.canvas as cv
import janggibase
from db import db

def move_on_top(piece,controls):
    controls.remove(piece)
    controls.append(piece)
    piece.board.update()


def start_drag(e:ft.DragStartEvent):
    move_on_top(e.control,e.control.board.controls)
    e.control.board.move_start_top=e.control.top
    e.control.board.move_start_left=e.control.left
    if e.control.piece.color == e.control.board.board.turn and (
            not e.control.board.ai or e.control.piece.color != e.control.board.aiturn
        ):
            for slot in e.control.board.slots:
                if e.control.piece.isValidMove(e.control.board.slots.index(slot)):
                    slot.content = ft.Image(f"img/able.png")
                    e.control.board.controls.remove(slot)
                    e.control.board.controls.append(slot)
                    e.control.update()
                    slot.update()


def bounce_back(board,piece):
    piece.top=board.move_start_top
    piece.left=board.move_start_left
    piece.update()

def drag(e: ft.DragUpdateEvent):
   e.control.top = max(0, e.control.top + e.delta_y)
   e.control.left = max(0, e.control.left + e.delta_x)
   e.control.update()

def drop(e:ft.DragEndEvent):
    for slot in e.control.board.slots:
        slot.content=None
        slot.update()

    for slot in e.control.board.slots:
        if (
            abs(e.control.top - slot.top) < 20
            and abs(e.control.left - slot.left) < 20
        ):
            place(e.control, slot)
            break
    else:
        bounce_back(e.control.board,e.control)
    e.control.update()

def place(piece,slot):
    piece.top=slot.top
    piece.left=slot.left
    piece.update()


class janggiPiece(ft.GestureDetector):
    def __init__(self, piece: janggibase.Piece, board: "janggiBoard"):
        super().__init__()
        self.piece=piece
        self.board=board
        self.mouse_cursor=ft.MouseCursor.MOVE
        self.drag_interval=5
        self.on_pan_start=start_drag
        self.on_pan_update=drag
        self.on_pan_end=drop
        self.left = 60 * (piece.location // 10)
        self.top = 60 * (9 - piece.location % 10)
        self.content=ft.Container(
            width=60,
            height=60,
            border_radius=ft.border_radius.all(5),
            content=ft.Image(f"img/{str(piece).upper()}{piece.color}.png"),
        )
    



class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.width = 60
        self.height = 60
        self.left = left
        self.top = top


class janggiBoard(ft.Stack):
    def __init__(self, board: janggibase.Board, ai=False, aiturn=None):
        super().__init__()
        
        self.board = board
        self.slots = []
        self.controls = []
        self.width = 540
        self.height = 600
        self.piecelist = []
        self.move_start_top=None
        self.move_start_left=None
        self.ai = AI(self.board, aiturn) if ai else None
        self.aiturn = aiturn
    def did_mount(self):
        cp = cv.Canvas(
            [
                cv.Path(
                    [
                        cv.Path.MoveTo(30, 30),
                        cv.Path.LineTo(30, 570),
                        cv.Path.MoveTo(90, 30),
                        cv.Path.LineTo(90, 570),
                        cv.Path.MoveTo(150, 30),
                        cv.Path.LineTo(150, 570),
                        cv.Path.MoveTo(210, 30),
                        cv.Path.LineTo(210, 570),
                        cv.Path.MoveTo(270, 30),
                        cv.Path.LineTo(270, 570),
                        cv.Path.MoveTo(330, 30),
                        cv.Path.LineTo(330, 570),
                        cv.Path.MoveTo(390, 30),
                        cv.Path.LineTo(390, 570),
                        cv.Path.MoveTo(450, 30),
                        cv.Path.LineTo(450, 570),
                        cv.Path.MoveTo(510, 30),
                        cv.Path.LineTo(510, 570),
                        cv.Path.MoveTo(30, 30),
                        cv.Path.LineTo(510, 30),
                        cv.Path.MoveTo(30, 90),
                        cv.Path.LineTo(510, 90),
                        cv.Path.MoveTo(30, 150),
                        cv.Path.LineTo(510, 150),
                        cv.Path.MoveTo(30, 210),
                        cv.Path.LineTo(510, 210),
                        cv.Path.MoveTo(30, 270),
                        cv.Path.LineTo(510, 270),
                        cv.Path.MoveTo(30, 330),
                        cv.Path.LineTo(510, 330),
                        cv.Path.MoveTo(30, 390),
                        cv.Path.LineTo(510, 390),
                        cv.Path.MoveTo(30, 450),
                        cv.Path.LineTo(510, 450),
                        cv.Path.MoveTo(30, 510),
                        cv.Path.LineTo(510, 510),
                        cv.Path.MoveTo(30, 570),
                        cv.Path.LineTo(510, 570),
                        cv.Path.MoveTo(210, 30),
                        cv.Path.LineTo(330, 150),
                        cv.Path.MoveTo(330, 30),
                        cv.Path.LineTo(210, 150),
                        cv.Path.MoveTo(210, 450),
                        cv.Path.LineTo(330, 570),
                        cv.Path.MoveTo(330, 450),
                        cv.Path.LineTo(210, 570),
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
        self.controls.append(cp)
        for i in range(90):
            self.slots.append(Slot(60 * (9 - i % 10), 60 * (i // 10)))
        self.controls.extend(self.slots)
        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece, self))
        self.controls.extend(self.piecelist)
        self.update()
        return super().did_mount()
    

if __name__ == "__main__":

    def main(page):
        page.add(janggiBoard(janggibase.Board(15)))

    ft.app(target=main)