import asyncio
import aiohttp
import json
from logger import logger  # Assuming logger is correctly imported from your module

UNISWAP_SUBGRAPH_URL = 'https://gateway-arbitrum.network.thegraph.com/api/[api-key]/subgraphs/id/EYCKATKGBKLWvSfwvBjzfCBmGwYNdVkduYXVivCsLRFu'

async def fetch_data():
    api_key = 'd1138f093bd7e27d795289a693f3f5e9'
    url = UNISWAP_SUBGRAPH_URL.replace('[api-key]', api_key)

    query = """
    {
        uniswapFactories(first: 5) {
            id
            pairCount
            totalVolumeUSD
            totalVolumeETH
        }
        tokens(where: {symbol: "USDT"}) {
            id
            symbol :
            name
            decimals
        }
    }
    """

    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "operationName": "Subgraphs",
            "variables": {}
        }
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return data
            else:
                logger.error(f"Failed to fetch data: {response.status}")
                return None

async def main():
    data = await fetch_data()
    if data:
        logger.info("Uniswap Factories:")
        for factory in data.get('data', {}).get('uniswapFactories', []):
            logger.info(f"Factory ID: {factory['id']}, Pair Count: {factory['pairCount']}, Total Volume USD: {factory['totalVolumeUSD']}, Total Volume ETH: {factory['totalVolumeETH']}")

        logger.info("Tokens:")
        for token in data.get('data', {}).get('tokens', []):
            logger.info(f"Token ID: {token['id']}, Symbol: {token['symbol']}, Name: {token.get('name')}, Decimals: {token['decimals']}")

if __name__ == "__main__":
    asyncio.run(main())