import json
import os

from dogpile.cache import make_region
from flask import Flask, render_template
import pendulum
from requests import Session, RequestException
from werkzeug.routing import BaseConverter

MAX_REPOSITORIES = 1000

app = Flask(__name__)
region = make_region().configure(
    'dogpile.cache.memory_pickle'
)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@region.cache_on_arguments()
def get_all_repositories():
    response = registry_request('_catalog?n={}'.format(MAX_REPOSITORIES))
    data = response.json()
    return data['repositories']


@app.route("/")
def index():
    return frontend_template('index.html', images=get_all_repositories())


@app.route('/image/<path:image>')
def image_detail(image):
    response = registry_request(image + '/tags/list')
    data = response.json()

    kwargs = {
        'tags': data['tags'],
        'image': image,
        'registry': os.environ['REGISTRY_URL'],
    }

    return frontend_template('image.html', **kwargs)


@app.route('/image/<path:image>/tag/<tag>')
def image_tag_detail(image, tag):
    response = registry_request(image + '/manifests/' + tag)
    data = response.json()

    history = []
    tag_detail = {}
    if data.get('history'):
        for item in data.get('history', []):
            if item.get('v1Compatibility'):
                raw = json.loads(item['v1Compatibility'])
                if not tag_detail:
                    tag_detail = raw
                cmds = raw.get('container_config', {}).get('Cmd', '')
                if cmds:
                    for cmd in cmds:
                        cmd = cmd.replace('/bin/sh -c #(nop) ', '')
                        cmd = cmd.replace('/bin/sh -c ', 'CMD ')
                        history.append(cmd)

    kwargs = {
        'tag': tag,
        'image': image,
        'layers': len(data['fsLayers']),
        'history': reversed(history),
        'tag_detail': tag_detail,
        'created': pendulum.parse(tag_detail.get('created')).diff_for_humans(),
    }

    return frontend_template('tag.html', **kwargs)


def frontend_template(template, **kwargs):
    '''
    Wrapper function around the flask render_template function
    to always set the frontend_url for the view.
    '''
    return render_template(template, frontend_url=FRONTEND_URL, **kwargs)


def registry_request(path, method="GET"):
    api_url = os.environ['REGISTRY_URL'] + '/v2/' + path

    try:
        response = getattr(session, method.lower())(api_url, verify=False)
        if response.status_code == 401:
            raise Exception('Return Code was 401, Authentication required / not successful!')
        else:
            return response
    except RequestException:
        raise Exception("Problem during docker registry connection")


if __name__ == "__main__":
    session = Session()

    # get authentication state or set default value
    REGISTRY_AUTH = os.environ.get('REGISTRY_AUTH', False)

    # get base_url or set default value
    FRONTEND_URL = os.getenv('FRONTEND_URL', '/')
    if not FRONTEND_URL.endswith('/'):
        FRONTEND_URL = FRONTEND_URL + "/"

    if REGISTRY_AUTH == "True" or REGISTRY_AUTH == "true":
        session.auth = (os.environ['REGISTRY_USER'], os.environ['REGISTRY_PW'])

    print("Registry URL: " + os.environ['REGISTRY_URL'])
    print("Frontend URL: " + FRONTEND_URL)

    app.run(host='0.0.0.0', debug=True)
