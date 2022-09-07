import urllib.request
import json
import pandas
import io
import datetime

import config

min15ago = datetime.datetime.now() - datetime.timedelta(minutes=15)
unix_time_start = min15ago.strftime("%s") + "000"
unix_time_end = str(int(min15ago.strftime("%s")) + (900)) + "000"

def satori_auth_handler():
    
    payload = '{"serviceAccountId": "' + config.satori_serviceaccount_id + '", "serviceAccountKey": "' + config.satori_serviceaccount_key + '"}'
    # Authenticate to Satori for a bearer token
    authheaders = {'content-type': 'application/json','accept': 'application/json'}
    url = "https://{}/api/authentication/token".format(config.satori_host)
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            url=url,
            headers=authheaders,
            data=payload.encode(encoding='utf-8', errors='strict'),
            method='POST'),
            timeout=60)
        rjson = json.loads(r.read())
        satori_token = rjson['token']
        return satori_token
    except Exception as err:
        print("Bearer Token Failure: :", err)
        print("Exception TYPE:", type(err))

def satori_audit_handler(satori_token, custom_tagname):
    # build request to rest API for audit entries, aka "data flows"
    
    
    audit_headers = {
    'Authorization': 'Bearer {}'.format(satori_token),
    }
    auditurl = "https://{}/api/data-flow/{}/export?from={}&to={}&tagsFilter={}".format(config.satori_host,
                                                                         config.satori_account_id,
                                                                         unix_time_start,
                                                                         unix_time_end,
                                                                         custom_tagname)
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            url=auditurl,
            headers=audit_headers,
            method='GET'),
            timeout=60)
        res_body = r.read().decode(encoding='utf-8')
        result = io.StringIO(res_body)
        df = pandas.read_csv(result)
        print(df.head())
        return df
    except Exception as err:
        print("Audit Retrieval Failure: :", err)
        print("Exception TYPE:", type(err))

def send_to_slack(event):

    res = urllib.request.urlopen(urllib.request.Request(
            url=config.slack_webhook,
            headers={'content-type': 'application/json','accept': 'application/json'},
            data=event.encode(encoding='utf-8', errors='strict'),
            method='POST'),
            timeout=60)
    return event