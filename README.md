# School
A collection of Ansible playbooks for orchestrating and managing a Swarm or Kubernetes (coming soon) cluster

## Getting started

> Zero to cluster in < 10 mins. 

### Step 1. Bootstrap your environment 

This step will setup your control center for your swarm. 

### Step 2. Create your swarm 

```
sh ./school.sh init 
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
