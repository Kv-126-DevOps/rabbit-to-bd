import json
import sys
import random
import requests

from config import *


def getChannel(data):
    for l in data.issue.labels:
        if l.name == "bug":
            return SLACK_BUG
        elif l.name == "userstory":
            return SLACK_US
        elif l.name == "testcase":
            return SLACK_TC
        else:
            return


def dataToMessage(data):
    user = data.issue.user.login
    action = data.action
    url = data.issue.html_url

    return f"{user} {action} issue in project.\n {url}"


def sendToSlack(data):
    if data.action != "opened":
        return

    url = SLACK_URL
    message = dataToMessage(data)
    title = (f"New Incoming Message :zap:")
    slack_data = {
        "icon_emoji": ":satellite:",
        "channel": getChannel(data),
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
