from azure.cosmos import CosmosClient
import os
import uuid
import json

url = "https://sajboxukscosmos001.documents.azure.com:443/"
key = os.environ.get('AZURE_API_KEY')

client = CosmosClient(url, credential=key)

def containerconn(database_name, container_name):

    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    return container

def select_notif_group(group_id):
    query='SELECT c.email FROM notif_groups f join c in f.email_addresses WHERE f.id = "%s"' % (group_id)
    container = containerconn("monitor_pydb", "notif_groups")
    email_addresses = (list(container.query_items(query=query, enable_cross_partition_query=True)))
    email_addresses = json.dumps(email_addresses, indent=True)
    return email_addresses

def select_monitor_sites():
    query='SELECT monitor_sites.url,monitor_sites.notif_group,monitor_sites.status_code FROM monitor_sites'
    container = containerconn("monitor_pydb", "monitor_sites")
    monitor_sites = (list(container.query_items(query=query, enable_cross_partition_query=True)))
    monitor_sites = json.dumps(monitor_sites, indent=True)
    return monitor_sites

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