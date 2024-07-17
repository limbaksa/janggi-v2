import flet as ft
import janggibase

def move_on_top(piece,controls):
    controls.remove(piece)
    controls.append(piece)

def start_drag(e:ft.DragStartEvent):
    move_on_top(e.control,e.control.board.controls)
    e.control.board.move_start_top=e.control.top
    e.control.board.move_start_left=e.control.left
    e.control.update()

def bounce_back(board,piece):
    piece.top=board.move_start_top
    piece.left=board.move_start_left
    board.update()

def drag(e: ft.DragUpdateEvent):
   e.control.top = max(0, e.control.top + e.delta_y)
   e.control.left = max(0, e.control.left + e.delta_x)
   e.control.update()

def drop(e:ft.DragEndEvent):
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
        piece.board.update()


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
        self.ontop = None
        self.width = 60
        self.height = 60
        self.left = left
        self.top = top


class janggiBoard(ft.Stack):
    def __init__(self, board: janggibase.Board):
        super().__init__()
        self.board = board
        self.slots = []
        self.controls = []
        self.width = 540
        self.height = 600
        for i in range(90):
            self.slots.append(Slot(60 * (9 - i % 10), 60 * (i // 10)))
        self.controls.extend(self.slots)
        self.piecelist = []
        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece, self))
        self.controls.extend(self.piecelist)
        self.move_start_top=None
        self.move_start_left=None


    

if __name__ == "__main__":

    def main(page):
        page.add(janggiBoard(janggibase.Board(15)))

    ft.app(target=main)