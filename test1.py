addresses = {
    "WETH": '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    "USDT": '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    "USDC": '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    "WBTC": '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
    "DAI": '0x6B175474E89094C44Da98b954EedeAC495271d0F'
}


async def get_arbitrage_abillity():
    token0_address = to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')  # WETH
    token1_address = to_checksum_address('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599')  # WBTC
    token2_address = to_checksum_address('0xdAC17F958D2ee523a2206206994597C13D831ec7')  # USDT

    token0_address, token1_address, token2_address = await uniswap_conn.correct_addresses(token0_address,
                                                                                          token1_address,
                                                                                          token2_address)

    token0_contract = await uniswap_conn.get_contract(token0_address)
    token1_contract = await uniswap_conn.get_contract(token1_address)
    token2_contract = await uniswap_conn.get_contract(token2_address)

    pair_address0_1 = await uniswap_conn.get_pair_address(token0_address, token1_address)
    pair_address1_2 = await uniswap_conn.get_pair_address(token1_address, token2_address)
    pair_address0_2 = await uniswap_conn.get_pair_address(token0_address, token2_address)

    pair_abi0_1 = await uniswap_conn.get_contract_abi(pair_address0_1)
    pair_abi1_2 = await uniswap_conn.get_contract_abi(pair_address1_2)
    pair_abi0_2 = await uniswap_conn.get_contract_abi(pair_address0_2)

    pair_contract0_1 = await uniswap_conn.get_pair_contract(pair_address0_1, pair_abi0_1)
    pair_contract1_2 = await uniswap_conn.get_pair_contract(pair_address1_2, pair_abi1_2)
    pair_contract0_2 = await uniswap_conn.get_pair_contract(pair_address0_2, pair_abi0_2)

# await get_arbitrage_abillity()