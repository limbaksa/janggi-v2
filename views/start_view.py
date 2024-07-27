import flet as ft
from flet_route import Params, Basket


def start_view(page, params, basket):
    return ft.View(
        "/",
        [
            ft.Image(
                src="img/K1.png",
                width=300,
                height=300,
                fit=ft.ImageFit.FILL,
            ),
            ft.Column(
                controls=[
                    ft.Text("장기닷컴", size=60),
                    ft.ElevatedButton(
                        "혼자 두기", on_click=lambda _: page.go("/self"), width=300
                    ),
                    ft.ElevatedButton(
                        "AI와 두기", on_click=lambda _: page.go("/ai"), width=300
                    ),
                    ft.ElevatedButton(
                        "대국 기록 보기", on_click=lambda _: page.go("/record/0"), width=300
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
