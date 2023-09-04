# ! /bin/bash

# trap ./scripts/docker/shutdown SIGINT SIGTERM EXIT

dockerBashFunction(){
  echo -e "Usage: $0 -c [container]"
  echo -e "\t-c container to run bash into e.g (api, mongodb). Defaults to api"
  exit 1
}

container=api

while getopts "c:h" opt
do
  case "$opt" in
    c ) container="$OPTARG" ;;
    h ) dockerBashFunction ;;
  esac
done

docker-compose run --entrypoint=bash $container
