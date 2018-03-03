#!/bin/bash -ex
branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
echo $branch
read -p "** Create/update image: ${1:-$branch} [Y/n]" -n 1 -r
echo    # (optional) move to a new line

if [[ $REPLY =~ ^[Yy]$ ]]
then
  docker build -t schoolorchestration/school:${1:-$branch} .
  docker push schoolorchestration/school:${1:-$branch}
fi
