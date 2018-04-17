docker run --rm -it \
    -v ~/.ssh:/root/.ssh \
    -v $(pwd)/settings.yml:/code/ansible/group_vars/all/settings.yml \
    -v $(pwd)/secrets.yml:/code/ansible/group_vars/all/secrets.yml \
    -v $(pwd)/digital_ocean.ini:/etc/ansible/inventory/digital_ocean.ini \
    -e "ANSIBLE_HOST_KEY_CHECKING=False" \
    -e "ANSIBLE_LIBRARY=/etc/ansible/library" \
    -e "ansible_ssh_key=/root/.ssh/id_rsa" \
    -e "ansible_user=$(whoami)" \
    schoolorchestration/school:latest \
    ansible-playbook provision.swarm.yml -i /etc/ansible/inventory/digital_ocean.py