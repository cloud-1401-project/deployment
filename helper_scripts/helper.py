import os
import sys
import re

import requests
import json
import time
import grpc
import auth_pb2_grpc
import auth_pb2
import random
channel = grpc.insecure_channel('localhost:50051')
stub = auth_pb2_grpc.AuthServiceStub(channel)


url = "http://127.0.0.1:8080/api/auth/"
admin_email = "admin@mail.com"
admin_password = "adminadmin"
debug_global = False


def signup(first_name, last_name, email, password):
    payload = {'first_name': first_name, 'last_name': last_name,
               'email': email, 'password': password}
    headers = {'Content-Type': 'application/json'}
    if debug_global:
        print(json.dumps(payload, indent=4, ensure_ascii=False))
    response = requests.request(
        "POST", url + "sign_up", headers=headers, data=json.dumps(payload))
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def signin(email, password):
    payload = {'email': email, 'password': password}
    headers = {'Content-Type': 'application/json'}
    if debug_global:
        print(json.dumps(payload, indent=4, ensure_ascii=False))
    response = requests.request(
        "POST", url + "sign_in", headers=headers, data=json.dumps(payload))
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def signout(token, reftok):
    payload = {'refresh_token': reftok}
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    if debug_global:
        print(json.dumps(payload, indent=4, ensure_ascii=False))
    response = requests.request(
        "POST", url + "sign_out", headers=headers, data=json.dumps(payload))
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def refresh(token, reftok):
    payload = {'refresh_token': reftok}
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    if debug_global:
        print(json.dumps(payload, indent=4, ensure_ascii=False))
    response = requests.request(
        "POST", url + "refresh", headers=headers, data=json.dumps(payload))
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def update_me(token, first_name, last_name, email, password, url="http://127.0.0.1:8080/api/users/"):
    # create payload based on what is passed in if they are not None or empty string
    payload = {}
    if first_name:
        payload['first_name'] = first_name
    if last_name:
        payload['last_name'] = last_name
    if email:
        payload['email'] = email
    if password:
        payload['password'] = password

    if debug_global:
        print(json.dumps(payload, indent=4, ensure_ascii=False))
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    response = requests.request(
        "PUT", url, headers=headers, data=json.dumps(payload))
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def update_admin(token, _id, first_name, last_name, email, password, access_level, url="http://127.0.0.1:8080/api/users/"):
    payload = {}
    if first_name:
        payload['first_name'] = first_name
    if last_name:
        payload['last_name'] = last_name
    if email:
        payload['email'] = email
    if password:
        payload['password'] = password
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    if debug_global:
        print(json.dumps(payload, indent=4, ensure_ascii=False))
    response = requests.request(
        "PUT", url + _id, headers=headers, data=json.dumps(payload))
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def create_user(token, first_name, last_name, email, password, access_level, url="http://127.0.0.1:8080/api/users/"):
    payload = {'first_name': first_name, 'last_name': last_name,
               'email': email, 'password': password, 'access_level': access_level}
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    if debug_global:
        print(json.dumps(payload, indent=4, ensure_ascii=False))
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def delete_me(token, url="http://127.0.0.1:8080/api/users/"):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    response = requests.request("DELETE", url, headers=headers)
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def delete_admin(token, _id, url="http://127.0.0.1:8080/api/users/"):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    response = requests.request("DELETE", url + _id, headers=headers)
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def get_one_user(token, _id, url="http://127.0.0.1:8080/api/users/"):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    response = requests.request("GET", url + _id, headers=headers)
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def get_my_acc(token, url="http://127.0.0.1:8080/api/users/my_acc"):
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.request("GET", url, headers=headers)
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code


def get_many_users(token, first_name, last_name, email, access_level, access_level_cmp, page=1, size=20, url="http://127.0.0.1:8080/api/users/"):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    # build query string from parameters if not empty or None
    query_string = "?"
    if first_name is not None and first_name != "":
        query_string += "first_name=" + first_name + "&"
    if last_name is not None and last_name != "":
        query_string += "last_name=" + last_name + "&"
    if email is not None and email != "":
        query_string += "email=" + email + "&"
    if access_level is not None:
        query_string += "access_level=" + str(access_level) + "&"
    if access_level_cmp is not None:
        query_string += "access_level_cmp=" + str(access_level_cmp) + "&"

    # remove last &
    if query_string != "?":
        query_string = query_string[:-1]
    if query_string == "?":
        query_string = ""
    response = requests.request("GET", url + query_string, headers=headers)
    if debug_global:
        print(query_string)
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code

def get_all_products(token, url="http://127.0.0.1:8000/api/products/all"):
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.request("GET", url, headers=headers)
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code

def create_random_products(token, url="http://127.0.0.1:8000/api/products/create_random_products"):
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.request("POST", url, headers=headers)
    if debug_global:
        print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text), response.status_code

def automated_test_pipeline():
    # signup
    random_email_signup = "test" + str(random.randint(0, 100)) + "@test.com"
    _, code = signup("test", "test", random_email_signup, "testtest")
    if code != 200:
        print("TEST[signup with correct data] failed")
    else:
        print("TEST[signup with correct data] succeeded")
    _, code = signup("test", "test", "ttttt.com", "te")
    if code != 400:
        print("TEST[signup with incorrect email and password] failed")
    else:
        print("TEST[signup with incorrect email and password] succeeded")

    # signin
    _, code = signin(random_email_signup, "testtest")
    if code != 200:
        print("TEST[signin with correct data] failed")
    else:
        print("TEST[signin with correct data] succeeded")

    # signout
    tokens, code = signin(random_email_signup, "testtest")
    if code != 200:
        print("TEST[signout with correct data] failed")
    else:
        _, code = signout(tokens["access_token"], tokens["refresh_token"])
        if code != 200:
            print("TEST[signout with correct data] failed")
        else:
            print("TEST[signout with correct data] succeeded")

    # create user with random email
    tokens, code = signin(admin_email, admin_password)
    random_email = "test" + str(random.randint(0, 100)) + "@test.com"
    if code != 200:
        print("TEST[create user with correct data] failed")
    else:
        _, code = create_user(
            tokens["access_token"], "test", "test", random_email, "testtest", 1)
        if code != 200:
            print("TEST[create user with correct data] failed")
        else:
            print("TEST[create user with correct data] succeeded")

    # get many users
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[get many users with correct data] failed")
    else:
        users, code = get_many_users(
            tokens["access_token"], "", "", random_email, None, None, None)
        if code != 200:
            print("TEST[get many users with correct data] failed")
        else:
            print("TEST[get many users with correct data] succeeded")

    # get one user
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[get one user with correct data] failed")
    else:
        users, code = get_one_user(
            tokens["access_token"], users["data"]["data"][0]["_id"]["$oid"])
        if code != 200:
            print("TEST[get one user with correct data] failed")
        else:
            print("TEST[get one user with correct data] succeeded")

    # update user
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[update user with correct data] failed")
    else:
        _, code = update_admin(tokens["access_token"], users["data"]
                               [0]["_id"]["$oid"], "test", "test", None, "testtest", None)
        if code != 200:
            print("TEST[update user with correct data] failed")
        else:
            print("TEST[update user with correct data] succeeded")

    # delete user
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[delete user with correct data] failed")
    else:
        _, code = delete_admin(
            tokens["access_token"], users["data"][0]["_id"]["$oid"])
        if code != 200:
            print("TEST[delete user with correct data] failed")
        else:
            print("TEST[delete user with correct data] succeeded")

    # update me
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[update my profile with correct data] failed")
    else:
        _, code = update_me(
            tokens["access_token"], "admiiiiiiiiin", "admiiiiiiiiiiiiiiin", None, None)
        if code != 200:
            print("TEST[update my profile with correct data] failed")
        else:
            print("TEST[update my profile with correct data] succeeded")

    # get me
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[get my profile with correct data] failed")
    else:
        _, code = get_my_acc(tokens["access_token"])
        if code != 200:
            print("TEST[get my profile with correct data] failed")
        else:
            print("TEST[get my profile with correct data] succeeded")

    # get products
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[getting products] failed")
    else:
        _, code = get_all_products(tokens["access_token"])
        if code != 200:
            print("TEST[getting products] failed")
        else:
            print("TEST[getting products] succeeded")

    # create random products
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[creating products] failed")
    else:
        _, code = create_random_products(tokens["access_token"])
        if code != 200:
            print("TEST[creating products] failed")
        else:
            print("TEST[creating products] succeeded")

    # create random products
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[creating products] failed")
    else:
        x = stub.HasAccess(auth_pb2.Resource(path='/api/products/all', method='GET', jwt=tokens['access_token'])).has_access
        print(f'x is {x}')
        # _, code = create_random_products(tokens["access_token"])
        # if code != 200:
        #     print("TEST[creating products] failed")
        # else:
        #     print("TEST[creating products] succeeded")

    # signout from admin
    tokens, code = refresh(tokens["access_token"], tokens["refresh_token"])
    if code != 200:
        print("TEST[signout from admin with correct data] failed")
    else:
        _, code = signout(tokens["access_token"], tokens["refresh_token"])
        if code != 200:
            print("TEST[signout from admin with correct data] failed")
        else:
            print("TEST[signout from admin with correct data] succeeded")

    # wait for keyboard input then return
    input("Press Enter to continue...")
    return



automated_test_pipeline()
