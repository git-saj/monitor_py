import cosmosdb
import monitor_smtp
import requests
import json

def request_sites():

    monitor_sites = json.loads(cosmosdb.select_monitor_sites())
    
    for site in monitor_sites:

        site_url = site["url"]
        site_group = site["notif_group"]
        site_expected_status = site["status_code"]

        request = requests.get(site_url)

        site_status_code = request.status_code

        if site_status_code != site_expected_status:
            monitor_smtp.monitor_sendmail(site_group, site_url, site_expected_status, site_status_code)

if __name__ == "__main__":
    request_sites()