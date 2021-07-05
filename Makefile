# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | \
		awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {\
			split(\$$1,A,/ /);for(i in A)print A[i]\
		}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"

# required for list
no_targets__:

VERSION=$$(poetry version -s)
PROJECT="bhagavad-gita-api"
DOCKER_ORG="bhagavadgita"
DOCKER_REPO="$(DOCKER_ORG)/$(PROJECT)"

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

fmt: clean
	@poetry run isort .
	@poetry run black .

hard-clean: clean
	@rm -rf .venv

pypi:
	@poetry publish --build

docker:
	@docker build -t $(PROJECT) .
	@docker tag $(PROJECT) $(DOCKER_REPO):latest
	@docker tag $(PROJECT) $(DOCKER_REPO):$(VERSION)

docker-release: docker
	@docker push -a $(DOCKER_REPO)

release: pypi docker-release
