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

def registry_request(path):
    api_url = os.environ['REGISTRY_URL'] + '/v2/' + path

    # set default value to False
    REGISTRY_AUTH = os.environ.get('REGISTRY_AUTH',False)

    if REGISTRY_AUTH == "True" or REGISTRY_AUTH == "true":
        from requests.auth import HTTPBasicAuth  
        auth = HTTPBasicAuth(os.environ['REGISTRY_USER'], os.environ['REGISTRY_PW'])
    else:
        auth = None

    try:
        r = requests.get(api_url, auth=auth)
        if r.status_code == 401:
            raise Exception('Return Code was 401, Authentication required / not successful!')
        else:
            return r
    except requests.exceptions.RequestException as e:
        raise Exception("Problem during docker registry connection")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
