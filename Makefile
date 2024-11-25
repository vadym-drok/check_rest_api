run-tests:
	docker-compose up -d && docker-compose exec web /bin/bash -c 'pytest'
	#docker-compose up -d
	#docker-compose exec -it web /bin/bash