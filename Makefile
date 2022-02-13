.PHONY: gen-docs
gen-docs:
	pip3 install -r docs/requirements.txt
	cd docs; make html

.PHONY: build
build:
	python3 -m pip install --upgrade build
	python3 -m build

.PHONY: release
release: build
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
