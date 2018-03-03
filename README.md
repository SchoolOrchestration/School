# School
A collection of Ansible playbooks for orchestrating and managing a Swarm or Kubernetes (coming soon) cluster

## Getting started

> Zero to cluster in < 10 mins.

### Step 1. Bootstrap your environment

Setup you Environment
```bash
#prod:
docker run -it --rm -v $(pwd):/code/configs schoolorchestration/school ansible-playbook bootstrap.yml
```

This step will setup your control center for your swarm.

Now, let's build our first node:

```
sh ./prepare.sh
```

This will ask you some questions, then go about launching a droplet in DigitalOcean.
It will secure the droplet and then create a snapshot. This snapshot will form the basis of new nodes which we join to the swarm

You should be able to ssh into this droplet without specifying a user. e.g.: `ssh 1.2.3.4`

----
### it works up to here

Now that we have our base snapshot, let's go ahead and make our swarm

```
sh ./swarm.sh
```

This will ask you some questions about the size of your swarm and stuff, and then go about creating some droplets.


### Step 3. Start running some services in your swarm

```
sh ./school.sh scaffold
```

### Step 4. Next steps

* Create a swarm node snapshot


## Managing your swarm:

### Add a node:

```
# prod (TBD)
# add three nodes:
sh ./school.sh add --count=3

# dev
docker-compose run --rm school sh /code/scripts/addnodes.sh
```

### Cleanly remove a node from the swarm:

```
# prod
sh ./school.sh remove --hostname=swarm-subtly-full-drake --ip=1.2.3.4 --with-delete

# dev

# remove the node from the swarm:
docker-compose run --rm school ansible-playbook manage.remove.node.yml -i inventory/digital_ocean.py -e ansible_user=$(whoami)

# delete the node
docker-compose run --rm school ansible-playbook manage.delete.node.yml -i inventory/digital_ocean.py -e ansible_user=$(whoami)
```

Maintenance tasks:

* Roll servers
* Resize the swarm
* ...
