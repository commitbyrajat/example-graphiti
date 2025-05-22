import asyncio
import logging
from logging import INFO

from dotenv import load_dotenv

from src.example_graphiti.connection import Connection
from src.example_graphiti.example_cart import ExampleCart
from src.example_graphiti.example_strategy import ExampleStrategy

logging.basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

load_dotenv()


async def main():
    cart = ExampleCart()

    conn = Connection()
    execute = cart.strategy_map.get(ExampleStrategy.from_string("quickstart"))
    await execute(conn)


if __name__ == "__main__":
    asyncio.run(main())
