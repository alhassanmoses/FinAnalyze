# ! /bin/bash

# trap ./scripts/docker/shutdown SIGINT SIGTERM EXIT


export MONGODB_DB_NAME="FinAnalyzeAPI"
export AUTH_TOKEN_TTL="60" 
export MONGODB_TEST_DB="finAnalyzeTest"

container=api

while getopts "c:h" opt
do
  case "$opt" in
    c ) container="$OPTARG" ;;
    h ) dockerBashFunction ;;
  esac
done

docker exec backend_api_1

pytest tests/test_*.py

exit_status=$?
if [[ "$exit_status" != "0" ]]; then
  echo -e "${RED}$exit_status test(s) failed${NORMAL}"
else
  echo -e "${GREEN}All tests Passed${NORMAL}"
fi
exit $exit_status