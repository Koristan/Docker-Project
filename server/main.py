#!/usr/bin/env python3

from fastapi import FastAPI, Body
import pymongo
from pymongo import MongoClient
import logging

app = FastAPI()

client = pymongo.MongoClient("mongodb://user:user@mongo:27017/")

db = client["messages_db"]

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

@app.get('/api/v1/messages/')
def get_messages():
    global db
    logger.info('\n\nGET MESSAGES!\n\n')
    messages = db["messages"]
    all_messages = {}
    count = 0
    logger.info('\n\nFOR CYCLE!\n\n')
    try:
        for message in messages.find():
            message['_id'] = str(message['_id'])
            all_messages[count] = message
            count += 1
        logger.info('\n\nRETURN!\n\n')
    except Exception as e:
        logger.critical(e)
        return "Ошибка сервера :("
    return all_messages

@app.post('/api/v1/message/')
def post_message(name : str, message_text : str):

    messages = db["messages"]

    mess = {
        "name" : name,
        "message" : message_text,
    }
    logger.info('\n\nDB CONNECT!\n\n')
    try: 
        messages.insert_one(mess)
    except Exception as e:
        return "DB connect error - " + str(e)
    return "succesfull"