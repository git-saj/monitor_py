import cosmosdb
import monitor_smtp
import requests
import json
import datetime
now = datetime.datetime.now()

def request_sites():

    check_int = 0

    monitor_sites = json.loads(cosmosdb.select_monitor_sites())
    
    for site in monitor_sites:

        site_url = site["url"]
        site_group = site["notif_group"]
        site_expected_status = site["status_code"]

        request = requests.get(site_url)

        site_status_code = request.status_code

        if int(site_status_code) != int(site_expected_status):
            check_int = 1
            monitor_smtp.monitor_sendmail(site_group, site_url, site_expected_status, site_status_code)

    if check_int == 0:
        output_str = "%s: %s sites checked and all returned expected status codes" % (now, len(monitor_sites))
        print(output_str)


if __name__ == "__main__":
    request_sites()