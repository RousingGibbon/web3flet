import logging

logger = logging.getLogger('uniswap_arbitrage')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('uniswap_arbitrage.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
