import logging
import os
import shlex
import ssl
import subprocess

import aiomqtt
from fastapi import FastAPI

from src.shared.settings import SETTINGS


def create_file_logger(filename: str):
    filename = os.path.abspath(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    logger = logging.getLogger(filename)
    fh = logging.FileHandler(filename)

    logger.setLevel(logging.INFO)
    fh.setLevel(logging.INFO)

    logger.addHandler(fh)
    return logger


def run_app(app: FastAPI | str, port: int):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port, reload=SETTINGS.debug)


def download_ca_certificate(output_file: str):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    url = shlex.quote(f"{SETTINGS.mosquitto_host}:{SETTINGS.mosquitto_port}")
    output_file = shlex.quote(output_file)
    script = f"openssl s_client -connect {url} -showcerts < /dev/null | openssl x509 -outform PEM > {output_file}"
    subprocess.run(script, shell=True, stdout=subprocess.PIPE)


def create_mqtt_client():
    cert_file = os.path.abspath("./data/certificate.pem")
    download_ca_certificate(cert_file)
    tls_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cert_file)
    return aiomqtt.Client(SETTINGS.mosquitto_host, SETTINGS.mosquitto_port, username=SETTINGS.mosquitto_user,
                          password=SETTINGS.mosquitto_password, tls_context=tls_context, tls_insecure=True)
