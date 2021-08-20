import logging
import os
import re

from flask import g
from requests import Session

from app import app


def main():
    registry_url = os.environ['REGISTRY_URL']

    # get authentication state or set default value
    registry_auth = os.environ.get('REGISTRY_AUTH', False)

    if os.environ.get('REGISTRY_VERIFY_SSL') == '0':
        registry_verify_ssl = False
    else:
        registry_verify_ssl = True

    # get base_url or set default value
    frontend_url = os.environ.get('FRONTEND_URL', '/')
    if not frontend_url.endswith('/'):
        frontend_url = frontend_url + "/"

    @app.before_request
    def prepare_context():
        g.session = Session()
        g.config = {
            'registry_url': registry_url,
            'registry_host': re.sub('https?://', '', registry_url),
            'registry_verify_ssl': registry_verify_ssl,
            'frontend_url': frontend_url,
            'max_repositories': int(os.environ.get('MAX_REPOSITORIES', 1000)),
        }

        if registry_auth == "True" or registry_auth == "true":
            g.session.auth = (os.environ['REGISTRY_USER'], os.environ['REGISTRY_PW'])

    print("Registry URL: " + registry_url)
    print("Frontend URL: " + frontend_url)

    debug = os.environ.get('DEBUG')
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    app.run(host='0.0.0.0', debug=debug)


if __name__ == '__main__':
    main()
