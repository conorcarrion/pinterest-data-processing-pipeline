# Pinterest Data Processing Pipeline
## Introduction

Pinterest has world-class machine learning engineering systems. They have billions of user interactions such as image uploads or image clicks which they need to process every day to inform the decisions to make. In this project, I build the system that takes in those events and runs them through two separate pipelines. One for the real-time streaming data and one processing batches of data. I use cloud resources such as google cloud platform as well as FastAPI, Kafka, Spark, and Airflow. 

You can watch the AICore introduction video for [The Pinterest Project](https://youtu.be/f8VNs1pmhb0) on Youtube.

<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="100"/> <img src="pictures/kafka_highres.png" alt="Kafka" width="100"/> <img src="pictures/Apache_Spark_logo.svg.png" alt="Spark" width="100"/> <img src="pictures/AirflowLogo.png" alt="Airflow" width="100"/>

### ChatGPT

A recent development in the coding scene has been ChatGPT, the chatbot launched with significant ability to debug and suggest code. I will be using ChatGPT to give feedback on any code that does not work, or suggest boilerplate code for various parts. As it was trained from older data and is known to suggest nonsensical or incorrect information, the documentation for the tools as well as resources from the AICore course will still be my main source of knowledge.

### Pinterest Event Emulation

AICore has provided a python script which uses SQLAlchemy to connect to an AWS RDS server. It runs an infinite loop where it pulls a row from the database and formats it as a dictionary called result, then sends a post request `requests.post("http://localhost:8000/pin/", json=result)` as well as printing the data event to the terminal. It then sleeps for 0-2s before continuing and pulling another row, etc. 

## Project 

### FastAPI and uvicorn 
To complete the webhook I need to configure FastAPI to receive the post requests sent by the Event Emulator. The boilerplate code for FastAPI is:

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



Running two terminals for this fastapi code and the emulator, I can confirm receipt of the post request:
```
INFO:     127.0.0.1:46044 - "POST /pin/ HTTP/1.1" 200 OK
```
HTTP status code 200 shows it is received.