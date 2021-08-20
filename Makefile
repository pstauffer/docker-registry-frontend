
run-devel: prepare
	DEBUG=1 .venv/bin/python docker_registry_frontend/run.py

prepare:
	python -m venv .venv
	.venv/bin/python -m pip install -r docker_registry_frontend/requirements.txt
