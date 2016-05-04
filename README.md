# docker-registry-frontend

## Run as Docker container

### Preparation

Change the environment variable ``REGISTRY_URL`` in the ``docker-compose.yml`` file.
```
REGISTRY_URL=https://docker-registry.example.com
```

### Base URL
This setting is optional, but if you need to set a base_url with a specified path for your docker-registry frontend, use the variable ``FRONTEND_URL``.
```
FRONTEND_URL=https://registry.example.com/frontend
```


### Basic Authentication

If the docker registry has basic authentication activated, you have to set the following environment variables in the ``docker-compose.yml`` file.
```
REGISTRY_AUTH=True
REGISTRY_USER=<user>
REGISTRY_PW=<password>
```

### Run Container
This will run the frontend application and a proxy container, which will forward your request to the application:

```bash
docker-compose up -d
```

After you've started the containers, the application is available on port 80.


## Debugging
```
docker-compse logs
```

## Run standalone application

### virtualenv

```
# install virtualenv and dependencies
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# set registry url
export REGISTRY_URL=https://docker-registry.example.com

# run application
python app.py
```

## To Do
* Docs> How tu run as standalone app (also with virtualenv)
* Feature> Add a configuration file

## Informations
* [Docker API](https://docs.docker.com/registry/spec/api)


## Features
* List all repositories
* List all tags of a repository
* Show tag details

## Screenshots
To get an overview about the docker-registry frontend, check out the [screenshots directory](screenshots).


## License
This project is licensed under [MIT](http://opensource.org/licenses/MIT).
