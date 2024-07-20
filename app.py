import flet as ft
from flet import Theme
from logger import logger
from flet_app.pages.main_page import MainView
import asyncio
from main import EthConnection
from main import UniswapConn

async def main(page: ft.Page):
    eth_conn = EthConnection()
    uniswap_conn = UniswapConn(eth_conn)
    page.session.set('eth_conn',  eth_conn)
    page.session.set('uniswap_conn', uniswap_conn)
    await uniswap_conn.setup()

    async def route_change(event):
        page.views.clear()
        if page.route == "/main":
            logger.debug(page.route)
            page.views.append(await MainView(page))
        # if page.route == "/login":
        #     logger.debug(page.route)
        #     page.views.append(await LoginView(page, logger))
        page.update()

    def run_async_task(coro):
        """Run an async task"""
        try:
            asyncio.create_task(coro)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(coro)

    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    async def yes_click(e):
        logger.info('Yes click on window_destroy()')
        page.window.destroy()

    async def no_click(e):
        confirm_dialog.open = False
        logger.debug('No click on window_destroy()')
        page.update()

    async def window_event(event):
        logger.debug(event.data)
        if event.data == "close":
            page.overlay.append(confirm_dialog)
            confirm_dialog.open = True
            page.update()
        if event.data == "resized":
            print("New page size:", page.window.width, page.window.height)
            page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=lambda e: run_async_task(yes_click(e))),
            ft.OutlinedButton("No", on_click=lambda e: run_async_task(no_click(e)))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.on_route_change = route_change
    page.go("/main")
    page.fonts = {"Circular": "/fonts/circular-medium.ttf"}
    page.theme = Theme(font_family="Circular")
    page.on_view_pop = view_pop
    page.window.prevent_close = True
    page.window.on_event = window_event
    page.title = "web3 project"

    page.adaptive = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()


ft.app(target=main, assets_dir="assets")