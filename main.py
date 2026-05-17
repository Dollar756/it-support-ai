import flet as ft

def main(page: ft.Page):
    page.title = "IT Support AI"

    page.add(
        ft.Text("Hola Jose 👋")
    )

ft.app(target=main)