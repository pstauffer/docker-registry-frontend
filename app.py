from flask import Flask
from flask import render_template
import requests
import json
import urllib2

app = Flask(__name__)

baseurl = 'https://docker-registry.example.com/v2/'
list_repos = '_catalog'
list_tags = 'tags/list'

tags_url = 'https://gist.githubusercontent.com/pstauffer/1d6b652cdbeae88f535e8fca123d6e07/raw/bbd207069a3977480ffdfbe10874b8080a1c655f/registry%2520tags%2520json'
repo_url = 'https://gist.githubusercontent.com/pstauffer/846e6783b1d07166ed8880d4e3373296/raw/7a52f91ed73879bc24ab8d87e625dd8b1528adc7/json%2520output'

@app.route("/")
def index():
    r = requests.get(repo_url)
    j = r.json()
    images = j['repositories']
    return render_template('index.html', images=images)

@app.route("/image/<namespace>/<image>")
@app.route("/image/<image>")
def tags(image,namespace=None):
    r = requests.get(tags_url)
    j = r.json()
    tags = j['tags']
    return render_template('image.html', image=image, namespace=namespace, tags=tags)


if __name__ == "__main__":
    app.run(debug=True)
