import flet as ft
import asyncio
from main import TokenAddresses


class Swapper(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.eth_conn = page.session.get('eth_conn')
        self.uniswap_conn = page.session.get('uniswap_conn')
        self.addresses = TokenAddresses.addresses
        self.page.snack_bar = ft.SnackBar(ft.Text('Choose currency to continue.'))
        self.tokenA = ft.Dropdown(
            width=100,
            options=[ft.dropdown.Option(key) for key in self.addresses.keys()],
            hint_text="Choose currency",
            border_radius=30,
            )
        self.tokenA_amount = ft.TextField(hint_text="Amount")
        self.tokenA_label = ft.Text('AVG price')
        self.tokenA_row = ft.Row(controls=[self.tokenA, self.tokenA_amount], alignment=ft.MainAxisAlignment.CENTER)
        self.tokenA_w = ft.Column(controls=[self.tokenA_label, self.tokenA_row])
        self.tokenB = ft.Dropdown(
            width=100,
            options=[ft.dropdown.Option(key) for key in self.addresses.keys()],
            hint_text="Choose currency",
            border_radius=30,

        )
        self.tokenB_amount = ft.TextField(hint_text="Amount")
        self.tokenB_label = ft.Text('AVG Price')
        self.tokenB_row = ft.Row(controls=[self.tokenB, self.tokenB_amount], alignment=ft.MainAxisAlignment.CENTER)
        self.tokenB_w = ft.Column(controls=[self.tokenB_label, self.tokenB_row])
        self.change = ft.IconButton(icon=ft.icons.SWAP_VERT)
        self.change_button = ft.Row(controls=[self.change], alignment=ft.MainAxisAlignment.CENTER)
        self.swap_button = ft.OutlinedButton(text="Swap", on_click=lambda e: self.run_async_task(self.swap_click(e)))
        self.swap_button.row = ft.Row(controls=[self.swap_button], alignment=ft.MainAxisAlignment.CENTER)

        self.commission = ft.Column(controls=[])
        self.content = ft.Column(
            controls=[self.tokenA_w, self.change, self.tokenB_w, self.swap_button.row, self.commission],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.run_thread(self.run_async, self.setup())

    @staticmethod
    def run_async(coroutine):
        asyncio.run(coroutine)

    @staticmethod
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

    async def setup(self):
        await self.eth_conn.check_connection()
        while True:
            eth_price = await self.uniswap_conn.get_token_price(self.addresses.get("WETH"), self.addresses.get("USDT"))
            gas_price = await self.uniswap_conn.eth_conn.get_gas_price()
            gas_price = self.eth_conn.web3.from_wei(gas_price, 'ether')
            commission = await self.uniswap_conn.get_token_price(self.addresses.get("WETH"), self.addresses.get("USDT"),
                                                                 amount_in=gas_price)
            current_block = await self.eth_conn.get_current_block()
            chain_id = await self.eth_conn.get_chain_id()
            eth_prices = ft.Text(f'ETH price: {eth_price:.2f} USD')
            gas = ft.Text(f'Current gas price: {commission:.5f} USD')
            block = ft.Text(f'Current block: {current_block}')
            chain = ft.Text(f'Chain ID: {chain_id}')
            self.commission.controls = [eth_prices, gas, block, chain]
            self.update()
            await asyncio.sleep(30)

    async def swap_click(self, e):
        if self.tokenA.value is None or self.tokenB.value is None:
            self.page.snack_bar.open = True
            self.page.update()
        else:
            await self.get_info()
            pass

        self.update()

    async def get_info(self):
        token0_address = self.addresses.get(self.tokenA.value)
        token1_address = self.addresses.get(self.tokenB.value)

        await self.uniswap_conn.get_symbols(token0_address)
        await self.uniswap_conn.get_symbols(token1_address)

        name0, symbol0 = await self.uniswap_conn.get_symbols(token0_address)
        name1, symbol1 = await self.uniswap_conn.get_symbols(token1_address)
        price01 = await self.uniswap_conn.get_token_price(token0_address, token1_address)
        price10 = await self.uniswap_conn.get_token_price(token1_address, token0_address)
        self.tokenA_label.value = f'{name0} = {price01:.6f} {name1} '
        self.tokenB_label.value = f'{name1} = {price10:.6f} {name0} '
