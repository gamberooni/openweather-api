import pandas as pd
import sqlalchemy
from openweather.models.base import Base
import logging

logger = logging.getLogger(__name__)


def format_multiline_dunder_str(multiline_str: str) -> str:

    """
    Formats a multiline f-string of a class __str__ method into a Pythonic format.
    """

    return ", ".join((multiline_str).replace("\n", "").replace(" ", "").split(","))


def write_df_to_sqlite(
    table_name: str, engine: sqlalchemy.engine, df: pd.DataFrame
) -> None:
    rows_written = df.to_sql(table_name, engine, if_exists="append", index=False)

    logger.info(f"Written {rows_written} row(s) to {table_name} table")


def fetch_data_and_write_to_db(
    model_instance: Base, table_name: str, engine: sqlalchemy.engine
) -> None:
    data = model_instance.get().stringify()
    data_normalized = pd.json_normalize(data, sep="_")  # flatten nested dict
    df = pd.DataFrame.from_dict(data_normalized)
    write_df_to_sqlite(table_name, engine, df)
