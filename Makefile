regenerate-requirements:
	pip-compile requirements/requirements.in -o requirements/requirements.txt

install:
	python setup.py install && rm -rf build dist slack.egg-info