# Backend e Broker MQTT

Inicialmente, copie para o contexto atual os arquivos necessários:

```shell
cp ../config.env .env
```

## Configuração do TLS/SSL

É necessário configurar alguns dados para a criação do certificado SSL. O arquivo `openssl.cnf` pode ser mantido quase inteiramente inalterado, mas certifique-se que o campo `CN` possui o IP (não pode ser URL por compatibilidade com a ESP) do servidor em que será hospedado. O arquivo `openssl.cnf` é funcional e contém essas configurações, assumindo que o IP é `143.107.232.252`.

## Execução do Broker

Para executar o broker MQTT, é suficiente baixar a sua imagem do Docker Hub e depois executá-lo

```shell
docker compose build
docker compose up broker -d # Sobe o container em modo detached
```

Podemos acompanhar a saída para verificar se está tudo certo:

```shell
docker compose logs -f broker
```