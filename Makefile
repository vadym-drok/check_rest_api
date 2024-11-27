run-tests:
	docker-compose up -d && \
	trap 'docker-compose stop' EXIT && \
	docker-compose exec web /bin/bash -c 'pytest $(path)'
