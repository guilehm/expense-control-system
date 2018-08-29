lint:
	@flake8
	@isort --check

test: 
	py.test -v
