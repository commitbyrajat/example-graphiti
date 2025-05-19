import asyncio
import logging
import os
from logging import INFO

from dotenv import load_dotenv
from graphiti_core.nodes import EpisodeType
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF

from src.example_graphiti.connection import Connection

logging.basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

load_dotenv()

async def main():
    conn = Connection()
    try:
        episodes = [
            {
                'content': 'Kamala Harris is the Attorney General of California. She was previously '
                           'the district attorney for San Francisco.',
                'type': EpisodeType.text,
                'description': 'podcast transcript',
            },
            {
                'content': 'As AG, Harris was in office from January 3, 2011 – January 3, 2017',
                'type': EpisodeType.text,
                'description': 'podcast transcript',
            },
            {
                'content': {
                    'name': 'Gavin Newsom',
                    'position': 'Governor',
                    'state': 'California',
                    'previous_role': 'Lieutenant Governor',
                    'previous_location': 'San Francisco',
                },
                'type': EpisodeType.json,
                'description': 'podcast metadata',
            },
            {
                'content': {
                    'name': 'Gavin Newsom',
                    'position': 'Governor',
                    'term_start': 'January 7, 2019',
                    'term_end': 'Present',
                },
                'type': EpisodeType.json,
                'description': 'podcast metadata',
            },
        ]

        enable_indexing = os.environ.get('ENABLE_INDEXING', 'true').lower() == 'true'

        if enable_indexing:
            await conn.add_episodes(episodes)
        else:
            print("\nIndexing is disabled.")

        print("\nSearching for: 'Who was the California Attorney General ?'")
        query = 'Who was the California Attorney General ?'
        results = await conn.hybrid_search(query)
        query = 'Who was the California Attorney General?'
        reranked_results = await conn.center_node_search(query,results)

        print(
            '\nPerforming node search using _search method with standard recipe NODE_HYBRID_SEARCH_RRF:'
        )
        node_search_config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
        node_search_config.limit = 5  # Limit to 5 results
        query = 'California Governor'
        await conn.node_search_by_recipe(query, node_search_config)

    finally:
        await conn.close()

if __name__ == '__main__':
    asyncio.run(main())