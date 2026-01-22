import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase
from dynaconf import settings


def get_engine() -> Engine:
    return create_engine(str(settings.database_url))


def setup_tables(engine: Engine):
    DeclarativeBase.metadata.create_all(engine)


def check_tables_exists(engine: Engine):
    all_found = False
    connection = None
    
    try:
        tables_dicts = DeclarativeBase.metadata.tables
        tables_names_from_base = [table.name for table in tables_dicts.values()]
        connection = engine.connect()
        all_found = all(
            engine.dialect.has_table(connection=connection, table_name=t_name)
            for t_name in tables_names_from_base
        )
    except Exception as e:
        logging.error(f"Error checking tables: {e}")
        raise e
    finally:
        if connection is not None:
            connection.close()
        engine.dispose()

    return all_found


def main():
    logging.info("Creating engine")
    db_engine = get_engine()
    logging.info("Created engine")
    logging.info("*" * 10)
    logging.info("Creating tables")
    setup_tables(db_engine)

    tables_exists = check_tables_exists(db_engine)
    # Raise an error if the tables do not exist
    if not tables_exists:
        raise ValueError("Tables were not set up correctly")
    else:
        logging.info("Tables set up successful")
