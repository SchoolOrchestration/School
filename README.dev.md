# School

This is documentation for working on these plays at Dev time

School infrastructure works on the concept of layers:

**Create**

1. Create droplet/s
2. harden / secure
3. user access

**Prepare/Purpose**

1. Install software

**Use**

1. Deploy apps

## Create node/s:

This simply refers to creating nodes. Will create droplets and secure them

```
ansible-playbook manage.create.nodes.yml -i inventory/digital_ocean.py -e 'host_key_checking=False'
```

**Tags and limits:**

* `--limit='harden_required'` = only run harden
* Harden tags: `users`, `firewall`, `harden_ssh`

**Examples**

**Run harden on a collection of nodes which did not complete processing**

If you ran the command above, and for some reason it failed before completing hardening, you can run just the harden script with:

```
ansible-playbook manage.create.nodes.yml -i inventory/digital_ocean.py --limit=harden_required -e 'host_key_checking=False ansible_ssh_user=root'
```

* Note: you will need to set ssh user to root the first time when you run harden


**Update users with access**

Edit the value of `ssh_users` (in `group_vars/all.yml`)

```
ansible-playbook manage.users.yml -i inventory/digital_ocean.py
```

Will update access to all boxes. Optionally limit with `--limit`

## Prepare nodes

Preparing nodes means preparing them for their purpose (e.g.: database (postgres etc, docker (swarm, k8s) etc))

## Delete nodes

Will delete any nodes tagged with `remove`

```
ansible-playbook manage.delete.node.yml -i inventory/digital_ocean.py
```

## Recipes

Things which may require a couple of plays

### Start a swarm

```
# create the original node:
ansible-playbook manage.create.nodes.yml -i inventory/digital_ocean.py -e 'host_key_checking=False node_count=1 tags=harden_required,server_swarm,server_swarm_manager,test_swarm dodroplet_purpose=swarm'

# Init the swarm:
ansible-playbook manage.swarm.create.yml -i inventory/digital_ocean.py
```

### Manage a swarm

Once you've set up a basic swarm, you can manage it's state with tags:

The following tags are important:

* `server_swarm`: Part of the swarm (will join as a worker by default)
* `server_swarm_worker`: Worker in a swarm
* `server_swarm_manager`: Manager in a swarm
* `server_swarm_remove`: Remove a node from a swarm

```
ansible-playbook manage.swarm.yml -i inventory/digital_ocean.py
```

**Notes:**

* Tags execute in order. So, if a node has: `server_swarm_worker` and `server_swarm_manager`, it will be a manager.
* _anything_ tagged with `server_swarm_remove` will be removed

### Manage a postgres cluster

**Create**

This example will create a 3 node cluser. 1x master and 2x slaves (in different regions)

**Create the master node**
```
ansible-playbook manage.create.nodes.yml -i inventory/digital_ocean.py -e 'host_key_checking=False node_count=1 tags=harden_required,pg_master,server_database dodroplet_purpose=postgres'
```

**Create the slaves**
```
ansible-playbook manage.create.nodes.yml -i inventory/digital_ocean.py -e 'host_key_checking=False node_count=2 tags=harden_required,pg_slave,server_database dodroplet_purpose=postgres'
```

Head over to `SchoolData` and run the playbook

```
# setup master with slaving:
ansible-playbook datas.yml -i inventory/digital_ocean.py
# verify replication is working:
ansible-playbook verify_replication.yml -i inventory/digital_ocean.py
```
