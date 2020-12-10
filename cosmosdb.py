from azure.cosmos import CosmosClient
import uuid

url = "https://sajboxukscosmos001.documents.azure.com:443/"
key = "FdYa0SfRB7HZZiB0W5JViY6XYyF6ARQmtdCazq3KXsZBuD0rOPNPOYXBOqEsxyKQza2heDQgIJF8gwUFNGjxPA=="

client = CosmosClient(url, credential=key)

def containerconn(database_name, container_name):

    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    return container

def mon_sites_upsert(url, notif_group, exp_status_code):
    mon_sites_container = containerconn("monitor_pydb", "monitor_sites")
    mon_sites_id = uuid.uuid1()

    mon_sites_container.upsert_item({
                    'id': '{0}'.format(mon_sites_id),
                    'url': '{0}'.format(url),
                    'notif_group': '{0}'.format(notif_group),
                    'status_code': '{0}'.format(exp_status_code)
                }
            )

    output = "Added monitoring for URL: %s to DB for notification group: %s with expected status code: %s" % (url, notif_group, exp_status_code)
    print(output)






#mon_sites_upsert('https://theboiz.gg', "d75ee3ee-3b2e-11eb-8aea-0022483f4bcf", "200")