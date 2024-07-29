import flet as ft
from flet_route import Params, Basket
import sys

sys.path.append("..")
from janggiBoard import janggiBoard
from janggibase import Board


class self_play:
    def __init__(self):
        self.board = None
        self.variant = -1

    def view(self, page: ft.Page, params: Params, basket: Basket):
        if self.board is not None:

            def nav_change(e):
                page.go(
                    "/ai"
                    if e.control.selected_index == 1
                    else "/record/0"
                    if e.control.selected_index == 2
                    else "/self"
                )

            def reset(e):
                self.board = None
                self.variant = -1
                page.go("/re/self")
                page.update()

            reset_button = ft.ElevatedButton(content=ft.Text("대국 초기화"), on_click=reset)
            turn_skip_button = ft.ElevatedButton(
                content=ft.Text("한 수 쉼"), on_click=self.board.skipTurn
            )
            resign_button = ft.ElevatedButton(
                content=ft.Text("기권"), on_click=self.board.resign
            )
            return ft.View(
                "/self",
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
                            self.board,
                            ft.Column(
                                controls=[
                                    turn_skip_button,
                                    resign_button,
                                    reset_button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                height=500,
                            ),
                            ft.VerticalDivider(width=1),
                        ],
                        expand=True,
                    )
                ],
            )
        else:
            if self.variant == -1:
                self.variant = 0

                def nav_change(e):
                    page.go(
                        "/ai"
                        if e.control.selected_index == 1
                        else "/record/0"
                        if e.control.selected_index == 2
                        else "/self"
                    )

                def set_variant_0_1(e):
                    dlg.open = False
                    page.update()

                def set_variant_0_2(e):
                    dlg2.open = False
                    page.update()

                def set_variant_1(e):
                    dlg2.open = False
                    page.update()
                    self.variant += 1

                def set_variant_2(e):
                    dlg2.open = False
                    page.update()
                    self.variant += 2

                def set_variant_3(e):
                    dlg2.open = False
                    page.update()
                    self.variant += 3

                def set_variant_4(e):
                    dlg.open = False
                    page.update()
                    self.variant += 4

                def set_variant_8(e):
                    dlg.open = False
                    page.update()
                    self.variant += 8

                def set_variant_12(e):
                    dlg.open = False
                    page.update()
                    self.variant += 12

                dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("초 상차림 선택"),
                    actions=[
                        ft.TextButton("상마상마", on_click=set_variant_0_1),
                        ft.TextButton("마상상마", on_click=set_variant_4),
                        ft.TextButton("상마마상", on_click=set_variant_8),
                        ft.TextButton("마상마상", on_click=set_variant_12),
                    ],
                )
                dlg.open = True
                dlg2 = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("한 상차림 선택"),
                    actions=[
                        ft.TextButton("상마상마", on_click=set_variant_3),
                        ft.TextButton("마상상마", on_click=set_variant_1),
                        ft.TextButton("상마마상", on_click=set_variant_2),
                        ft.TextButton("마상마상", on_click=set_variant_0_2),
                    ],
                )
                dlg2.open = True

                def reload_page(e):
                    page.go("/re/self")
                    page.update()

                return ft.View(
                    "/self",
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
                                dlg2,
                                dlg,
                                ft.Column(
                                    [
                                        ft.ElevatedButton(
                                            text="대국 시작",
                                            on_click=reload_page,
                                            width=400,
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    width=900,
                                ),
                            ],
                            expand=True,
                        )
                    ],
                )
            else:
                self.board = janggiBoard(Board(self.variant))

                def nav_change(e):
                    page.go(
                        "/ai"
                        if e.control.selected_index == 1
                        else "/record/0"
                        if e.control.selected_index == 2
                        else "/self"
                    )

                def reset(e):
                    self.board = None
                    self.variant = -1
                    page.go("/re/self")
                    page.update()

                reset_button = ft.ElevatedButton(
                    content=ft.Text("대국 초기화"), on_click=reset
                )
                turn_skip_button = ft.ElevatedButton(
                    content=ft.Text("한 수 쉼"), on_click=self.board.skipTurn
                )
                resign_button = ft.ElevatedButton(
                    content=ft.Text("기권"), on_click=self.board.resign
                )
                return ft.View(
                    "/self",
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
                                self.board,
                                ft.Column(
                                    controls=[
                                        turn_skip_button,
                                        resign_button,
                                        reset_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    height=500,
                                ),
                                ft.VerticalDivider(width=1),
                            ],
                            expand=True,
                        )
                    ],
                )
