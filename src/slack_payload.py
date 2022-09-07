import urllib.request
import json
import pandas
import io
import datetime


def build_slack_payload(tag, timestamp, database, user, tool, table, action, flow_id):

#    print(row[0]) #timestamp
#    print(row[5]) #database
#    print(row[6]) #user
#    print(row[8]) #tool
#    print(row[9]) #table
#    print(row[18]) #query
#    print(row[24]) #action
#    print("-----------------------------------------")


    message = '''
    {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New Audit Alert for tag: %s",
                    "emoji": true
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Action Taken:*\n_%s_"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Dataset:*\n%s"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*When:*\n%s"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*User:*\n%s"
                    }
                ]
            },
             {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Tool:*\n%s"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Table:*\n%s"
                    }
                ]
            },
             {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Flow ID:*\n<https://app.satoricyber.com/audit?timeFrame=last90days&flowId=%s | more info in app>"
                    }
                ]
            }
            
        ]
    }
    ''' % (tag, action, database, timestamp, user, tool, table, flow_id)
    return message