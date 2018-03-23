PROJECT:=$(shell gcloud config list project --format="value(core.project)")
PASSWORD:=$(shell openssl rand -hex 28 | base64)

.PHONY: templates
templates:
	sed "s/<PASSWORD>/${PASSWORD}/g" secrets.yaml.tmpl > secrets.yaml
	sed "s/<PROJECT>/${PROJECT}/g" guestbook.yaml.tmpl > guestbook.yaml
	sed "s/<PROJECT>/${PROJECT}/g" celery.yaml.tmpl > celery.yaml
	sed "s/<PROJECT>/${PROJECT}/g" postgres.yaml.tmpl > postgres.yaml
	sed "s/<PROJECT>/${PROJECT}/g" redis.yaml.tmpl > redis.yaml

.PHONY: clean
clean:
	rm -f *.yaml
