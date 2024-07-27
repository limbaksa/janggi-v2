import flet as ft
from flet_route import Params, Basket


def reload(page, params, basket):
    if params.page == "self":
        page.go("/self")
    elif params.page == "ai":
        page.go("/ai")
    elif params.page == "record":
        page.go("/record/0")
    else:
        page.go(f"/record/{params.page[6:]}")
