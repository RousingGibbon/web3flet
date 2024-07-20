import flet as ft
from flet import Container


class Settings(Container):
    def __init__(self):
        super().__init__()
        self.enter_field = ft.TextField(hint_text="example hint", )
        self.enter_field_text = ft.Text(value="example -", text_align=ft.TextAlign.START)
        self.enter_box = ft.Row(controls=[self.enter_field_text, self.enter_field], alignment=ft.MainAxisAlignment.START)
        self.set0 = ft.ExpansionTile(
           title=ft.Text("web3ex"),
           affinity=ft.TileAffinity.PLATFORM,
           initially_expanded=False,
           collapsed_text_color=ft.colors.WHITE,
           text_color=ft.colors.WHITE,
           controls=[
               self.enter_box,
               ft.ListTile(title=ft.Text("This is sub-tile number 4")),
               ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        )
        self.set1 = ft.ExpansionTile(
            title=ft.Text("web3"),
            affinity=ft.TileAffinity.PLATFORM,
            initially_expanded=False,
            collapsed_text_color=ft.colors.WHITE,
            text_color=ft.colors.WHITE,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        )

        self.set2 = ft.ExpansionTile(
            title=ft.Text("settings"),
            affinity=ft.TileAffinity.PLATFORM,
            initially_expanded=False,
            collapsed_text_color=ft.colors.WHITE,
            text_color=ft.colors.WHITE,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        )

        self.set3 = ft.ExpansionTile(
            title=ft.Text("General"),
            affinity=ft.TileAffinity.PLATFORM,
            initially_expanded=False,
            collapsed_text_color=ft.colors.WHITE,
            text_color=ft.colors.WHITE,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        )

        self.settings_list = ft.Column(controls=[self.set0, self.set1, self.set2, self.set3],
                                       scroll=ft.ScrollMode.ALWAYS, expand=True)

        self.content = self.settings_list
        self.visible = False
        self.expand = True
