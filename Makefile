.PHONY: test


clean:
	python setup.py clean
	rm -f MANIFEST
	rm -rf dist

test:
	python -m unittest discover test
