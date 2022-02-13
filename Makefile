gen-docs:
	pip3 install -r docs/requirements.txt
	cd docs; make html
build:
	python3 -m pip install --upgrade build
	python3 -m build
release:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
