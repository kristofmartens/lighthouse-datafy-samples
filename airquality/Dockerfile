FROM datamindedbe/spark-k8s-glue:2.4.3-2.12-hadoop-2.9.2-v2

ENV PYSPARK_PYTHON python3
WORKDIR /opt/spark/work-dir

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN pip3 install -e .
