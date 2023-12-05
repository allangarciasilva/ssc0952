# Backend e Broker MQTT

Inicialmente, copie para o contexto atual os arquivos necessários:

```shell
cp ../config.env .env
```

## Configuração do TLS/SSL

É necessário configurar alguns dados para a criação do certificado SSL. O arquivo pode ser mantido quase inteiramente inalterado, mas certifique-se que o campo `CN` possui o IP (não pode ser URL por causa da compatibilidade com a ESP) do servidor em que será hospedado. O arquivo `openssl.cnf` é funcional e contém essas configurações, assumindo que o IP é `143.107.232.252`.

Uma vez completa essa configuração, pode-se gerar o certificado. Escolha uma senha segura (por exemplo, gerada com o `openssl rand -hex 32`) e copie para a sua clipboard. Execute o script abaixo e cole a senha conforme solicitado:

```shell
sh ./scripts/mosquitto_setup_certificates.sh
```

> Caso acontece algo de errado durante essa configuração, para tentar de novo pode ser útil deletar a pasta `mosquitto` com o comando `sudo rm -rf mosquitto`.

## Execução do Broker

Para executar o broker MQTT, é suficiente baixar a sua imagem do Docker Hub e depois executá-lo

```shell
docker compose pull broker
docker compose up broker -d # Sobe o container em modo detached
```

Depois, deve-se adicionar o usuário que foi configurado no arquivo `config.env`. Há um script pronto para tal:

```shell
sh ./scripts/mosquitto_add_user.sh
docker compose restart broker # Reinicia o broker para aplicar as mudanças
```
