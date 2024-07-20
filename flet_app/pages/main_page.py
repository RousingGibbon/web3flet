import flet as ft
from flet_app.controls.settings_container import Settings
import asyncio
from flet_app.controls.main_controls import Swapper
from flet_app.controls.app_bar import _AppBar
from flet_app.controls.nav_bar import _NavigationBar
from flet_app.utils.navigate import navigate
from flet_app.controls.pool_table import PoolContainer
from flet_app.controls.arbitage import ArbitrageContainer


async def MainView(page : ft.Page):

    def run_async_task(coro):
        """Run an async task"""
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(coro)
            return task
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)

    async def init():
        settings_container = Settings()
        main_container = Swapper(page)
        app_bar = _AppBar()
        navigation_bar = _NavigationBar()
        pool_container = PoolContainer(page)
        arbitrage_container = ArbitrageContainer(page)
        return settings_container, main_container, app_bar, navigation_bar, pool_container, arbitrage_container

    settings_container, main_container, app_bar, navigation_bar, pool_container, arbitrage_container = await init()

    app_bar.settings_button.on_click = lambda e: run_async_task(coro=navigate(page, navigation_bar, main_container,
                                                                settings_container, pool_container, arbitrage_container, e=3))
    navigation_bar.on_change = lambda e: run_async_task(coro=navigate(page, navigation_bar, main_container,
                                                                settings_container, pool_container, arbitrage_container, e=e))

    page.add(main_container, settings_container)
    main_view = ft.View(
        "/main",
        [app_bar, main_container, navigation_bar, settings_container,pool_container, arbitrage_container],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )

    return main_view
