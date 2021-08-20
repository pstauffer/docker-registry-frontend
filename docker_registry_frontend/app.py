from flask import Flask, g
import pendulum
from werkzeug.routing import BaseConverter

from utils import (
    get_all_repositories,
    frontend_template,
    process_manifest_data,
    registry_request,
)

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route("/")
def index():
    return frontend_template('index.html', images=get_all_repositories(g.config.get('max_repositories')))


@app.route('/image/<path:image>')
def image_detail(image):
    response = registry_request(image + '/tags/list')
    data = response.json()

    kwargs = {
        'tags': data['tags'] if data['tags'] else [],
        'image': image,
        'registry': g.config.get('registry_host'),
    }

    return frontend_template('image.html', **kwargs)


@app.route('/image/<path:image>/tag/<tag>')
def image_tag_detail(image, tag):
    response = registry_request(image + '/manifests/' + tag)
    data = response.json()

    history, tag_detail = process_manifest_data(data)

    kwargs = {
        'tag': tag,
        'image': image,
        'layers': len(data['fsLayers']),
        'history': reversed(history),
        'labels': tag_detail.get('config', {}).get('Labels', {}),
        'tag_detail': tag_detail,
        'created': pendulum.parse(tag_detail.get('created')).diff_for_humans(),
    }

    return frontend_template('tag.html', **kwargs)
