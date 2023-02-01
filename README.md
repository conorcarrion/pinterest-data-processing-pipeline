# Pinterest Data Processing Pipeline
## Introduction

Pinterest has world-class machine learning engineering systems. They have billions of user interactions such as image uploads or image clicks which they need to process every day to inform the decisions to make. In this project, I build the system that takes in those events and runs them through two separate pipelines. One for the real-time streaming data and one processing batches of data. I use cloud resources such as Google Cloud Platform as well as FastAPI, Kafka, Spark, and Airflow.

The AICore introduction video for [The Pinterest Project](https://youtu.be/f8VNs1pmhb0) is available on Youtube.

<a href="https://fastapi.tiangolo.com/"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="100"/> </a> <a href="https://kafka-python.readthedocs.io/en/master/index.html"> <img src="pictures/kafka_highres.png" alt="Kafka" width="100"/> </a> <a href="https://spark.apache.org/docs/latest/api/python/"><img src="pictures/Apache_Spark_logo.svg.png" alt="Spark" width="100"/></a><a href="https://airflow.apache.org/docs/"> <img src="pictures/AirflowLogo.png" alt="Airflow" width="100"/></a> <a href="https://chat.openai.com/chat"><img src="pictures/chatgpt.jpg" alt="ChatGPT" width="60"/></a>

### [ChatGPT](https://chat.openai.com/chat)

A recent development in the coding scene is ChatGPT, the chatbot launched with significant ability to debug and suggest code. I used ChatGPT to give feedback on any code that did not work, or suggest boilerplate code for various parts. As it was trained from older data and is known to suggest nonsensical or incorrect information, the documentation for the tools as well as resources from the AICore course were still my main source of knowledge. I mention it as a disclosure as it was very helpful, however all work is my own.

### Pinterest Event Emulation

AICore provided a python script which uses SQLAlchemy to connect to AICore's pre-setup AWS RDS server containing spoof Pinterest event data. It runs an infinite loop where it pulls a row from the database and formats it as a dictionary called result, then sends a post request: `requests.post("http://localhost:8000/pin/", json=result)` as well as printing the data event to the terminal. It then sleeps for 0-2s before continuing and pulling another row, etc, thus providing a stream of pin data for me to process.

---

## Project

### [FastAPI webhook receiver](API/pin_api.py)
To complete the webhook I needed to configure FastAPI to receive the post requests sent by the Event Emulator. The boilerplate code for FastAPI is:

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/url/")
def get_db_row():
    # do x
    return x


if __name__ == '__main__':
    uvicorn.run("app_name:app", host="localhost", port=8000)
```

I developed from this starting point to use Pydantic's BaseModel class. Pydantic is a data validation and settings management library. BaseModel provides a convenient base class for defining the structure and types of the data that it represents.

While not strictly necessary for this project, benefits from using it are typically the built-in support for data validation, type annotations, and automatic generation of documentation.

Using VScode integrated terminals I ran two terminals: my fastapi receiver and the emulator. I confirmed receipt of the post request in the terminal:
```
INFO:     127.0.0.1:46044 - "POST /pin/ HTTP/1.1" 200 OK
```
HTTP status code 200 shows it is received.

---

## [Kafka](https://kafka.apache.org/)
### Setup
To run Kafka locally I downloaded the kafka binary from their website and installed it in usr/local/kafka_2.13-3.3.1. I ensured I had Python and Java installed.
To run Zookeeper I used `bin/zookeeper-server-start.sh config/zookeeper.properties
` and to run Kafka server itself I ran `bin/kafka-server-start.sh config/server.properties
`. Both of these were opened in two more VScode integrated terminals bringing our open terminals while running to 4.

Though I am going to use Kafka-Python, I learned how to use the Kafka CLI to create a topic, write some events and create consumers using the [Kafka quickstart guide](https://kafka.apache.org/quickstart). I also watched some of the [Kafka 101](https://developer.confluent.io/learn-kafka/apache-kafka/events/) videos on Confluent's website with the intriguing Tim Berglund.

### [Kafka-Python](https://kafka-python.readthedocs.io/en/master/index.html)
#### [KafkaAdminClient](lib/admin/kafka_admin_client.py) & Topics
I installed kafka-python with pip and read the [documentation](https://kafka-python.readthedocs.io/en/master/apidoc/modules.html). By finding examples of KafkaConsumer, KafkaProducer, KafkaAdminClient and KafkaClient as well as asking ChatGPT, I aggregated my knowledge and made classes in their own .py file using the boilerplate code as the `__init__` method. This is probably taking the OOP principles too far for so little code, but it keeps things nice separated.

To MyKafkaAdminClient class (kafka_admin_client.py) I added a create topic method. I ran this to create my topic "Pins". I then ran
```
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```
in the terminal to confirm my topic had been created.

#### [KafkaProducer](lib/batch/producer.py)

I created a KafkaProducer class using the [docs](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html) and added a method which sends a message to the topic. I used `json.dumps().encode(ascii)` as the serializer. The value serializer is a function  that is used to convert the payload/value of a message being sent to the Kafka broker into bytes before being transmitted over the network.

I added `kf = MyKafkaProducer(config.get("DEFAULT", "bootstrap.servers"))` to my API and then within the webhook receiver I added `kf.send_message(topic="Pins", value=data)` so that the Pin event is sent to the topic "Pins".

#### [KafkaConsumer](lib/batch/batch_consumer.py)

I created a KafkaConsumer class using some boilerplate code from chatgpt and arguments from the [docs](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html).
While the project suggests I use a AWS S3 bucket, I have used amazon cloud services for another project, so I wanted to use google cloud platform instead so that I could get some experience using the google interface (Amazon also charged me £18 for an RDS table with 5 rows in it, so I was feeling a bit miffed with them). So after configuring the Google cloud platform bucket using the web interface, I added a method to MyKafkaConsumer to consume messages from the topic and upload them to the bucket in the form `filename.json`. Each filename was given a unique uuid using the uuid library.

---

## Other Components

### [Google Cloud Platform](lib/admin/gcp_bucket.py)

For connection to my Google Cloud bucket I downloaded the keyfile or service account file as it is also called. It is simply a json with the details for the bucket. I used the python google cloud library to connect to my storage account and project. I then added methods to create a bucket, write to a bucket of choice and delete json files from the bucket.

### [Spark](lib/batch/batch_spark.py)

`pip install Pyspark` to start off. I created a yaml file with the details for the Google Cloud Platform credentials and made a "BatchSpark" class in batch_spark.py. I initially was using a "gcs connector.jar" from Maven but I could not get it to work and found another method via trawling Stack Overflow, other forums and chatgpt. I added a method to load all the json files in the bucket using *.json.

### [Data Clean](lib/admin/data_clean.py)

The data from the pin events has some aspects which need to be adjusted. The Follower count column has a mix of thousands and millions. Some of the rows contain no information. Some of the rows have no tags in the tag_list column and it has parsed that as "N,o, ,T,a,g,s, ,A,v,a,i,l,a,b,l,e". The "been_downloaded" column is better as boolean than binary 1/0. The poster_name column has been purged for data-protection reasons so is blank and can also be dropped.


### [Airflow and DAGs](lib/batch/batch_spark_clean_dag.py)

A Directed acyclic graph is a core component of the apache airflow scheduling system. It is essentially a configuration file, written in python, which describes the parameters for the scheduled task.

First the arguments for the DAG are described. These include when the scheduled task should start occurring, at what time, whether to retry and when. One can also describe a series of tasks, including tasks to perform in case of failure, etc.


### [Run Daily Batch Process](lib/batch/run.py)

```python
def run():
    client = GCPBucketClient()
    spark = BatchSpark()

    MyKafkaConsumer.consume_messages_to_bucket(client, "project-pin-api")

    df = spark.load_batch_from_bucket()
    df = data_clean(df)

    # load dataframe to HBASE and perform daily analysis

    client.delete_json_files("project-pin-api")
```
This simple piece of code is the daily task which will be completed by the DAG. A Google Cloud Platform client is created which connects to my project. A spark instance is created. My kafka consumer then consumes messages from the topic and uploads them as json files to the bucket. Spark then loads these json files as a batch of data and loads it to a dataframe. Some cleaning is done on the batch. At this point the dataframe could be loaded to some long term storage or analysis performed and the metrics from that analysis saved. Finally a clean up of the contents of the bucket is performed.

### [Real-Time Streaming Spark](lib/streaming/streaming_spark.py)

set PYSPARK environment variables which do ...

create spark context and spark streaming context

create spark session

set spark up to receive data from kafka, subscribing to pins topic, with offset

sql query to cast/capture entire value column as a string.

create schema for the expected data

explode out the data from the json into a dataframe.

// Add comments to code directly.
