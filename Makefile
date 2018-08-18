
build:
	docker build . -t boardgamenightbackend

serve_test:
	docker run --env-file ~/.boardgamenight -p 5000:5000 -v $(shell pwd):/app -ti boardgamenightbackend ./app.py

