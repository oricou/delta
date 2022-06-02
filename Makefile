.PHONY: docker

run:
	python3 --version
	poetry run python3 delta.py

docker:
	tar czvf apps.tgz delta.py */
	docker build -t oricou/delta .

docker_no_cache:
	tar czvf apps.tgz delta.py */
	docker build --no-cache -t oricou/delta .

install:
	docker login
	docker push oricou/delta

docker_run:
	docker run -dit --name delta -p8000:8000 oricou/delta
