import html
import json
import logging
import os
import re

from dogpile.cache import make_region
from flask import g, render_template
from requests import RequestException

EXPIRATION_TIME = int(os.environ.get('CACHE_EXPIRATION', 600))

region = make_region().configure(
    'dogpile.cache.memory_pickle',
    expiration_time=EXPIRATION_TIME,
)


@region.cache_on_arguments()
def get_all_repositories(max_repositories):
    response = registry_request('_catalog?n={}'.format(max_repositories))
    data = response.json()
    return data['repositories']


def process_manifest_data(data):
    hightlights = [
        r'^(FROM)', r'^(MAINTAINER)', r'^(RUN)', r'^(ADD)',
        r'^(COPY)', r'^(EXPOSE)', r'^(USER)', r'^(ENTRYPOINT)',
        r'^(CMD)', r'^(ENV)', r'^(VOLUME)', r'^(LABEL)', r'^(ARG)'
    ]

    replacements = {
        r'^/bin/sh -c #\(nop\) ': '',
        r'^/bin/sh -c ': 'RUN ',
        r'^/bin/sh': '',
        r'^-c': '',
        r'^#\(nop\)': ''
    }

    def process_cmds(cmds):
        if not cmds:
            raise StopIteration()
        for cmd in cmds:
            cmd = html.escape(cmd)
            for key in replacements:
                cmd = re.sub(key, replacements[key], cmd).strip()
            for highlight in hightlights:
                cmd = re.sub(highlight, r'<span class="highlight">\1</span>', cmd)
            if cmd:
                yield cmd

    history = []
    tag_detail = {}
    if data.get('history'):
        for item in data.get('history', []):
            if item.get('v1Compatibility'):
                raw = json.loads(item['v1Compatibility'])
                if not tag_detail:
                    tag_detail = raw
                cmds = raw.get('container_config', {}).get('Cmd', '')
                history.extend(process_cmds(cmds))

    return history, tag_detail


def registry_request(path, method="GET"):
    api_url = os.environ['REGISTRY_URL'] + '/v2/' + path

    try:
        logging.debug('%s %s verify=%s', method.upper(), api_url, g.config.get('registry_verify_ssl'))
        response = getattr(g.session, method.lower())(api_url, verify=g.config.get('registry_verify_ssl'))
        if response.status_code == 401:
            raise Exception('Return Code was 401, Authentication required / not successful!')
        else:
            return response
    except RequestException:
        logging.exception('registry request')
        raise Exception("Problem during docker registry connection")


def frontend_template(template, **kwargs):
    '''
    Wrapper function around the flask render_template function
    to always set the frontend_url for the view.
    '''
    return render_template(template, frontend_url=g.config.get('frontend_url'), **kwargs)
