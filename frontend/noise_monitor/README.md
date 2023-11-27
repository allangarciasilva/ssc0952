# Backend e Broker MQTT

Para essa parte, foi disponibilizado uma configuração de imagem que instala todas as dependências necessárias pelo Flutter, incluindo o Android SDK, e compila a aplicação. Com isso, pode-se conectar um smartphone Android via USB e, em um terminal dentro do container, enviar a aplicação. 

> **Atenção:** É necessário a opção de **Depuração USB** do Android esteja ativada. O tutorial oficial para ativação pode ser encontrado [aqui](https://developer.android.com/studio/debug/dev-options?hl=pt-br). Em alguns dispositivos, a opção **Número da versão** pode estar sob o nome de **Número de compilação**.

Compilar e abrir o terminal, faça:

```shell
# Copia os arquivos do Protobuf para a pasta atual
sh ./scripts/setup.sh

# Constrói a imagem e abre um terminal dentro do container
docker compose build flutter
docker compose run --rm -it flutter bash
```

> **Atenção:** o processo de *build* da imagem pode ser demorado e requisitar uma quantidade considerável de memória.
 
## Instalação

No terminal aberto, você pode verificar se a ESP está corretamente detectada utilizando o comando:

```shell
adb devices
```

> Caso não tenha sido listado nenhum disposivo, além de verificar que o Android está com a Depuração USB ativa, caso você tenha o ADB instalado na sua máquina host, pode ser necessário desativá-lo. Para isso, utilize o comando: `adb kill-server` (pode ser necessário executar mais de uma vez).

Por fim, para enviar o programa para o smartphone, pode-se utilizar:

```shell
flutter install
```

A aplicação deve, então, ter sido instalada com o nome de `noise_monitor`.

## Obtenção do APK

Outra forma de instalar o aplicativo no celular é utilizando o APK que foi compilado durante a construção da imagem e instalar manualmente no aparelho.

O APK compilado encontra-se no caminho `/home/developer/app/release.apk` e pode ser obtido por meio de:

```shell
# No terminal do host
docker compose up -d flutter
docker compose cp flutter:/home/developer/app/release.apk ./release.apk
docker compose down flutter
```

Uma vez obtido o APK, pode-se movê-lo para o smartphone e instalá-lo normalmente.