
build:
	docker build . -t boardgamenightbackend

serve_test:
	docker run --env-file ~/.boardgamenight -p 5000:5000 -v $(shell pwd):/app -ti boardgamenightbackend ./app.py


production:
	docker stop boardgamenight_backend || true
	sleep .2
	docker rm -f boardgamenight_backend || true
	docker run --env-file ~/.boardgamenight -p 5000:5000 -d --name boardgamenight_backend  boardgamenightbackend ./app.py


