.PHONY: test

clean:
	python setup.py clean
	rm -f MANIFEST
	rm -rf dist
	rm -f *.pyc

test:
	python -m unittest discover test
