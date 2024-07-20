from web3 import Web3
from eth_utils import to_checksum_address
import json
from logger import logger
import aiohttp
import asyncio
from typing import Any, Tuple
from web3.contract import Contract
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class TokenAddresses:
    addresses = {
        "WETH": to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'),
        "USDT": to_checksum_address('0xdAC17F958D2ee523a2206206994597C13D831ec7'),
        "USDC": to_checksum_address('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'),
        "WBTC": to_checksum_address('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'),
        "DAI":  to_checksum_address('0x6B175474E89094C44Da98b954EedeAC495271d0F')
    }


    @classmethod
    def unique_pairs(cls):
        tokens = list(cls.addresses.keys())
        seen_pairs = set()
        for token1 in tokens:
            for token2 in tokens:
                if token1 != token2:
                    pair = tuple(sorted((token1, token2)))
                    if pair not in seen_pairs:
                        seen_pairs.add(pair)
                        yield pair

    @classmethod
    def unique_triplets(cls):
        tokens = list(cls.addresses.keys())
        seen_triplets = set()

        for triplet in combinations(tokens, 3):
            # Сортируем и создаем неизменяемую комбинацию для уникальности
            sorted_triplet = tuple(sorted(triplet))
            if sorted_triplet not in seen_triplets:
                seen_triplets.add(sorted_triplet)
                yield sorted_triplet



class EthConnection:
    def __init__(self):
        self.infura_url = 'https://mainnet.infura.io/v3/edcb17ba2f524017b1192f0cad991fe5'
        self.web3 = Web3(Web3.HTTPProvider(endpoint_uri=self.infura_url))
        self.addresses = TokenAddresses.addresses

    async def check_connection(self) -> None:
        """
        Checks the connection to the Ethereum network.
        Logs an error and exits if the connection fails, logs success otherwise.
        """

        if not self.web3.is_connected():
            logger.error("Failed to connect to Ethereum network")
            exit()
        else:
            logger.info('Connection to Ethereum network success')

    async def get_gas_price(self) -> int:
        """
        Retrieves the current gas price in wei and gwei.

        Returns:
          int: Gas price in wei.
        """

        gas_price_wei = self.web3.eth.gas_price
        gas_price_gwei = self.web3.from_wei(gas_price_wei, 'gwei')
        logger.info(f'Gas price now - {gas_price_wei} wei')
        logger.info(f'Gas price now - {gas_price_gwei} gwei')
        return gas_price_wei

    async def get_current_block(self) -> int:
        """
        Retrieves the current block number.

        Returns:
           int: Current block number.
        """
        current_block = self.web3.eth.block_number
        logger.info(f'Current block id: {current_block}')
        return current_block

    async def get_chain_id(self) -> int:
        """
        Retrieves the chain ID.

        Returns:
            int: Chain ID.
        """

        chain_id = self.web3.eth.chain_id
        logger.info(f'Chain id: {chain_id}')
        return chain_id


class UniswapConn:
    def __init__(self, eth_conn: EthConnection):
        self.eth_conn = eth_conn
        self.api_key = 'D4MJ7VZY93C8CF498NZT3PSJGTJVKMHS7W'

        self.router_address = to_checksum_address('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
        self.factory_address = to_checksum_address('0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f')

        self.router_abi = None
        self.factory_abi = None
        self.erc20_abi = None

        self.uniswap_router = None
        self.uniswap_factory = None

        self.abis = {}
        self.contracts = {}
        self.pair_addresses = {}
        self.symbols = {}
        self.names = {}
        self.decimals = {}
        self.reserves = {}

    @staticmethod
    def run_async_task(coro: Any) -> asyncio.Task:
        """
        Runs an async task in the event loop.

        Args:
            coro (Any): Coroutine to run.

        Returns:
            asyncio.Task: The task created.
        """
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(coro)
            return task
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            task = loop.create_task(coro)
            return task

    async def setup(self) -> None:
        """
        Sets up the Uniswap connection by retrieving necessary ABIs and initializing contracts.
        """

        self.router_abi: json = await self.get_contract_abi(self.router_address)
        self.factory_abi: json = await self.get_contract_abi(self.factory_address)
        with open('abis/erc20.json', 'r', encoding='utf-8') as file:
            self.erc20_abi: json = json.load(file)

        self.uniswap_router: Contract = self.eth_conn.web3.eth.contract(
            address=self.router_address, abi=self.router_abi)
        self.uniswap_factory: Contract = self.eth_conn.web3.eth.contract(
            address=self.factory_address, abi=self.factory_abi)

        self.abis[self.router_address]=self.router_abi
        self.abis[self.factory_address]=self.factory_abi
        self.contracts[self.router_address]=self.uniswap_router
        self.contracts[self.factory_address]=self.uniswap_factory

    async def get_decimals(self, token_address):
        if self.decimals.get(token_address):
            return self.decimals.get(token_address)
        else:
            token_contract = await self.get_contract(token_address)
            self.decimals[token_address] = token_contract.functions.decimals().call()
            return token_contract.functions.decimals().call()

    async def get_contract_abi(self, address: str, retries: int = 6, delay: int = 10) -> json:
        """
        Retrieves the contract ABI from Etherscan.

        Args:
           address (str): The contract address.
           retries (int): Number of retries if the request fails. Default is 6.
           delay (int): Delay between retries in seconds. Default is 10.

        Returns:
           json: The contract ABI.

        Raises:
           ValueError: If no contract ABI is found or if there is an Etherscan API error.
           ConnectionError: If the request fails after the specified number of retries.
        """
        if self.abis.get(address):
            return self.abis.get(address)
        else:
            url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={self.api_key}'
            for attempt in range(retries):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data['status'] == '1':
                                self.abis[f'{address}'] = json.loads(data['result'])
                                return json.loads(data['result'])
                            elif data['status'] == '0' and data['message'] == 'No contract ABI found':
                                raise ValueError(f"No contract ABI found for address {address}")
                            else:
                                print(data)
                                print(address)
                                raise ValueError(f"Etherscan API error: {data['message']}")
                        elif response.status == 502:
                            if attempt < retries - 1:
                                await asyncio.sleep(delay)
                            else:
                                raise ConnectionError(
                                    f"Failed to fetch ABI from Etherscan after {retries} attempts: {response.status}")
                        else:
                            raise ConnectionError(f"Failed to fetch ABI from Etherscan: {response.status}")

    async def get_contract(self, token_address: str) -> Contract | None:
        """
         Retrieves the contract for a given token address.

         Args:
             token_address (str): The token contract address.

         Returns:
            Contract | None: The contract instance or None if an error occurs.
         """
        try:
            if self.contracts.get(token_address):
                return self.contracts.get(token_address)
            else:
                token_contract = self.eth_conn.web3.eth.contract(address=token_address, abi=self.erc20_abi)
                self.contracts[token_address] = token_contract
                return token_contract
        except Exception as e:
            logger.error(f"Error getting contract for {token_address}: {e}")
            return None

    async def get_pair_address(self, token0_address: str, token1_address: str) -> str | None:
        """
        Retrieves the pair address for two tokens.

        Args:
            token0_address (str): Address of token0.
            token1_address (str): Address of token1.

        Returns:
            Optional[str]: The pair address or None if an error occurs.
        """
        try:
            if self.pair_addresses.get(f'{token0_address, token1_address}'):
                return self.pair_addresses.get(f'{token0_address, token1_address}')
            else:
                pair_address = self.uniswap_factory.functions.getPair(token0_address, token1_address).call()
                self.pair_addresses[f'{token0_address, token1_address}'] = pair_address
                logger.info(f"Pair address for {token0_address} and {token1_address}: {pair_address}")
                return pair_address
        except Exception as e:
            logger.error(f"Error getting pair address for {token0_address} and {token1_address}: {e}")
            return None

    async def get_pair_contract(self, pair_address: str, pair_abi: json) -> Contract | None:
        """
        Retrieves the pair contract for a given pair address.

        Args:
            pair_address (str): The pair address.
            pair_abi (json): The ABI of the pair contract.

        Returns:
            Contract | None: The pair contract instance or None if an error occurs.
        """
        try:
            if self.contracts.get(pair_address):
                return self.contracts.get(pair_address)
            else:
                pair_contract = self.eth_conn.web3.eth.contract(address=pair_address, abi=pair_abi)
                self.contracts[f'{pair_address}'] = pair_contract
            return pair_contract
        except Exception as e:
            logger.error(f"Error getting pair contract for {pair_address}: {e}")
            return None

    async def get_reserves(self, token0_address: str, token1_address: str, pair_contract: Contract, ) -> Tuple[int | None, int | None]:
        """
        Retrieves the reserves for a pair-contract in the order of the given token addresses.

        Args:
            token0_address (str): The address of the first token.
            token1_address (str): The address of the second token.
            pair_contract (Contract): The pair contract instance.

        Returns:
            Tuple[int | None, int | None]: The reserves for token0 and token1 or None if an error occurs.
        """
        try:
            if self.reserves.get(token0_address) and self.reserves.get(token1_address):
                contract_token0_address = pair_contract.functions.token0().call()
                reserve0 = self.reserves.get(token0_address)
                reserve1 = self.reserves.get(token1_address)
                if contract_token0_address.lower() == token0_address.lower():
                    return reserve0, reserve1
                else:
                    return reserve1, reserve0
            else:

                reserves = pair_contract.functions.getReserves().call()
                reserve0 = reserves[0]
                reserve1 = reserves[1]

                # Получаем адреса токенов из контракта
                contract_token0_address = pair_contract.functions.token0().call()

                # Возвращаем резервы в порядке переданных адресов
                if contract_token0_address.lower() == token0_address.lower():
                    return reserve0, reserve1
                else:
                    return reserve1, reserve0
        except Exception as e:
            logger.error(f"Error getting reserves: {e}")
            return None, None

    async def get_symbols(self, token_address) -> Tuple[str | None, str | None]:
        """
        Fetch the name and symbol of a token given its contract.

        Args:
            token_address (str): Address of the token.

        Returns:
            Tuple[str | None, str | None]: A tuple containing the name and symbol of the token.
        """
        try:
            token_contract = await self.get_contract(token_address)
            if self.symbols.get(token_contract) and self.names.get(token_contract):
                name = self.names.get(token_contract)
                symbol = self.symbols.get(token_contract)
                return name, symbol

            name = token_contract.functions.name().call()
            symbol = token_contract.functions.symbol().call()
            self.symbols[token_contract]=symbol
            self.names[token_contract]=name

            return name, symbol
        except Exception as e:
            logger.error(f"Error getting symbols: {e}")
            return None, None

    async def get_token_price(self, token0_address: str, token1_address: str,  amount_in: float = 1) -> float | None:
        """
        Get the current price of one token in terms of another token.

        Args:
            token0_address (str): The address of the input token.
            token1_address (str): The address of the output token.
            amount_in (float): The amount of input tokens to get the price for. Default is 1 token.

        Returns:
             float | None: The price of the input tokens in terms of the output tokens.
        """
        if not token0_address or not token1_address:
            raise ValueError("Token addresses must be provided")


        pair_address = await self.get_pair_address(token0_address,token1_address)
        pair_abi = await self.get_contract_abi(pair_address)
        pair_contract = await self.get_pair_contract(pair_address, pair_abi)

        decimals0 = await self.get_decimals(token0_address)
        decimals1 = await self.get_decimals(token1_address)

        name0, symbol0 = await self.get_symbols(token0_address)
        name1, symbol1 = await self.get_symbols(token1_address)

        logger.info(f"Decimals for {name0} ({symbol0}): {decimals0}")
        logger.info(f"Decimals for {name1} ({symbol1}): {decimals1}")

        try:
            reserve0, reserve1 = await self.get_reserves(token0_address, token1_address, pair_contract)

            if reserve0 is None or reserve1 is None:
                return None

            adjusted_reserve0 = reserve0 / (10 ** decimals0)
            adjusted_reserve1 = reserve1 / (10 ** decimals1)

            logger.info(f"Adjusted reserve {name0} = {adjusted_reserve0}")
            logger.info(f"Adjusted reserve {name1} = {adjusted_reserve1}")

            amount_out_token = (float(adjusted_reserve1) / float(adjusted_reserve0)) * float(amount_in)

            logger.info(f"Price of 1 {name0} ({symbol0}) in {name1} ({symbol1}): {amount_out_token}")
            return amount_out_token
        except Exception as e:
            try:
                logger.warning(f"Direct pair contract call failed: {e}")
                amount_in_scaled = int(amount_in * (10 ** decimals0))
                path = [token0_address, token1_address]
                amounts_out = self.uniswap_router.functions.getAmountsOut(amount_in_scaled, path).call()
                amount_out = amounts_out[-1]
                amount_out_token = amount_out / (10 ** decimals1)
                logger.info(f"Price of 1 {name0} ({symbol0}) in {name1} ({symbol1}): {amount_out_token}")
                return amount_out_token

            except Exception as e:
                logger.error(f"Error getting current price: {e}")
                return None

    async def get_liquidity_in_usd(self, token0_address: str, token1_address: str) -> float | None:
        """
        Get the current liquidity volume in USD by reserves and current USD price.

        Args:
            token0_address (str): The address of the first token.
            token1_address (str): The address of the second token.

        Returns:
            float | None: The liquidity volume in USD.
        """
        usdt_address = self.eth_conn.addresses.get("USDT")

        if token0_address == usdt_address or token1_address == usdt_address:
            # Определение адреса токена, который не является USDT
            non_usdt_token_address = token1_address if token0_address == usdt_address else token0_address

            # Получение цены токена, который не является USDT, в USD
            token_price_in_usdt = await self.get_token_price(non_usdt_token_address, usdt_address)
            if token_price_in_usdt is None:
                return None

            # Получение адреса пары для токена и USDT
            pair_address = await self.get_pair_address(non_usdt_token_address, usdt_address)
            if not pair_address:
                return None

            pair_abi = await self.get_contract_abi(pair_address)
            pair_contract = await self.get_pair_contract(pair_address, pair_abi)
            if not pair_contract:
                return None

            # Получение резервов
            reserve_non_usdt_token, reserve_usdt = await self.get_reserves(non_usdt_token_address, usdt_address, pair_contract)
            if reserve_non_usdt_token is None or reserve_usdt is None:
                return None

            # Получение десятичных знаков
            non_usdt_token_decimals = await self.get_decimals(non_usdt_token_address)
            usdt_decimals = await self.get_decimals(usdt_address)

            # Преобразование резервов в реальные значения
            adjusted_reserve_non_usdt_token = float(reserve_non_usdt_token) / (10 ** non_usdt_token_decimals)
            adjusted_reserve_usdt = float(reserve_usdt) / (10 ** usdt_decimals)

            # Расчет ликвидности в USD
            liquidity_usd = (adjusted_reserve_non_usdt_token * float(token_price_in_usdt)) + (
                        adjusted_reserve_usdt * 1.0)

            logger.info(f"Adjusted reserve {non_usdt_token_address} = {adjusted_reserve_non_usdt_token}")
            logger.info(f"Price of 1 {non_usdt_token_address} in USD: {token_price_in_usdt}")
            logger.info(f"Adjusted reserve {usdt_address} = {adjusted_reserve_usdt}")
            logger.info(f"Liquidity in USD: {liquidity_usd}")

            return liquidity_usd

        # Если оба токена не USDT
        pair_address = await self.get_pair_address(token0_address, token1_address)
        if not pair_address:
            return None

        pair_abi = await self.get_contract_abi(pair_address)
        pair_contract = await self.get_pair_contract(pair_address, pair_abi)
        if not pair_contract:
            return None

        # Получение резервов
        reserve0, reserve1 = await self.get_reserves(token0_address, token1_address, pair_contract)
        if reserve0 is None or reserve1 is None:
            return None

        # Получение десятичных знаков
        decimals0 = await self.get_decimals(token0_address)
        decimals1 = await self.get_decimals(token1_address)

        # Преобразование резервов в реальные значения
        adjusted_reserve0 = float(reserve0) / (10 ** decimals0)
        adjusted_reserve1 = float(reserve1) / (10 ** decimals1)

        # Получение цен токенов
        price0 = await self.get_token_price(token0_address, token1_address)
        price1 = await self.get_token_price(token1_address, usdt_address)

        if price0 is None or price1 is None:
            return None

        # Расчет ликвидности в USD
        liquidity_usd = (adjusted_reserve0 * float(price0)) + (adjusted_reserve1 * float(price1))

        logger.info(f"Adjusted reserve {token0_address} = {adjusted_reserve0}")
        logger.info(f"Adjusted reserve {token1_address} = {adjusted_reserve1}")
        logger.info(f"Price of 1 {token0_address} in {token1_address}: {price0}")
        logger.info(f"Price of 1 {token1_address} in USD: {price1}")
        logger.info(f"Liquidity in USD: {liquidity_usd}")

        return liquidity_usd
    async def get_last_swap(self, token0_address: str, token1_address: str, pair_contract: Contract) -> float | None:

            latest_block = self.eth_conn.web3.eth.get_block('latest')['number']
            from_block = latest_block - (24 * 60 * 4)  # приблизительно 1 блок в 15 секунд

            latest_swaps = pair_contract.events.Swap().get_logs(fromBlock=from_block, toBlock='latest')
            if latest_swaps:
                # Determine which tokens are involved in the swap
                token0 = pair_contract.functions.token0().call()
                token1 = pair_contract.functions.token1().call()

                # Get decimals for tokens
                decimals0 = await self.get_decimals(token0)
                decimals1 = await self.get_decimals(token1)

                logger.info(f"Token0: {token0}, Token1: {token1}")
                logger.info(f"Decimals for Token0: {decimals0}, Decimals for Token1: {decimals1}")

                for swap in reversed(latest_swaps):
                    amount0_in = swap['args']['amount0In'] / (10 ** decimals0)
                    amount1_in = swap['args']['amount1In'] / (10 ** decimals1)
                    amount0_out = swap['args']['amount0Out'] / (10 ** decimals0)
                    amount1_out = swap['args']['amount1Out'] / (10 ** decimals1)

                    logger.info(f"Swap details - Amount0In: {amount0_in}, Amount1In: {amount1_in}")
                    logger.info(f"Swap details - Amount0Out: {amount0_out}, Amount1Out: {amount1_out}")

                    # Determine which token is token0 and which is token1
                    if to_checksum_address(token0) == to_checksum_address(token0_address):

                        if to_checksum_address(token1) == to_checksum_address(token1_address):
                            # Token0 was swapped for Token1
                            if amount0_in > 0:
                                price = amount1_out / amount0_in
                            else:
                                price = amount1_in / amount0_out
                        else:
                            # Token1 was swapped for Token0
                            if amount1_in > 0:
                                price = amount0_out / amount1_in
                            else:
                                price = amount0_in / amount1_out
                    else:
                        # Reverse case: token0 and token1 are swapped
                        if to_checksum_address(token1) == to_checksum_address(token0_address):
                            # Token1 was swapped for Token0
                            if amount1_in > 0:
                                price = amount0_out / amount1_in
                            else:
                                price = amount0_in / amount1_out
                        else:
                            # Token0 was swapped for Token1
                            if amount0_in > 0:
                                price = amount1_out / amount0_in
                            else:
                                price = amount1_in / amount0_out

                    logger.info(f"Calculated price: {price}")

                    if price is not None:
                        return price

    async def get_arbitrage_abillity(self, token0_address, token1_address, token2_address):

        token0_name, token0_symbol = await self.get_symbols(token0_address)
        token1_name, token1_symbol = await self.get_symbols(token1_address)
        token2_name, token2_symbol = await self.get_symbols(token2_address)

        print(token0_name, token1_name, token2_name)

        pair_address0_1 = await self.get_pair_address(token0_address, token1_address)
        pair_address1_2 = await self.get_pair_address(token1_address, token2_address)
        pair_address0_2 = await self.get_pair_address(token0_address, token2_address)

        pair_abi0_1 = await self.get_contract_abi(pair_address0_1)
        pair_abi1_2 = await self.get_contract_abi(pair_address1_2)
        pair_abi0_2 = await self.get_contract_abi(pair_address0_2)

        pair_contract0_1 = await self.get_pair_contract(pair_address0_1, pair_abi0_1)
        pair_contract1_2 = await self.get_pair_contract(pair_address1_2, pair_abi1_2)
        pair_contract0_2 = await self.get_pair_contract(pair_address0_2, pair_abi0_2)

        price0_in_terms_of_1 = await self.get_token_price(token0_address, token1_address)
        price1_in_terms_of_0 = await self.get_token_price(token1_address, token0_address)
        price1_in_terms_of_2 = await self.get_token_price(token1_address, token2_address)
        price2_in_terms_of_1 = await self.get_token_price(token2_address, token1_address)
        price2_in_terms_of_0 = await self.get_token_price(token2_address, token0_address)
        price0_in_terms_of_2 = await self.get_token_price(token0_address, token2_address)

        p01 = price0_in_terms_of_1
        p10 = price1_in_terms_of_0
        p12 = price1_in_terms_of_2
        p21 = price2_in_terms_of_1
        p20 = price2_in_terms_of_0
        p02 = price0_in_terms_of_2

        print(f'{token0_symbol}-{token2_symbol}, {price0_in_terms_of_2}')  # ok
        print(f'{token2_symbol}-{token0_symbol}, {price2_in_terms_of_0}')  # OK

        print(f'{token2_symbol}-{token1_symbol}, {price2_in_terms_of_1}')  # OK
        print(f'{token1_symbol}-{token2_symbol}, {price1_in_terms_of_2}')  # OK

        print(f'{token0_symbol}-{token1_symbol}, {price0_in_terms_of_1}')  # OK
        print(f'{token1_symbol}-{token0_symbol}, {price1_in_terms_of_0}')  # OK

        initial_amount_usdt = 1
        initial_amount_token0 = initial_amount_usdt * price2_in_terms_of_0
        initial_amount_token1 = initial_amount_usdt * price2_in_terms_of_1
        initial_amount_token2 = initial_amount_usdt

        price0_in_terms_of_1 = await self.get_last_swap(token0_address, token1_address, pair_contract0_1)
        price1_in_terms_of_0 = await self.get_last_swap(token1_address, token0_address, pair_contract0_1)
        price1_in_terms_of_2 = await self.get_last_swap(token1_address, token2_address, pair_contract1_2)
        price2_in_terms_of_1 = await self.get_last_swap(token2_address, token1_address, pair_contract1_2)
        price2_in_terms_of_0 = await self.get_last_swap(token2_address, token0_address, pair_contract0_2)
        price0_in_terms_of_2 = await self.get_last_swap(token0_address, token2_address, pair_contract0_2)

        result012 = (initial_amount_token0 / (
                    initial_amount_token0 * price0_in_terms_of_1 * price1_in_terms_of_2 * p20) - 1.0) * 100
        result021 = (initial_amount_token0 / (
                    initial_amount_token0 * price0_in_terms_of_2 * price2_in_terms_of_1 * p10) - 1.0) * 100
        result102 = (initial_amount_token1 / (
                    initial_amount_token1 * price1_in_terms_of_0 * price0_in_terms_of_2 * p21) - 1.0) * 100
        result120 = (initial_amount_token1 / (
                    initial_amount_token1 * price1_in_terms_of_2 * price2_in_terms_of_0 * p01) - 1.0) * 100
        result201 = (initial_amount_token2 / (
                    initial_amount_token2 * price2_in_terms_of_0 * price0_in_terms_of_1 * p12) - 1.0) * 100
        result210 = (initial_amount_token2 / (
                    initial_amount_token2 * price2_in_terms_of_1 * price1_in_terms_of_0 * p02) - 1.0) * 100

        arbitrage_routes = [
            (f"{token0_symbol} -> {token1_symbol} -> {token2_symbol}", result012),
            (f"{token0_symbol} -> {token2_symbol} -> {token1_symbol}", result021),
            (f"{token1_symbol} -> {token0_symbol} -> {token2_symbol}", result102),
            (f"{token1_symbol} -> {token2_symbol} -> {token0_symbol}", result120),
            (f"{token2_symbol} -> {token0_symbol} -> {token1_symbol}", result201),
            (f"{token2_symbol} -> {token1_symbol} -> {token0_symbol}", result210),
        ]
        result = []
        for route, profit in arbitrage_routes:
            result.append((route, profit))
            print(f"{route}, Profit: {profit}")
        return result

async def main():
    eth_conn = EthConnection()
    await eth_conn.check_connection()
    gas = await eth_conn.get_gas_price()
    await eth_conn.get_current_block()
    await eth_conn.get_chain_id()

    uniswap_conn = UniswapConn(eth_conn)
    await uniswap_conn.run_async_task(uniswap_conn.setup())

    token0_address = uniswap_conn.eth_conn.addresses.get("WBTC")
    token1_address = uniswap_conn.eth_conn.addresses.get("WETH")
    # token2_address = to_checksum_address('0xdAC17F958D2ee523a2206206994597C13D831ec7')
    #
    # token0_contract = await uniswap_conn.get_contract(token0_address)
    # token1_contract = await uniswap_conn.get_contract(token1_address)
    #
    #
    # pair_address = await uniswap_conn.get_pair_address(token0_address, token1_address)
    # pair_abi = await uniswap_conn.get_contract_abi(pair_address)
    # pair_contract = await uniswap_conn.get_pair_contract(pair_address, pair_abi)
    #
    # print(await uniswap_conn.get_token_price(token0_contract.address, token1_contract.address, 1))
    #
    # await uniswap_conn.get_arbitrage_abillity(token2_address, token1_address, token0_address)
    x = await uniswap_conn.get_liquidity_in_usd(eth_conn.addresses.get("USDT"),eth_conn.addresses.get("WBTC"))
    print(x)
if __name__ == "__main__":
    asyncio.run(main())