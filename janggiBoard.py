import flet as ft
from janggiplayer import AI
import flet.canvas as cv
import janggibase
from db import db

def move_on_top(piece,controls):
    controls.remove(piece)
    controls.append(piece)
    piece.board.update(movingPiece=piece)

def start_drag(e:ft.DragStartEvent):
    move_on_top(e.control,e.control.board.controls)
    e.control.board.move_start_top=e.control.top
    e.control.board.move_start_left=e.control.left
    if e.control.piece.color == e.control.board.board.turn and (
            not e.control.board.ai or e.control.piece.color != e.control.board.aiturn
        ):
            ablelist=[]
            for slot in e.control.board.slots:
                if e.control.piece.isValidMove(e.control.board.slots.index(slot)):
                    ablelist.append(ft.Container(content=ft.Image(f"img/able.png"),left=slot.left,top=slot.top,width=50,height=50))
            e.control.board.ablelist.extend(ablelist)
            e.control.board.update(e.control)


def bounce_back(board,piece):
    piece.top=board.move_start_top
    piece.left=board.move_start_left
    piece.update()

def drag(e: ft.DragUpdateEvent):
   e.control.top = max(0, e.control.top + e.delta_y)
   e.control.left = max(0, e.control.left + e.delta_x)
   e.control.update()

def drop(e:ft.DragEndEvent):
    for able in e.control.board.ablelist:
        e.control.board.controls.remove(able)
    e.control.board.ablelist=[]
    e.control.board.update(e.control)
    if e.control.piece.color == e.control.board.board.turn and (
            not e.control.board.ai or e.control.piece.color != e.control.board.aiturn
        ):
        for slot in e.control.board.slots:
            if (
                abs(e.control.top - slot.top) < 20
                and abs(e.control.left - slot.left) < 20
            ):
                if e.control.piece.isValidMove(e.control.board.slots.index(slot)):
                        trymove = e.control.board.board.move(
                            e.control.piece.location, e.control.board.slots.index(slot)
                        )
                        if trymove:
                            e.control.board.moved=[]
                            e.control.board.moved.append(
                                ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                                opacity=0.2,
                                width=50,
                                height=50,
                                left=slot.left,
                                top=slot.top))
                            e.control.board.moved.append(
                                ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                                opacity=0.2,
                                width=50,
                                height=50,
                                left=e.control.slot.left,
                                top=e.control.slot.top))
                            e.control.board.update(e.control)
                            place(e.control,slot)
                            if trymove == -1:
                                e.control.board.gameOver(
                                    e.control.board.board.isGameOver(e.control.board.board.turn)
                                )

                            if e.control.board.ai:
                                m = e.control.board.ai.getMove()
                                move = janggibase.Piece.UCIToMove(m)
                                e.control.board.moved=[]
                                trymove = e.control.board.board.move(*move)
                                piece = e.control.board.slots[move[0]].ontop
                                if m!='@@@@':
                                    e.control.board.moved.append(
                                        ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                                                     opacity=0.2,
                                                     width=50,
                                                     height=50,
                                                     left=piece.slot.left,
                                                     top=piece.slot.top))

                                    e.control.board.moved.append(
                                        ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                                                     opacity=0.2,
                                                     width=50,
                                                     height=50,
                                                     left=e.control.board.slots[move[1]].left,
                                                     top=e.control.board.slots[move[1]].top))
                                    e.control.board.update(piece)
                                    place(piece,e.control.board.slots[move[1]])
                                else:
                                    e.control.board.update()
                                if trymove == -1:
                                    e.control.board.gameOver(
                                        e.control.board.board.isGameOver(e.control.board.board.turn)
                                    )

                            return
                        else:
                            e.control.bounce_back()
                            e.control.update()
                            return
        else:
            bounce_back(e.control.board,e.control)
    else:
        bounce_back(e.control.board,e.control)
    e.control.update()

def place(piece,slot):
    piece.slot.ontop = None
    piece.slot=slot
    piece.top=slot.top
    piece.left=slot.left
    slot.ontop=piece
    if len(piece.board.controls):
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
        self.left = 50 * (piece.location // 10)
        self.top = 50 * (9 - piece.location % 10)
        self.content=ft.Container(
            width=50,
            height=50,
            border_radius=ft.border_radius.all(5),
            content=ft.Image(f"img/{str(piece).upper()}{piece.color}.png"),
        )
        self.slot = board.slots[piece.location]
        self.slot.ontop = self
    



class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.width = 50
        self.height = 50
        self.left = left
        self.top = top
        self.ontop=None


class janggiBoard(ft.Stack):
    def __init__(self, board: janggibase.Board, ai=False, aiturn=None,aiskill=None):
        super().__init__()
        
        self.board = board
        self.slots = []
        self.controls = []
        self.piecelist = []
        self.ablelist=[]
        self.moved=[]
        self.width = 450
        self.height = 500
        self.move_start_top=None
        self.move_start_left=None
        self.ai = AI(self.board, aiturn,aiskill) if ai else None
        self.aiturn = aiturn
        for i in range(90):
            self.slots.append(Slot(50 * (9 - i % 10), 50 * (i // 10)))
        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece, self))

    def did_mount(self):
        cp = cv.Canvas(
            [
                cv.Path(
                    [
                        cv.Path.MoveTo(25, 25),
                        cv.Path.LineTo(25, 475),
                        cv.Path.MoveTo(75, 25),
                        cv.Path.LineTo(75, 475),
                        cv.Path.MoveTo(125, 25),
                        cv.Path.LineTo(125, 475),
                        cv.Path.MoveTo(175, 25),
                        cv.Path.LineTo(175, 475),
                        cv.Path.MoveTo(225, 25),
                        cv.Path.LineTo(225, 475),
                        cv.Path.MoveTo(275, 25),
                        cv.Path.LineTo(275, 475),
                        cv.Path.MoveTo(325, 25),
                        cv.Path.LineTo(325, 475),
                        cv.Path.MoveTo(375, 25),
                        cv.Path.LineTo(375, 475),
                        cv.Path.MoveTo(425, 25),
                        cv.Path.LineTo(425, 475),
                        cv.Path.MoveTo(25, 25),
                        cv.Path.LineTo(425, 25),
                        cv.Path.MoveTo(25, 75),
                        cv.Path.LineTo(425, 75),
                        cv.Path.MoveTo(25, 125),
                        cv.Path.LineTo(425, 125),
                        cv.Path.MoveTo(25, 175),
                        cv.Path.LineTo(425, 175),
                        cv.Path.MoveTo(25, 225),
                        cv.Path.LineTo(425, 225),
                        cv.Path.MoveTo(25, 275),
                        cv.Path.LineTo(425, 275),
                        cv.Path.MoveTo(25, 325),
                        cv.Path.LineTo(425, 325),
                        cv.Path.MoveTo(25, 375),
                        cv.Path.LineTo(425, 375),
                        cv.Path.MoveTo(25, 425),
                        cv.Path.LineTo(425, 425),
                        cv.Path.MoveTo(25, 475),
                        cv.Path.LineTo(425, 475),
                        cv.Path.MoveTo(175, 25),
                        cv.Path.LineTo(275, 125),
                        cv.Path.MoveTo(275, 25),
                        cv.Path.LineTo(175, 125),
                        cv.Path.MoveTo(175, 375),
                        cv.Path.LineTo(275, 475),
                        cv.Path.MoveTo(275, 375),
                        cv.Path.LineTo(175, 475),
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
        self.controls.extend(self.slots)
        self.controls.extend(self.piecelist)
        self.controls.extend(self.moved)
        self.update()
        return super().did_mount()
    
    def update(self,movingPiece=None,add=None):
        cp = cv.Canvas(
            [
                cv.Path(
                    [
                        cv.Path.MoveTo(25, 25),
                        cv.Path.LineTo(25, 475),
                        cv.Path.MoveTo(75, 25),
                        cv.Path.LineTo(75, 475),
                        cv.Path.MoveTo(125, 25),
                        cv.Path.LineTo(125, 475),
                        cv.Path.MoveTo(175, 25),
                        cv.Path.LineTo(175, 475),
                        cv.Path.MoveTo(225, 25),
                        cv.Path.LineTo(225, 475),
                        cv.Path.MoveTo(275, 25),
                        cv.Path.LineTo(275, 475),
                        cv.Path.MoveTo(325, 25),
                        cv.Path.LineTo(325, 475),
                        cv.Path.MoveTo(375, 25),
                        cv.Path.LineTo(375, 475),
                        cv.Path.MoveTo(425, 25),
                        cv.Path.LineTo(425, 475),
                        cv.Path.MoveTo(25, 25),
                        cv.Path.LineTo(425, 25),
                        cv.Path.MoveTo(25, 75),
                        cv.Path.LineTo(425, 75),
                        cv.Path.MoveTo(25, 125),
                        cv.Path.LineTo(425, 125),
                        cv.Path.MoveTo(25, 175),
                        cv.Path.LineTo(425, 175),
                        cv.Path.MoveTo(25, 225),
                        cv.Path.LineTo(425, 225),
                        cv.Path.MoveTo(25, 275),
                        cv.Path.LineTo(425, 275),
                        cv.Path.MoveTo(25, 325),
                        cv.Path.LineTo(425, 325),
                        cv.Path.MoveTo(25, 375),
                        cv.Path.LineTo(425, 375),
                        cv.Path.MoveTo(25, 425),
                        cv.Path.LineTo(425, 425),
                        cv.Path.MoveTo(25, 475),
                        cv.Path.LineTo(425, 475),
                        cv.Path.MoveTo(175, 25),
                        cv.Path.LineTo(275, 125),
                        cv.Path.MoveTo(275, 25),
                        cv.Path.LineTo(175, 125),
                        cv.Path.MoveTo(175, 375),
                        cv.Path.LineTo(275, 475),
                        cv.Path.MoveTo(275, 375),
                        cv.Path.LineTo(175, 475),
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
        self.controls.extend(self.slots)
        self.piecelist = []
        for color in range(2):
            for piece in self.board.pieces[color]:
                if movingPiece is not None and piece==movingPiece.piece:
                    pass
                else:
                    self.piecelist.append(janggiPiece(piece, self))
        self.controls.extend(self.piecelist)
        if movingPiece is not None:
            self.piecelist.append(movingPiece.piece)
            self.controls.append(movingPiece)
        self.controls.extend(self.ablelist)
        self.controls.extend(self.moved)
        if add is not None:
            self.controls.append(add)
        
        super().update()

    def skipTurn(self, e) -> bool:
            if self.ai and (self.aiturn==self.board.turn):
                dlg=ft.AlertDialog(
                    title=ft.Text(
                        "AI턴에는 수를 쉴 수 없습니다"
                    )
                )
                dlg.open=True
                self.controls.append(dlg)
                self.update()
                return False
            trymove = self.board.move(0, 0)
            if trymove:
                if trymove == -1:
                    self.gameOver(self.board.isGameOver(self.board.turn))
                self.moved=[]
                self.update()
                if self.ai:
                    m = self.ai.getMove()
                    move = janggibase.Piece.UCIToMove(m)
                    trymove = self.board.move(*move)
                    piece = self.slots[move[0]].ontop
                    self.moved.append(
                        ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                                     opacity=0.2,
                                     width=50,
                                     height=50,
                                     left=piece.slot.left,
                                     top=piece.slot.top))

                    self.moved.append(
                        ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                                     opacity=0.2,
                                     width=50,
                                     height=50,
                                     left=self.slots[move[1]].left,
                                     top=self.slots[move[1]].top))
                    place(piece,self.slots[move[1]])
                    piece.update()
                    if trymove == -1:
                        self.gameOver(self.board.isGameOver(self.board.turn))
                return True
            else:
                dlg=ft.AlertDialog(
                    title=ft.Text(
                        "장군일 때는 수를 쉴 수 없습니다"
                    )
                )
                dlg.open=True
                self.controls.append(dlg)
                self.update()
                return False

    def resign(self, e):
        if (not self.ai) or self.aiturn != self.board.turn and not self.board.gameOver:
            tryresign = self.board.resign()
            if tryresign:
                self.gameOver(tryresign)

    def gameOver(self, result):
        dlg = ft.AlertDialog(
            title=ft.Text(
                result,
                size=50,
                color=ft.colors.GREEN
                if result[0] == "초"
                else ft.colors.RED
                if result[0] == "한"
                else ft.colors.GREY,
            )
        )
        dlg.open = True
        self.update(add=dlg)
        if self.ai:
            if self.aiturn:
                db.add_game(
                    "USER",
                    "AI",
                    (len(self.board.gameRecord) + 1) // 2,
                    result,
                    self.board.variant,
                    " ".join(self.board.gameRecord),
                )
            else:
                db.add_game(
                    "AI",
                    "USER",
                    (len(self.board.gameRecord) + 1) // 2,
                    result,
                    self.board.variant,
                    " ".join(self.board.gameRecord),
                )
        else:
            db.add_game(
                "USER",
                "USER",
                (len(self.board.gameRecord) + 1) // 2,
                result,
                self.board.variant,
                " ".join(self.board.gameRecord),
            )

    def AI_firstmove(self):
        m = self.ai.getFirstMove()
        move = janggibase.Piece.UCIToMove(m)
        self.board.move(*move)
        piece = self.slots[move[0]].ontop
        self.moved=[]
        self.moved.append(
            ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                         opacity=0.2,
                         width=50,
                         height=50,
                         left=piece.slot.left,
                         top=piece.slot.top))
        
        self.moved.append(
            ft.Container(bgcolor=ft.colors.LIGHT_BLUE,
                         opacity=0.2,
                         width=50,
                         height=50,
                         left=self.slots[move[1]].left,
                         top=self.slots[move[1]].top))
        place(piece,self.slots[move[1]])
    

if __name__ == "__main__":

    def main(page):
        page.add(janggiBoard(janggibase.Board(15)))

    ft.app(target=main)