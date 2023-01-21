include Make.in

CONFIG=doca.ini

install-doca:
	$(call _info, Installing doca package...)
	pip install . && rm -fr dist build doca.egg-info

create-doca-docs:
	$(call _info, Add new documentation rst files)
	sphinx-apidoc -o docs doca

update-doca-docs:
	$(call _info, Updating documentation for doca package...)
	cd docs && make html && cd ..
	cd docs && make latexpdf && cd ..

update-doca-repo:
	$(call _info, Pushing doca package to origin...)
	git pull origin --all

start-doca:
	$(call _info, Starting doca pipeline...)
	doca -c ${CONFIG}

build-image:
	docker build --rm -t ${PROJECT_NAME}/python:latest .
	docker system prune -f
