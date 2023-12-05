FROM eclipse-mosquitto:2.0

RUN apk upgrade --update-cache --available && \
    apk add openssl && \
    rm -rf /var/cache/apk/*

COPY ./static/run.sh /run.sh

CMD ["sh", "run.sh"]
