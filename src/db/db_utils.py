import pandas as pd
from sqlalchemy import Engine, create_engine


def get_db_engine(db_config: dict) -> Engine:
    """Function wich get config and return engine"""
    user = db_config.get('user')
    password = db_config.get('password')
    host = db_config.get('host')
    port = db_config.get('port')
    database = db_config.get('database')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    return engine


def put_dataframe_in_posgre(df: pd.DataFrame,
                            table_name: str,
                            engine: Engine) -> None:
    """Function wich get one file and put data from file to database"""
    df.to_sql(table_name, engine, if_exists='append', index=False)
    return None
