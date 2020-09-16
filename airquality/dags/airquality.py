from airflow import DAG
from airflow.operators.datafy_spark_plugin import DatafySparkSubmitOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "Datafy",
    "depends_on_past": False,
    "start_date": datetime(year=2020, month=9, day=15),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


image = "{{ macros.image('airquality') }}"
role = "datafy-dp-{{ macros.env() }}/eks-job-role-samples-{{ macros.env() }}"

dag = DAG(
    "airquality", default_args=default_args, schedule_interval="@daily", max_active_runs=1
)

executor_memory = "1G"
sample_task = DatafySparkSubmitOperator(
    dag=dag,
    task_id="sample",
    num_executors="1",
    executor_memory=executor_memory,
    driver_memory="512M",
    env_vars={"AWS_REGION": "eu-west-1"},
    conf={
        "spark.kubernetes.container.image": image,
        "spark.kubernetes.driver.annotation.iam.amazonaws.com/role": role,
        "spark.kubernetes.executor.annotation.iam.amazonaws.com/role": role,
    },
    spark_main_version=2,
    application="/opt/spark/work-dir/src/airquality/app.py",
    application_args=["--date", "{{ ds }}", "--jobs", "sample", "--env", "{{ macros.env() }}"],
)
