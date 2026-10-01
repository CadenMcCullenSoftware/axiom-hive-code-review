.PHONY: test check

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

check:
	python3 -m compileall -q src tests
	$(MAKE) test
