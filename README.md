# School
A collection of Ansible playbooks for orchestrating and managing a Swarm or Kubernetes (coming soon) cluster

## Getting started

> Zero to cluster in < 10 mins.

### Step 1. Bootstrap your environment

Setup you ENvironment
```bash
docker-compose run --rm school ansible-playbook bootstrap.yml 
```
This step will setup your control center for your swarm.

```
# prod
.. long docker run command goes here ..

# dev
docker-compose run --rm school ansible-playbook bootstrap.yml
```

### Step 2. Create your swarm

```
# prod
sh ./school.sh init

# dev
docker-compose run --rm school ansible-playbook provision.swarm.node.yml -i inventory/digital_ocean.py
```

### Step 3. Start running some services in your swarm

```
sh ./school.sh scaffold
```

### Step 4. Next steps

* Create a swarm node snapshot


## Maintaining your swarm:

Maintenance tasks:

* Roll servers
* Resize the swarm
* ...
