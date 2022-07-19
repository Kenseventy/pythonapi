from azure.cosmos import exceptions, CosmosClient, PartitionKey

url = 'https://kmazureresume.documents.azure.com:443/'
key = '1Cma5jR9rzgmQnuSiikrJq88qrGBrIGgosrQU1hxngbDMpFl973XQVUEhpGXSAeGgkpE9g5EQUorfggW7eH1UA=='
client = CosmosClient(url, key)
database_name = 'AzureResume'
container_name = 'api'