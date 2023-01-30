# Pinterest Data Processing Pipeline
## Introduction

Pinterest has world-class machine learning engineering systems. They have billions of user interactions such as image uploads or image clicks which they need to process every day to inform the decisions to make. In this project, I build the system that takes in those events and runs them through two separate pipelines. One for the real-time streaming data and one processing batches of data. I use cloud resources such as google cloud platform as well as FastAPI, Kafka, Spark, and Airflow. 

You can watch the AICore introduction video for [The Pinterst Project](https://youtu.be/f8VNs1pmhb0) on Youtube.

<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="100"/>
<img src="pictures/kafka_highres.png" alt="Kafka" width="100"/>
<img src="pictures/Apache_Spark_logo.svg.png" alt="Spark" width="100"/>
<img src="pictures/AirflowLogo.png" alt="Airflow" width="100"/>

# The Event Emulator

AICore has provided me with a python script which uses SQLAlchemy to connect to an AWS RDS server. It runs an infinite loop where it pulls a row from the database and formats it as a dictionary called result, then uses `requests.post("http://localhost:8000/pin/", json=result)` as well as printing the data event to the terminal. 

## Project 

### FastAPI and uvicorn 
To complete the webhook I need to configure FastAPI to receive the post requests sent by the Event Emulator. 