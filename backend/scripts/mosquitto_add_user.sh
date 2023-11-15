#!/bin/bash

USER="$@"
PASSWORD_FILE=/mosquitto/config/password_file

docker compose run --rm broker sh -c "
touch $PASSWORD_FILE
chown root $PASSWORD_FILE
chgrp root $PASSWORD_FILE
chmod 0700 $PASSWORD_FILE
mosquitto_passwd $PASSWORD_FILE $USER
"