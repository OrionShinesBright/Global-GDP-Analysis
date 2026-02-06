all:
	ruff check
	ruff format
	python dashboard.py
	rm -rf __pycache__/ .ruff_cache/

run:
	python dashboard.py

check:
	ruff check

format:
	ruff format

clean:
	rm -rf __pycache__/ .ruff_cache/
