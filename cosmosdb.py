from azure.cosmos import CosmosClient

url = "https://sajboxukscosmos001.documents.azure.com:443/"
key = "FdYa0SfRB7HZZiB0W5JViY6XYyF6ARQmtdCazq3KXsZBuD0rOPNPOYXBOqEsxyKQza2heDQgIJF8gwUFNGjxPA=="

client = CosmosClient(url, credential=key)

def containerconn(database_name, container_name):

    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    return container