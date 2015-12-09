import os
import json
import requests
from django.core.cache import cache

CLIENT_ID='ZVu6cFFGxMJohgsaDsbLfu9jNs4pQEif'
CLIENT_SECRET='47C2LzDqv9b7C120'

def get_apigee_token():
    access_token = None

    if cache.get('APIGEE-ACCESS-TOKEN') :
        access_token = cache.get('APIGEE-ACCESS-TOKEN')
    else:
        req = requests.post("https://developer.api.autodesk.com/authentication/v1/authenticate",
                            data={'client_id': CLIENT_ID,
                                  'client_secret': CLIENT_SECRET,
                                  'grant_type': 'client_credentials'
                                 }, verify=False)

        if req.status_code == 200:
            access_token = req.json()['access_token']
            cache.set('APIGEE-ACCESS-TOKEN', access_token, 1700)

    return access_token

def create_oss_bucket(bucket):
    print "getting token"
    access_token = get_apigee_token()

    if not access_token :
        return '{"token_failed"}'

    req = requests.post("https://developer.api.autodesk.com/oss/v2/buckets",
                       headers={"Authorization": "Bearer %s" % access_token,
                                "Content-Type": "application/json"},
                       data= json.dumps({"bucketKey" : bucket, "policyKey" : "transient"}) , verify=False)

    if req.status_code != 200:
        print req.json()
        return '{"create_failed"}'
    else:
        return req.json()

def upload_oss_obj(bucket,local_file, oss_obj_name):

    access_token = get_apigee_token()

    if not access_token :
        return '{"token_failed"}'

    with open(local_file, 'rb') as file_to_be_upload:
        req = requests.put("https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s"
                           % (bucket, oss_obj_name),
                           headers={"Authorization": "Bearer %s" % access_token,
                                    "Content-Type": "application/octet-stream"},
                           data=file_to_be_upload, verify=False)
        if req.status_code != 200:
            return '{"upload_failed"}'
        else:
            return req.json()

if __name__ == "__main__":

    v =  create_oss_bucket("hupahupa")
    print v