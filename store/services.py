from django.contrib.auth.models import User
from store.models import Store
from django.core.cache import cache
import os
import json
import requests

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
        else:
            print "access code creation failed"

    return access_token

def create_oss_bucket(bucket):

    access_token = get_apigee_token()

    if not access_token :
        print '{"token_failed"}'
        return

    req = requests.post("https://developer.api.autodesk.com/oss/v2/buckets",
                       headers={"Authorization": "Bearer %s" % access_token,
                                "Content-Type": "application/json"},
                       data= json.dumps({"bucketKey" : bucket, "policyKey" : "transient"}) , verify=False)

    if req.status_code != 200:
        print req.json()
        return '{"create_failed"}'

    else:
        print req.json()
    return

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

def create_user(email, password):
    user_obj = User.objects.create_user(username=email.split('@')[0],
                                 email=email,
                                 password=password)
    return user_obj

def create_store(user_obj, store_name):
    store_obj = Store.objects.create(user=user_obj, name=store_name)
    return store_obj.id

