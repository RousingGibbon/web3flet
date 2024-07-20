import flet as ft
from flet import Container


class Settings(Container):
    def __init__(self):
        super().__init__()
        self.Enter_BOT_Names_Field = ft.TextField(hint_text="Введите имена ботов через запятую", )
        self.enter_field = ft.Text(value="Имя бота -", text_align=ft.TextAlign.START)
        self.enter_box = ft.Row(controls=[self.enter_field, self.Enter_BOT_Names_Field], alignment=ft.MainAxisAlignment.START)
        self.telegram_settings = ft.ExpansionTile(
           title=ft.Text("Настройки TelegramBOT"),
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
        self.discord_settings = ft.ExpansionTile(
            title=ft.Text("Настройки DiscordBOT"),
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

        self.vk_settings = ft.ExpansionTile(
            title=ft.Text("Настройки VKBOT"),
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

        self.general_settings = ft.ExpansionTile(
            title=ft.Text("Общие настройки"),
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

        self.settings_list = ft.Column(controls=[self.telegram_settings, self.discord_settings, self.vk_settings, self.general_settings],
                              scroll=ft.ScrollMode.ALWAYS, expand=True)

        self.content = self.settings_list
        self.visible = False
        self.expand = True
