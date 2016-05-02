from flask import Flask, render_template

from requests import Session, RequestException
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    r = registry_request('_catalog')
    j = r.json()
    images = j['repositories']
    return render_template('index.html', images=images)

@app.route('/image/<path:image>')
def tags(image):
    r = registry_request(image + '/tags/list')
    j = r.json()
    tags = j['tags']
    return render_template('image.html', image=image, tags=tags, registry=os.environ['REGISTRY_URL'])

def registry_request(path):
    api_url = os.environ['REGISTRY_URL'] + '/v2/' + path

    try:
        r = s.get(api_url)
        if r.status_code == 401:
            raise Exception('Return Code was 401, Authentication required / not successful!')
        else:
            return r
    except RequestException:
        raise Exception("Problem during docker registry connection")

if __name__ == "__main__":
    s = Session()

    # if not set, set authentication default value to False
    REGISTRY_AUTH = os.environ.get('REGISTRY_AUTH',False)

    if REGISTRY_AUTH == "True" or REGISTRY_AUTH == "true":
        s.auth = (os.environ['REGISTRY_USER'], os.environ['REGISTRY_PW'])

    app.run(host='0.0.0.0', debug=True)
