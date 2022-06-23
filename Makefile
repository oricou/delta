.PHONY: docker

debug:
	sed -i -e 's/^@profile/#@profile/' delta.py
	sed -i -e 's/profile = True/profile = False/' delta.py
	poetry run python delta.py

run:
	sed -i -e 's/^@profile/#@profile/' delta.py
	sed -i -e 's/profile = True/profile = False/' delta.py
	#poetry run gunicorn --workers 1 -b 0.0.0.0:8000 delta:server
	poetry run gunicorn --timeout 360 --workers 1 -b 0.0.0.0:8000 delta:server

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
	docker run -it --name delta -p8000:8000 oricou/delta
