import flet as ft
from flet import AppBar


class Appbar(AppBar):
    def __init__(self, page):
        super().__init__()
        self.title = ft.Text("web3App")
        self.page = page
        self.theme_mode_button = ft.IconButton(ft.icons.SUNNY, on_click=self.toggle_theme)
        self.change_scheme_button = ft.IconButton(ft.icons.COLORIZE, )
        self.theme_button = ft.Row(
            controls=[self.theme_mode_button, self.change_scheme_button],
            vertical_alignment=ft.CrossAxisAlignment.END,
            alignment=ft.MainAxisAlignment.END
        )
        self.settings_button = ft.IconButton(icon=ft.icons.SETTINGS)
        self.actions = [self.theme_button, self.settings_button]
        self.leading = ft.IconButton(icon=ft.icons.QUESTION_MARK)
        self.visible = True

    def toggle_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.update()