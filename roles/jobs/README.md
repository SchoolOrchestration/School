Role Name
=========

Job's are used to run a container that performs and admin task (i.e DB backups or Single time jobs like migrations)

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------


needed variables:
- **job_name**: The name of the job (required)
- **job_image**: docker image of the job (required)
- **job_environment**: list of name and values
- **job_command**: the command to run in the container
- **job_replicas**: The amount of containerized jobs to run
- **job_repeat**: The interval at which the job must run

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
