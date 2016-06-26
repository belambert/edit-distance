.PHONY: test

all:

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
	python3 setup.py test

coverage:
	python3 -m coverage erase
	python3 -m coverage run setup.py test
	python3 -m coverage html
	python3 -m coverage report
