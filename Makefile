test:
	python -m unittest

black:
	black -l 120 watersnake/
	black -l 120 tests/