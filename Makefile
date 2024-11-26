run-tests:
	docker-compose up -d && docker-compose exec web /bin/bash -c 'pytest'
