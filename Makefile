run-tests:
	docker-compose exec web /bin/bash -c 'pytest $(path)'


docker-run-tests:
	docker-compose build && \
	docker-compose up -d && \
	trap 'docker-compose stop' EXIT && \
	docker-compose exec web /bin/bash -c 'pytest $(path)'
