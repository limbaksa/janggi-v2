import flet as ft
from flet_route import Params, Basket
import sys

sys.path.append("..")
from db import db
from replayBoard import replayBoard
from eval import get_eval


class play_record:
    def __init__(self):
        self.eval_values = {}

    def view(self, page: ft.Page, params: Params, basket: Basket):
        if not int(params.id):

            def nav_change(e):
                page.go(
                    "/ai"
                    if e.control.selected_index == 1
                    else "/record/0"
                    if e.control.selected_index == 2
                    else "/self"
                )

            def open_record(e):
                page.go(f"/record/{e.control.data}")

            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("대국 번호")),
                    ft.DataColumn(ft.Text("초")),
                    ft.DataColumn(ft.Text("한")),
                    ft.DataColumn(ft.Text("수"), numeric=True),
                    ft.DataColumn(ft.Text("결과")),
                    ft.DataColumn(ft.Text("복기하기")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"{i}")),
                            ft.DataCell(ft.Text(f"{db.get_cho(i)}")),
                            ft.DataCell(ft.Text(f"{db.get_han(i)}")),
                            ft.DataCell(ft.Text(f"{db.get_moves(i)}")),
                            ft.DataCell(ft.Text(f"{db.get_result(i)}")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
                                    data=i,
                                    on_click=open_record,
                                )
                            ),
                        ]
                    )
                    for i in range(1, db.game_count() + 1)
                ],
            )

            lv = ft.ListView(expand=1, spacing=10, padding=20)
            lv.controls.append(table)
            return ft.View(
                f"/record/{params.id}",
                controls=[
                    ft.Row(
                        [
                            ft.NavigationRail(
                                selected_index=None,
                                label_type=ft.NavigationRailLabelType.ALL,
                                on_change=nav_change,
                                expand=False,
                                min_width=80,
                                min_extended_width=400,
                                group_alignment=-1,
                                destinations=[
                                    ft.NavigationRailDestination(
                                        icon=ft.icons.PLAY_ARROW,
                                        selected_icon=ft.icons.PLAY_ARROW_OUTLINED,
                                        label="혼자 두기",
                                    ),
                                    ft.NavigationRailDestination(
                                        icon_content=ft.Icon(ft.icons.ADB),
                                        selected_icon_content=ft.Icon(
                                            ft.icons.ADB_OUTLINED
                                        ),
                                        label="AI와 두기",
                                    ),
                                    ft.NavigationRailDestination(
                                        icon=ft.icons.LIST,
                                        selected_icon_content=ft.Icon(
                                            ft.icons.LIST_OUTLINED
                                        ),
                                        label_content=ft.Text("대국 목록 보기",size=10),
                                    ),
                                ],
                            ),
                            ft.VerticalDivider(width=1),
                            lv,
                        ],
                        expand=True,
                    )
                ],
            )
        else:

            def nav_change(e):
                page.go(
                    "/ai"
                    if e.control.selected_index == 1
                    else "/record/0"
                    if e.control.selected_index == 2
                    else "/self"
                )

            def set_move(e):
                if e.control.data < len(board.moveNotation)-1:
                    board.set_move(e.control.data)
                elif e.control.data==len(board.moveNotation)-1:
                    board.set_move(e.control.data-1)

            def reset_move(e):
                board.set_move(-1)

            def eval(e):
                dlg = ft.AlertDialog(modal=True, title=ft.Text("분석중입니다..", size=40))
                dlg.open = True
                board.controls.append(dlg)
                board.update()
                eval_list = []
                for i in range(1, len(board.fenRecord)):
                    eval_list.append(get_eval(board.fenRecord[i]))
                self.eval_values[params.id] = eval_list
                dlg.open = False
                board.controls.remove(dlg)
                page.go(f"/re/record{params.id}")

            board = replayBoard(*db.get_record(int(params.id)))
            next_move = ft.ElevatedButton(content=ft.Text("다음 수",size=10), on_click=board.move)
            prev_move = ft.ElevatedButton(
                content=ft.Text("이전 수",size=10), on_click=board.undo_move
            )
            reset = ft.ElevatedButton(content=ft.Text("수 초기화",size=10), on_click=reset_move)
            eval_all = ft.ElevatedButton(content=ft.Text("분석하기",size=10), on_click=eval)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Container(content=ft.Text("초",size=12),width=40)),
                    ft.DataColumn(ft.Container(content=ft.Text("분석치",size=12),width=40)),
                    ft.DataColumn(ft.Container(content=ft.Text("한",size=12),width=40)),
                    ft.DataColumn(ft.Container(content=ft.Text("분석치",size=12),width=40)),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(content=ft.Text(f"{board.moveNotation[2*i]}",size=12),width=40),
                                data=2 * i,
                                on_tap=set_move,
                            ),
                            ft.DataCell(
                                ft.Container(content=ft.Text(
                                    f"{self.eval_values[params.id][2*i] if (params.id in self.eval_values and 2*i<len(board.moveNotation)-1) else '-'}",size=12
                                ),width=40)
                            ),
                            ft.DataCell(
                                ft.Container(content=ft.Text(
                                    f"{'-' if 2*i+1>=len(board.moveNotation) else board.moveNotation[2*i+1]}",size=12
                                ),width=40),
                                data=2 * i + 1,
                                on_tap=set_move,
                            ),
                            ft.DataCell(
                                ft.Container(content=ft.Text(
                                    f"{self.eval_values[params.id][2*i+1] if (params.id in self.eval_values and 2*i+1<len(board.moveNotation)-1) else '-'}",size=12
                                ),width=40)
                            ),
                        ]
                    )
                    for i in range((len(board.moveNotation) + 1) // 2)
                ],
                border_radius=0
            )

            lv = ft.ListView(expand=1, spacing=8, padding=0)
            lv.controls.append(table)
            return ft.View(
                f"/record/{params.id}",
                controls=[
                    ft.Row(
                        [
                            ft.NavigationRail(
                                selected_index=None,
                                label_type=ft.NavigationRailLabelType.ALL,
                                on_change=nav_change,
                                expand=False,
                                min_width=80,
                                min_extended_width=400,
                                group_alignment=-1,
                                destinations=[
                                    ft.NavigationRailDestination(
                                        icon=ft.icons.PLAY_ARROW,
                                        selected_icon=ft.icons.PLAY_ARROW_OUTLINED,
                                        label="혼자 두기",
                                    ),
                                    ft.NavigationRailDestination(
                                        icon_content=ft.Icon(ft.icons.ADB),
                                        selected_icon_content=ft.Icon(
                                            ft.icons.ADB_OUTLINED
                                        ),
                                        label="AI와 두기",
                                    ),
                                    ft.NavigationRailDestination(
                                        icon=ft.icons.LIST,
                                        selected_icon_content=ft.Icon(
                                            ft.icons.LIST_OUTLINED
                                        ),
                                        label_content=ft.Text("대국 목록 보기",size=10),
                                    ),
                                ],
                            ),
                            ft.VerticalDivider(width=1),
                            board,
                            ft.Column(
                                controls=[next_move, prev_move, reset, eval_all],
                                alignment=ft.MainAxisAlignment.CENTER,
                                height=500,
                            ),
                            ft.VerticalDivider(width=1),
                            ft.Container(content=lv,width=400),
                        ],
                        expand=True,
                    )
                ],
            )
