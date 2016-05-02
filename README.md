# docker-registry-frontend

## Run as Docker container

### Preparation

Change the environment variable ``REGISTRY_URL`` in the ``docker-compose.yml`` file.
```
REGISTRY_URL=https://docker-registry.example.com
```

### Basic Authentication

If the docker registry has basic authentication activated, you have to set the following environment variables in the ``docker-compose.yml`` file.
```
REGISTRY_AUTH=True
REGISTRY_USER=<user>
REGISTRY_PW=<password>
```

### Run
This will run the frontend application and a proxy container, which will forward your request to the application:

```bash
docker-compose up -d
```

After you've started the containers, the application is available on port 80.


## Debug
```
docker-compse logs
```


## To Do

* [ ] curl -i HEAD https://xxx.example.com/v2/debian/manifests/latest -> https://gist.github.com/pstauffer/ab2e1486c680539a87b5d3a069c71a21
* [ ] Home Button
* [ ] Navigation
* [ ] About Page

## Informations
* [Docker API](https://docs.docker.com/registry/spec/api)


## License
This project is licensed under `MIT <http://opensource.org/licenses/MIT>`_.
