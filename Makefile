init:
	pip install pipenv --user
	pipenv install --dev

test:
	pipenv run python test_tboard.py -v
