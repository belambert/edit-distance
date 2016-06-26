.PHONY: test

clean:
	python setup.py clean
	rm -f MANIFEST
	rm -rf dist
	rm -rf edit_distance.egg-info/
	rm -rf build
	find . -name __pycache__ -exec rm -rf '{}' \;
	find . -name *.pyc -exec rm -rf '{}' \;

test:
	python -m unittest discover test
