env:
	python3 -m venv .

init:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt
