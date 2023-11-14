CERT_PATH=./mosquitto/certs
if [ ! -d "$CERT_PATH" ] ; then
    rm -rf $CERT_PATH
fi
mkdir -p $CERT_PATH

openssl genrsa -des3 -out $CERT_PATH/ca.key 2048
openssl req -new -x509 -days 1826 -key $CERT_PATH/ca.key -out $CERT_PATH/ca.crt -config openssl.cnf
openssl genrsa -out $CERT_PATH/server.key 2048
openssl req -new -out $CERT_PATH/server.csr -key $CERT_PATH/server.key -config openssl.cnf
openssl x509 -req -in $CERT_PATH/server.csr -CA $CERT_PATH/ca.crt -CAkey $CERT_PATH/ca.key -CAcreateserial -out $CERT_PATH/server.crt -days 360

# adicionar no mosquitto.config:



# adicionar no código da esp:
# no começo, colocar o conteudo de server.crt:
# const char* CA_cert = \
# "-----BEGIN CERTIFICATE-----\n" \
# "MIIDhjCCAm4CFFWtvjXIZjRJmNrZRyACTnDdcqBoMA0GCSqGSIb3DQEBCwUAMIGE\n" \
# "MQswCQYDVQQGEwJCUjELMAkGA1UECAwCU1AxDjAMBgNVBAcMBXRlc3RlMQ4wDAYD\n" \
# "VQQKDAV0ZXN0ZTEOMAwGA1UECwwFdGVzdGUxGDAWBgNVBAMMDzE0My4xMDcuMjMy\n" \
# "LjI1MjEeMBwGCSqGSIb3DQEJARYPdGVzdGVAdGVzdGUuY29tMB4XDTIzMTExNDE3\n" \
# "MDA1NVoXDTI0MTEwODE3MDA1NVowejELMAkGA1UEBhMCQlIxCzAJBgNVBAgMAlNQ\n" \
# "MQ4wDAYDVQQHDAV0ZXN0ZTEOMAwGA1UECgwFdGVzdGUxDjAMBgNVBAsMBXRlc3Rl\n" \
# "MRgwFgYDVQQDDA8xNDMuMTA3LjIzMi4yNTIxFDASBgkqhkiG9w0BCQEWBXRlc3Rl\n" \
# "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtDnhsSmlTqyBhLo9YUcv\n" \
# "6ppdu2ejV0nbAJPghxNJ1SjvRdFBtb/sHPI0bOMNTE6CGKvqRMiY085xqkuTzMHw\n" \
# "sIryWEHkZiBZc8SJ3zXSSAt4ZKmrYWK2y5WVuKa8CxrWvn1bbK6OrnNipPQnGVHJ\n" \
# "57nLRL0qOaRjF2RgpNbzqJrvLc2GjO+qDWfFpaVlJ0j3tHCjdjrjPtILmX8115ii\n" \
# "BFhcsBBHd7civXUhUHrY0BoJesTn8ZQa/saoVde86+H7XIDYjYYElXhi96dGMOMe\n" \
# "C8YiD7T9WT5rEBb7pwongs6+kdwStYT1ljp+gzTj7na+LXhKvgedGqQaMIkr5rdD\n" \
# "MwIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQCPgfMADz5iJ88sur6QvEFXSf7PTiX2\n" \
# "aF3UJOxHHqGaG7aubS7a8bCFWInN51+CeY12V4HHCgYf3JCsCFgvFBIXj5UjHnCE\n" \
# "44E9MvG5lNkwTkrW9PhyvXjbrQeGaFg8saKYjcyHTO8mFgE6nLmtNcw/JhCRjh1Q\n" \
# "6NqicjcagyRORfXNI5gmFZ0cPNWGVAWsEy9dlGmuU7eEfUVLeZrMzDvdaizppAHH\n" \
# "Pz/prjUIaOU++MHSImZFNXr4YWJK28wZ7chi8MZoXwvW8T3RUI3JfPTDxtglUN/0\n" \
# "Lbu8CZ7WaioZd3fg6xp2JswnCDMKbYkuaOXfLpN6TZZQ/5bVhqHlwjYe\n" \
# "-----END CERTIFICATE-----";

# em setup:
# client.setCACert(CA_cert);