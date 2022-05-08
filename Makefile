.PHONY: docker

movies:
	poetry run python movie_data_analysis/data/get_data.py
	poetry run python movie_data_analysis/main.py

run:
	poetry run python delta.py

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
