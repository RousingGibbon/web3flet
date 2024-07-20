import flet as ft
from flet import AppBar
import asyncio


class _AppBar(AppBar):
    def __init__(self):
        super().__init__()
        self.title = ft.Text("web3App")
        self.theme_mode_button = ft.IconButton(ft.icons.SUNNY)
        self.change_scheme_button = ft.IconButton(ft.icons.COLORIZE, )
        self.theme_button = ft.Row([self.theme_mode_button, self.change_scheme_button],
             vertical_alignment=ft.CrossAxisAlignment.END,
             alignment=ft.MainAxisAlignment.END)

        self.settings_button = ft.IconButton(icon=ft.icons.SETTINGS)
        self.actions = [self.theme_button, self.settings_button]
        self.leading = ft.IconButton(icon=ft.icons.QUESTION_MARK)
        self.visible = True




        