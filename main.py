import os

import flet as ft
from dotenv import load_dotenv
from openai import OpenAI

# CARGAR VARIABLES
load_dotenv()

# CLIENTE GROQ
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def main(page: ft.Page):

    page.title = "IT Support AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    page.window_width = 500
    page.window_height = 700
    page.padding = 15

    # CHAT
    chat = ft.Column(
        expand=True,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # INPUT
    user_input = ft.TextField(
        hint_text="Describe tu problema técnico...",
        border_radius=15,
        expand=True,
        filled=True,
    )

    # CREAR MENSAJE
    def create_message(text, is_user=False):

        return ft.Row(
            alignment=(
                ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
            ),
            controls=[
                ft.Container(
                    content=ft.Text(
                        text,
                        color="white",
                        size=15,
                    ),
                    bgcolor=("#0078ff" if is_user else "#2b2b2b"),
                    padding=15,
                    border_radius=15,
                    width=320,
                )
            ],
        )

    # ENVIAR MENSAJE
    def send_message(e):

        if user_input.value.strip() == "":
            return

        user_text = user_input.value

        # MENSAJE USUARIO
        chat.controls.append(create_message(user_text, True))

        page.update()

        try:

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": ("Eres un asistente profesional " "de soporte TI."),
                    },
                    {
                        "role": "user",
                        "content": user_text,
                    },
                ],
            )

            bot_reply = completion.choices[0].message.content

        except Exception as error:

            bot_reply = f"Error IA: {error}"

        # RESPUESTA BOT
        chat.controls.append(create_message(bot_reply, False))

        user_input.value = ""

        page.update()

    # BOTON
    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color="white",
        bgcolor="#0078ff",
        on_click=send_message,
    )

    # ENTER
    user_input.on_submit = send_message

    # LAYOUT
    page.add(
        ft.Row(
            [
                ft.Icon(
                    ft.Icons.SUPPORT_AGENT,
                    color="#0078ff",
                    size=35,
                ),
                ft.Text(
                    "IT Support AI",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
            ]
        ),
        ft.Divider(),
        chat,
        ft.Row(
            [
                user_input,
                send_button,
            ]
        ),
    )


ft.run(main)
