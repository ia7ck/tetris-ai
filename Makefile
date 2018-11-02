init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run python test_tboard.py -v
