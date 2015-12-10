from django.contrib.auth.models import User, Permission
from django.core.cache import cache
import os
import json
import requests
import urllib
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
import datetime

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

    return

def upload_oss_obj(bucket,local_file, oss_obj_name):
    print "In OSS Upload"
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
            print req.json()
            return "Not Uploaded"
        else:
            return req.json()["objectId"]

def check_store_created(store_name, user_id):
    from store.models import Store
    return bool(Store.objects.filter(name=store_name, user_id=user_id))

def create_or_get_store(request):
    email, password, store_name, username = request.POST['email'], request.POST['password'], request.POST['store_name'], request.POST['user_name']
    try:
        user_obj = User.objects.create_user(username=username, email=email, password=password, is_staff=1)
    except IntegrityError:
        print "User already registered"
        user_obj = User.objects.filter(username=username)[0]
    print user_obj.id
    perms = ('Can add store', 'Can change store', 'Can delete store', 'Can add products', 'Can change products', 'Can delete products',)
    for perm in perms:
        permission_obj = Permission.objects.get(name=perm)
        user_obj.user_permissions.add(permission_obj)
    user_obj = authenticate(username=username, password=password)
    print "authenticated user" + str(user_obj)
    login(request, user_obj)
    if not check_store_created(store_name, user_obj.id):
        from store.models import Store
        store_obj = Store(user=user_obj, name=store_name, created_date=datetime.datetime.now())
        store_obj.save()
        create_oss_bucket(store_name)
    return True

def register_oss_object(object_id):

    access_token = get_apigee_token()

    if not access_token :
        print '{"token_failed"}'
        return

    req = requests.post("https://developer.api.autodesk.com/viewingservice/v1/register",
                       headers={"Authorization": "Bearer %s" % access_token,
                                "Content-Type": "application/json"},
                       data= json.dumps({"urn" : urllib.urlencode(object_id) }) , verify=False)

    if req.status_code != 200:
        print req.json()

    return

