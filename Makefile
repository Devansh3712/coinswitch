PY = venv/bin/python3

requirements:
	$(PY) -m poetry export -f requirements.txt --output requirements.txt --without-hashes
