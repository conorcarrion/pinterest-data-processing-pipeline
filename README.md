# Pinterest Data Processing Pipeline
## Introduction

Pinterest has world-class machine learning engineering systems. They have billions of user interactions such as image uploads or image clicks which they need to process every day to inform the decisions to make. In this project, I build the system that takes in those events and runs them through two separate pipelines. One for the real-time streaming data and one processing batches of data. I use cloud resources such as google cloud platform as well as FastAPI, Kafka, Spark, and Airflow. 

You can watch the AICore introduction video for [The Pinterest Project](https://youtu.be/f8VNs1pmhb0) on Youtube.

<a href="https://fastapi.tiangolo.com/"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="100"/> </a> <a href="https://kafka-python.readthedocs.io/en/master/index.html"> <img src="pictures/kafka_highres.png" alt="Kafka" width="100"/> </a> <a href="https://spark.apache.org/docs/latest/api/python/"><img src="pictures/Apache_Spark_logo.svg.png" alt="Spark" width="100"/></a><a href="https://airflow.apache.org/docs/"> <img src="pictures/AirflowLogo.png" alt="Airflow" width="100"/></a> <a href="https://chat.openai.com/chat"><img src="pictures/chatgpt.jpg" alt="ChatGPT" width="60"/></a>

### [ChatGPT](https://chat.openai.com/chat)

A recent development in the coding scene is ChatGPT, the chatbot launched with significant ability to debug and suggest code. I used ChatGPT to give feedback on any code that did not work, or suggest boilerplate code for various parts. As it was trained from older data and is known to suggest nonsensical or incorrect information, the documentation for the tools as well as resources from the AICore course were still my main source of knowledge. I mention it as a disclosure as it was very helpful, however all work is my own. 

### Pinterest Event Emulation

AICore provided a python script which uses SQLAlchemy to connect to an AWS RDS server. It runs an infinite loop where it pulls a row from the database and formats it as a dictionary called result, then sends a post request `requests.post("http://localhost:8000/pin/", json=result)` as well as printing the data event to the terminal. It then sleeps for 0-2s before continuing and pulling another row, etc. 

## Project 

### [FastAPI webhook receiver](API/pin_api.py) 
To complete the webhook I needed to configure FastAPI to receive the post requests sent by the Event Emulator. The boilerplate code for FastAPI is:

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/pin/")
def get_db_row():
    # do x
    return x


if __name__ == '__main__':
    uvicorn.run("pin_API:app", host="localhost", port=8000)
```

I developed this code further to use Pydantic's BaseModel class. Pydantic is a data validation and settings management library. BaseModel provides a convenient base class for defining the structure and types of the data that it represents. 

While not strictly necessary for this project, benefits from using it are typically the built-in support for data validation, type annotations, and automatic generation of documentation.

Using VScode integrated terminals I ran two terminals: my fastapi receiver and the emulator. I confirmed receipt of the post request in the terminal:
```
INFO:     127.0.0.1:46044 - "POST /pin/ HTTP/1.1" 200 OK
```
HTTP status code 200 shows it is received.

## [Kafka](https://kafka.apache.org/)
### Setup
To run Kafka locally I downloaded the kafka binary from their website and installed it in usr/local/kafka_2.13-3.3.1. I ensured I had Python and Java installed.
To run Zookeeper I used `bin/zookeeper-server-start.sh config/zookeeper.properties
` and to run Kafka server itself I ran `bin/kafka-server-start.sh config/server.properties
`. Both of these were opened in two more VScode integrated terminals bringing our open terminals while running to 4.

I learned how to use the Kafka CLI to create a topic, write some events and create consumers using the [Kafka quickstart guide](https://kafka.apache.org/quickstart).

### [Kafka-Python](https://kafka-python.readthedocs.io/en/master/index.html)
#### [KafkaAdminClient](lib/admin/kafka_admin_client.py) & Topics
I installed kafka-python with pip and read the [documentation](https://kafka-python.readthedocs.io/en/master/apidoc/modules.html). By finding examples of KafkaConsumer, KafkaProducer, KafkaAdminClient and KafkaClient as well as asking ChatGPT, I aggregated my knowledge and made classes in their own .py file using the boilerplate code as the `__init__` method. 

To MyKafkaAdminClient class (kafka_admin_client.py) I added a create topic method. I ran this to create my topic "Pins". I then ran 
```
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```
in the terminal to confirm my topic had been created.

#### [KafkaProducer](lib/batch/producer.py)

I created a KafkaProducer class and added a method which sends a message to the topic. I used `json.dumps().encode(ascii)` as the serializer. The value serializer is a function  that is used to convert the payload/value of a message being sent to the Kafka broker into bytes before being transmitted over the network.




#### Consumer
