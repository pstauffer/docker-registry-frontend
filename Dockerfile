FROM pstauffer/python3

MAINTAINER confirm IT solutions, pstauffer

RUN addgroup -g 666 flask && \
    adduser -u 666 -G flask -h /home/flask -g "flask User" -s /bin/sh -D flask && \
    mkdir /home/flask/templates

COPY flask-app/requirements.txt /home/flask/requirements.txt
COPY flask-app/app.py /home/flask/app.py
COPY flask-app/templates/* /home/flask/templates/

EXPOSE 5000

RUN pip install --no-cache-dir -r /home/flask/requirements.txt && \
    chown -R flask:flask /home/flask && \
    chmod -R o-rwx /home/flask

USER flask

CMD python /home/flask/app.py
