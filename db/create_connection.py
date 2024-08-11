import logging
import psycopg2
from config_data.config import Config, load_config


logger = logging.getLogger(__name__)
config: Config = load_config()


def create_connection():
    try:
        connection = psycopg2.connect(
            database=config.database.db,
            user=config.database.user,
            password=config.database.password,
            host=config.database.host,
        )
        logger.info('Successfully connected to the database')
        return connection

    except Exception as e:
        logger.info(f'Error: {e}')
        return None
