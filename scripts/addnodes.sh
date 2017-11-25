#!/bin/bash -ex
docker-compose run --rm school ansible-playbook manage.create.nodes.yml -i inventory/digital_ocean.py
docker-compose run --rm school ansible-playbook manage.join.nodes.yml -i inventory/digital_ocean.py -e ansible_user=$(whoami)