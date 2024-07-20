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
            ft.DataColumn(ft.Text('Available pools')),
            ft.DataColumn(ft.Text('Contract Address')),
            ft.DataColumn(ft.Text('Price')),
            ft.DataColumn(ft.Text('Volume')),
        ]
        self.rows = []

        self.page.run_thread(self.run_async, self.setup())

    @staticmethod
    def run_async(coroutine):
        asyncio.run(coroutine)

    @staticmethod
    def format_liquidity(amount: float) -> str:
        """
        Reference to humanizer. Converts float into more readable format.

        Args:
            amount (float): Сумма в USD.

        Returns:
            str: Отформатированная сумма.
        """
        if amount >= 1_000_000_000:
            return f"{amount / 1_000_000_000:.1f}B USD"
        elif amount >= 1_000_000:
            return f"{amount / 1_000_000:.1f}M USD"
        elif amount >= 1_000:
            return f"{amount / 1_000:.1f}k USD"
        else:
            return f"{amount:.2f} USD"

    async def setup(self):
        for token0, token1 in TokenAddresses.unique_pairs():
            token0_address = TokenAddresses.addresses[token0]
            token1_address = TokenAddresses.addresses[token1]
            pair_address = await self.uniswap_conn.get_pair_address(token0_address, token1_address)
            token0_name, token0_symbol = await self.uniswap_conn.get_symbols(token0_address)
            token1_name, token1_symbol = await self.uniswap_conn.get_symbols(token1_address)
            price0_in_1 = await self.uniswap_conn.get_token_price(token0_address, token1_address)
            price1_in_0 = await self.uniswap_conn.get_token_price(token1_address, token0_address)
            liquidity = await self.uniswap_conn.get_liquidity_in_usd(token1_address, token0_address)

            self.rows.extend([
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{token0_symbol}/{token1_symbol}")),
                        ft.DataCell(ft.Text(f"{pair_address}")),
                        ft.DataCell(ft.Text(f"{price0_in_1}")),
                        ft.DataCell(ft.Text(f"{self.format_liquidity(liquidity)}"))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{token1_symbol}/{token0_symbol}")),
                        ft.DataCell(ft.Text(f"{pair_address}")),
                        ft.DataCell(ft.Text(f"{price1_in_0}")),
                        ft.DataCell(ft.Text(f"{self.format_liquidity(liquidity)}"))
                    ]
                ),
            ])
            self.update()


class PoolContainer(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.content = ft.ListView(controls=[Data(page)], auto_scroll=False)
        self.visible = False
        self.expand = True
