import urllib.request
import json
import pandas
import io
import datetime

import slack_payload
import satori

def lambda_handler(event, context):

   test = satori.satori_audit_handler(satori.satori_auth_handler(), event['tag'])
   for index, row in test.iterrows():
       payload = slack_payload.build_slack_payload(event['tag'], row[0], row[5], row[6], row[8], row[9], row[24], row[3])
       satori.send_to_slack(payload)    

