IMAGE_NAME := liexpress

build:
	docker build -t $(IMAGE_NAME) .

test:
	python3 -m pytest tests/

run:
	docker-compose up --build
