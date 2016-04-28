FROM pstauffer/python3

MAINTAINER confirm IT solutions, pstauffer

COPY flask-app/requirements.txt /requirements.txt
COPY flask-app/app.py /app.py

EXPOSE 5000

RUN pip install --no-cache-dir -r /requirements.txt && \
    mkdir /templates

COPY flask-app/templates/* /templates/

CMD python /app.py
