import cosmosdb
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime
now = datetime.datetime.now()


def monitor_sendmail(group_id, url, expected_status_code, status_code):
    
    receivers = json.loads(cosmosdb.select_notif_group(group_id))

    for receiver in receivers:
        time_now = now.strftime("%Y-%m-%d %H:%M:%S")
        receiver = receiver["email"]

        msg_str = """<div style="font-family: inherit">The following site is reporting and unexpected HTTP status code: %s</div>
                    <div style="font-family: inherit">Expected status code: %s</div>
                    <div style="font-family: inherit">Reported status code: %s</div>
                    <div style="font-family: inherit">Timestamp: %s</div>""" % (url, expected_status_code, status_code, time_now)

        message = Mail(
            from_email='monitor@sajbox.com',
            to_emails=receiver,
            subject="Monitoring Alert: %s" % (url),
            html_content=msg_str
        )

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            output_str = "%s: Successfully sent monitoring alert to %s for site: %s with site status code: %s. Email status code: %s" % (time_now, receiver, url, status_code, response.status_code)
            print(output_str)
        except Exception as e:
            print(e)

        