# Backend e Broker MQTT

Inicialmente, copie para o contexto atual os arquivos necessários:

```shell
cp ../config.env .env
```

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