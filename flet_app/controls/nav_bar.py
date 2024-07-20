import flet as ft
from flet import NavigationBar


class Navigation(NavigationBar):
    def __init__(self):
        super().__init__()
        self.destinations = [
            ft.NavigationDestination(icon=ft.icons.API_OUTLINED, selected_icon=ft.icons.API_ROUNDED, label="Главная"),
            ft.NavigationDestination(icon=ft.icons.KEYBOARD_HIDE, label="Картинки"),
            ft.NavigationDestination(icon=ft.icons.MESSENGER_OUTLINE_SHARP, selected_icon=ft.icons.MESSENGER,
                                     label="К чатам"),
        ]
        self.border = ft.Border(top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0))
        self.animation_duration = 1000
        self.selected_index = 0
