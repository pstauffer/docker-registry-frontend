from flask import Flask, render_template

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
    return render_template('image.html', image=image, tags=tags, registry=os.environ['REGISTRY_URL'])

def set_basic_auth_state():
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
    api_url = os.environ['REGISTRY_URL'] + '/v2/' + path

    if ENV_BASIC_AUTH:
        try:
            from requests.auth import HTTPBasicAuth  
            return requests.get(api_url, auth=HTTPBasicAuth(os.environ['REGISTRY_USER'], os.environ['REGISTRY_PW']))
        except requests.exceptions.RequestException as e:
            print ("Problem during docker registry connection")
            raise
    else:
        try:
            return requests.get(api_url)
        except requests.exceptions.RequestException as e:
            print ("Problem during docker registry connection")
            raise

if __name__ == "__main__":
    # set local variable for basic authentication
    ENV_BASIC_AUTH = set_basic_auth_state()
    app.run(host='0.0.0.0', debug=True)
