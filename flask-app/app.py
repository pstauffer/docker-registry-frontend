from flask import Flask, render_template

from requests import Session, RequestException
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    r = registry_request('_catalog')
    j = r.json()

    return frontend_template('index.html', images=j['repositories'])

@app.route('/image/<path:image>')
def tags(image):
    r = registry_request(image + '/tags/list')
    j = r.json()

    kwargs = {
        'tags': j['tags'],
        'image': image,
        'registry': os.environ['REGISTRY_URL'],
    }

    return frontend_template('image.html', **kwargs)


def frontend_template(template, **kwargs):
    '''
    Wrapper function around the flask render_template function
    to always set the frontend_url for the view.
    '''
    return render_template(template, frontend_url=FRONTEND_URL, **kwargs)


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

    # get authentication state or set default value
    REGISTRY_AUTH = os.environ.get('REGISTRY_AUTH',False)

    # get base_url or set default value
    FRONTEND_URL = os.getenv('FRONTEND_URL','/')

    if REGISTRY_AUTH == "True" or REGISTRY_AUTH == "true":
        s.auth = (os.environ['REGISTRY_USER'], os.environ['REGISTRY_PW'])

    print os.environ['REGISTRY_URL']

    app.run(host='0.0.0.0', debug=True)
