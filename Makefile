.PHONY: docker

run:
	python3 --version
	poetry run python3 delta.py

debug:
	sed -i -e 's/^@profile/#@profile/' delta.py
	sed -i -e 's/profile = True/profile = False/' delta.py
	poetry run python delta.pyi

profile:
	sed -i -e 's/^#@profile/@profile/' delta.py
	sed -i -e 's/profile = False/profile = True/' delta.py
	poetry run kernprof -l delta.py
	poetry run python -m line_profiler delta.py.lprof

docker:
	mv ps_ap_chessgames/data /tmp
	tar czvf apps.tgz delta.py */
	mv /tmp/data ps_ap_chessgames/
	docker build -t oricou/delta .

docker_no_cache:
	mv ps_ap_chessgames/data /tmp
	tar czvf apps.tgz delta.py */
	mv /tmp/data ps_ap_chessgames/
	docker build --no-cache -t oricou/delta .

install:
	docker login
	docker push oricou/delta

docker_run:
	docker run -dit --name delta -p8000:8000 oricou/delta
