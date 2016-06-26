.PHONY: test

all:
	python --version

clean:
	python setup.py clean
	rm -f MANIFEST
	rm -rf dist
	rm -rf edit_distance.egg-info/
	rm -rf build
	rm -rf htmlcov
	find . -name *.pyc -exec rm -rf '{}' \;

doc:
	pydoc -w `find edit_distance -name '*.py'`

showdoc:
	pydoc `find edit_distance -name '*.py'`

test:
	python setup.py test

coverage:
	python -m coverage erase
	python -m coverage run setup.py test
	python -m coverage html
	python -m coverage report
