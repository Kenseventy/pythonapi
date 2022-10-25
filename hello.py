from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json
import os
from config import url,key


client = CosmosClient(url, key)
database_name = 'AzureResume'
container_name = 'api'
# [END create_client]

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)
# [END get_container]

item = { "firstname": "John", "lastname": "Doe"}

test = container.create_item(body=item)




#item = container.read_item("1",partition_key="1")
#item["count"] = int(item["count"])
#item["count"] = (item["count"] + 1)
#updated_count = container.upsert_item(item)

#with open('resume.json', "r") as json_file:
#    data = json.load(json_file)
#    data['Resume']['viewCount'] = item["count"]

#with open('resume.json', "w") as json_file:
#    json.dump(data,json_file)
