#
#  Makefile
#
#  Central entry point for running the solution.
#

default: test

test: .venv
	.venv/bin/locust -f locust_tests/locust_test.py --host http://localhost:8001/

flake8: .venv
	.venv/bin/flake8 bidder/app/*.py bidder/streamer/*.py

black: .venv
	.venv/bin/black bidder/app/*.py bidder/streamer/*.py
	rm -fr .venv

.venv: test_requirements.txt
	python3 -m venv .venv
	.venv/bin/pip install -r test_requirements.txt
	touch .venv

up: .venv
	docker-compose up -d

clearenv: 
	rm -fr .venv 
	docker-compose down



