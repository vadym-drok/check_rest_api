run-tests:
	docker-compose exec web /bin/bash -c 'pytest $(path)'
