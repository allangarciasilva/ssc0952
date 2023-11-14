MOSQUITTO_PASSWORD_FILE=./mosquitto/config/password_file
if [ -d "$MOSQUITTO_PASSWORD_FILE" ] ; then
    rm -rf $MOSQUITTO_PASSWORD_FILE
fi

if [ ! -f "$MOSQUITTO_PASSWORD_FILE" ]; then
    mkdir -p $(dirname $MOSQUITTO_PASSWORD_FILE)
    touch $MOSQUITTO_PASSWORD_FILE
fi

mkdir -p ./proto
cp -u ../proto/*.proto ./proto
docker compose build