from flask import Flask, render_template, url_for

import requests
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    r = registry_request('_catalog')
    j = r.json()
    images = j['repositories']
    return render_template('index.html', images=images)

@app.route("/about")
def about():
    return render_template('layout.html')

@app.route('/image/<path:image>')
def tags(image):
    r = registry_request(image + '/tags/list')
    j = r.json()
    tags = j['tags']
    return render_template('image.html', image=image, tags=tags, registry=get_registry_url())

def get_registry_url():
    try:
        os.environ['REGISTRY_URL']
    except KeyError:
        print ("Registry URL not set!")
        raise
    else:
        return os.environ['REGISTRY_URL']

def get_registry_user():
    try:
        os.environ['REGISTRY_USER']
    except KeyError:
        return "Registry User not set!"
    else:
        return os.environ['REGISTRY_USER']

def get_registry_password():
    try:
        os.environ['REGISTRY_PW']
    except KeyError:
        return "Registry Password not set!"
    else:
        return os.environ['REGISTRY_PW']


def get_basic_auth():
    try:
        os.environ['BASIC_AUTH']
    except KeyError:
        return False
    else:
        if os.environ['BASIC_AUTH'] == "true":
            return True
        else:
            return False

def registry_request(path):
    api_url = get_registry_url() + '/v2'
    full_url = api_url + '/' + path

    if get_basic_auth():
        try:
            from requests.auth import HTTPBasicAuth  
            return requests.get(full_url, auth=HTTPBasicAuth(get_registry_user(), get_registry_password()))
        except requests.exceptions.RequestException as e:
            print ("Problem during docker registry connection")
            raise
    else:
        try:
            return requests.get(full_url)
        except requests.exceptions.RequestException as e:
            print ("Problem during docker registry connection")
            raise

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
