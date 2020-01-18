install:
	python3 -m venv .
	source bin/activate
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

activate:
	source bin/activate

quit:
	deactivate