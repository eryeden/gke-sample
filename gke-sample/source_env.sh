#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

GCS_CREDENTIALS="${SCRIPT_DIR}/asset/service-account-file.json"

# Populate the service-account-file.json for GCS
if [ -f "${GCS_CREDENTIALS}" ]; then
  export GOOGLE_APPLICATION_CREDENTIALS=${GCS_CREDENTIALS}
else
  printf "${GCS_CREDENTIALS} file is not found.
Please follow https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication
And place service-account-file.json under asset directory.
"
fi