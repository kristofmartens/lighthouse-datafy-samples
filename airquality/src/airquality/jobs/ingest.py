from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

from airquality.jobs import entrypoint
from airquality.common.spark import transform, SparkLogger
from airquality.transformations.shared import add_ds, filter_by_country

DataFrame.transform = transform


@entrypoint("ingest")
def run(spark: SparkSession, environment: str, date: str):
    """Main ETL script definition.

    :return: None
    """
    # execute ETL pipeline
    logger = SparkLogger(spark)
    logger.info(f"Executing job for {environment} on {date}")
    data = extract_data(spark, date)
    transformed = transform_data(data, date)
    load_data(spark, transformed, date)


def extract_data(spark: SparkSession, date: str) -> DataFrame:
    """Load data from a source

    :param spark: Spark session object.
    :param date: The execution date as a string
    :return: Spark DataFrame.
    """
    return spark.read.json(f"s3://openaq-fetches/realtime-gzipped/{date}")


def transform_data(data: DataFrame, date: str) -> DataFrame:
    """Transform original dataset.

    :param data: Input DataFrame.
    :param date: The context date
    :return: Transformed DataFrame.
    """
    return data


def load_data(spark: SparkSession, data: DataFrame, date: str, path='s3a://datafy-training/airquality/raw'):
    """Writes the output dataset to some destination

    :param spark: the spark session
    :param environment: the environment
    :param data: DataFrame to write.
    :param database: The hive database to use.
    :param database: The path to write to.
    :return: None
    """
    (
        data.coalesce(1)
            .write
            .mode("overwrite")
            .format("json")
            .save(path=f"{path}/{date}")
    )
