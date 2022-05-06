run:
	poetry run python delta.py

docker:
	tar czvf apps.tgz delta.py */
	docker build -t bicente/lambda .

docker_no_cache:
	tar czvf apps.tgz delta.py */
	docker build --no-cache -t bicente/lambda .

install:
	docker login
	docker push bicente/lambda

docker_run:
	docker run -dit --name lambda -p8000:8000 bicente/lambda
