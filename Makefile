gen-docs:
	pip3 install -r docs/requirements.txt
	cd docs; make html
install:
	python3 setup.py build
	python3 setup.py install
release:
	python3 setup.py register
	python3 setup.py sdist upload
