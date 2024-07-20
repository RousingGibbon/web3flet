import flet as ft
import asyncio
from flet_app.controls.main_controls import TokenAddresses


class Data(ft.DataTable):
    def __init__(self, page):
        super().__init__(columns=[], rows=[])
        self.page = page
        self.uniswap_conn = page.session.get('uniswap_conn')
        self.addresses = TokenAddresses()
        self.columns = [
            ft.DataColumn(ft.Text('Route')),
            ft.DataColumn(ft.Text('Profit')),
        ]
        self.rows = []

        self.page.run_thread(self.run_async, self.setup())

    @staticmethod
    def run_async(coroutine):
        asyncio.run(coroutine)

    async def setup(self):
        for token0, token1, token2 in TokenAddresses.unique_triplets():
            token0_address = TokenAddresses.addresses[token0]
            token1_address = TokenAddresses.addresses[token1]
            token2_address = TokenAddresses.addresses[token2]

            results = await self.uniswap_conn.get_arbitrage_ability(token0_address, token1_address, token2_address)
            for result in results:
                route, profit = result
                self.rows.extend([
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"{route}")),
                            ft.DataCell(ft.Text(f"{profit}")),

                        ]
                    ),
                ])
                self.update()


class ArbitrageContainer(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.content = ft.ListView(controls=[Data(page)], auto_scroll=False)
        self.visible = False
        self.expand = True
