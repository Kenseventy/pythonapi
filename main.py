from enum import Enum
from importlib.resources import path
import string
from unicodedata import name
from starlette.requests import Request
from starlette.responses import Response
from fastapi import FastAPI, Request, Form
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import config
import json
import os
from datetime import date
from fastapi.templating import Jinja2Templates



# [END create_client]

database = config.client.get_database_client(config.database_name)
container = database.get_container_client(config.container_name)


path = 'C:/Users/Kenseventy/Git/apicounter/'

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

class Guest(BaseModel):
    name: str
    message: str | None = None

@app.get("/")
async def root(request: Request):
    client_host = request.client.host
    item = container.read_item("counter",partition_key="counter")
    item["count"] = int(item["count"])
    item["count"] = (item["count"] + 1)
    updated_count = container.upsert_item(item) 
    with open('resume.json', "r") as json_file:
        data = json.load(json_file)
    data['resume']['viewCount'] = item["count"]

    with open('resume.json', "w") as json_file:
        json.dump(data,json_file)
    file_path = os.path.join(path, "resume.json")
    return FileResponse(file_path)




@app.post("/guestbook")
async def create_item(item: Guest):
    test = container.query_items(query="SELECT VALUE COUNT(1) FROM c", enable_cross_partition_query=True)
    test_list = list(test)
    item_count = test_list[0]
    id = "message" + str(item_count)
    name = item.name
    message = item.message
    today = date.today()
    data = {"id": id, "name": name, "message": message, "date": str(today)}
    post = container.create_item(body=data)
    thank = "Thank you for your message " + item.name
    return thank

@app.get("/form")
def form_post(request: Request):
    item = container.query_items(query="SELECT * FROM c WHERE IS_DEFINED(c.name)", enable_cross_partition_query=True)
    result = print(item)
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/form")
def form_post(request: Request, name: str = Form(...)):
    result = name
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})