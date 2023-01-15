from fastapi import FastAPI
import uvicorn
import json
from lib.data import Data
from lib.producer import MyKafkaProducer
import configparser

app = FastAPI()


config = configparser.ConfigParser()
config.read("config/client.properties")
kf = MyKafkaProducer(config.get("DEFAULT", "bootstrap.servers"))


@app.post("/pin/")
def get_db_row(item: Data):
    data = dict(item)
    kf.send_message(topic="Pins", value=data)
    return item


if __name__ == "__main__":
    uvicorn.run("pin_api:app", host="localhost", port=8000)
