from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

from airquality.jobs import entrypoint
from airquality.common.spark import transform, SparkLogger
from airquality.transformations.shared import add_ds, filter_by_country

DataFrame.transform = transform


@entrypoint("sample")
def run(spark: SparkSession, environment: str, date: str):
    """Main ETL script definition.

    :return: None
    """
    # execute ETL pipeline
    logger = SparkLogger(spark)
    logger.info(f"Executing job for {environment} on {date}")
    data = extract_data(spark, date)
    transformed = transform_data(data, date)
    load_data(spark, transformed)


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
    return data.transform(add_ds(date)).transform(filter_by_country("BE"))


def load_data(spark: SparkSession, data: DataFrame, database=f"airquality", path='s3a://datafy-training/airquality/'):
    """Writes the output dataset to some destination

    :param spark: the spark session
    :param environment: the environment
    :param data: DataFrame to write.
    :param database: The hive database to use.
    :param database: The path to write to.
    :return: None
    """
    spark.catalog.setCurrentDatabase(database)
    (
        data.coalesce(1)
            .write
            .mode("overwrite")
            .format("parquet")
            .partitionBy("ds")
            .saveAsTable("airquality_pyspark", path=path)
    )
