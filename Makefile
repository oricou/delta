run:
	poetry run python delta.py

docker:
	tar czvf apps.tgz delta.py */
	docker build -t bicente/gragas .

docker_no_cache:
	tar czvf apps.tgz delta.py */
	docker build --no-cache -t bicente/gragas .

install:
	docker login
	docker push bicente/gragas

docker_run:
	docker run -dit --name gragas -p8000:8000 bicente/gragas
