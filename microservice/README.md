# Microsserviços

Lembre-se de abrir a pasta atual:

```shell
cd ./microservice # A partir da raiz do repositório
```

Copie para o contexto atual os arquivos necessários:

```shell
rm -rf .env proto
cp ../proto proto -r
cp ../config.env .env
```

## Publicação da imagem Docker

A fim de simplificar o deploy, todos os microsserviços construídos usam a mesma imagem Docker, modificando apenas o seu comando de execução. Essa está definida no arquivo `Dockerfile` neste repositório e, para utilizá-la no Kubernetes, devemos publicá-la no Dockerhub.

Inicialmente, é necessário criar uma conta no Dockerhub e se autenticar na máquina na local. O processo de autenticação pode ser realizado por meio do comando abaixo, substituindo-se devidamente as credenciais:

```shell
docker login -u=<usuario> -p=<senha>
``` 

> **Atenção:** Um modo mais seguro de autenticação envolve o uso de um Access Token. Para mais detalhes, consulte a documentação oficial: <https://docs.docker.com/security/for-developers/access-tokens/>.

Agora, podemos construir e publicar a imagem (você pode alterar `$DOCKER_USER` e `$IMAGE_NAME` conforme a necessidade).

```shell
docker build -t $DOCKER_USER/$IMAGE_NAME . && \
docker push $DOCKER_USER/$IMAGE_NAME
```

Para o presente trabalho, o perfil utilizado (`$DOCKER_USER`) foi o `allangarcia2004`, com a imagem (`$IMAGE_NAME`) `ssc0965`. Portanto, caso deseje baixar localmente a imagem utilizada para desenvolvimento, faça:

```shell
docker pull allangarcia2004/ssc0965:latest
```

Não esqueça essa identificação `$DOCKER_USER/$IMAGE_NAME`, pois ela será usada depois na configuração do Kubernetes.

## Instalação do K3s

Vamos instalar uma distribuição simplificada do Kubernetes, chamada de K3s. Assumimos aqui uma configuração em que haverá um único node (uma única máquina), que conterá todos os pods relativos aos microsserviços. Também assumiremos que, no firewall dessa máquina, foram liberadas as portas `$HTTP_PORT` e `$WS_PORT`, conforme definido no `config.env`.

Por padrão, o intervalo de portas (do host) disponíveis ao Kubernetes é `30000-32767`. Por limitações das portas liberadas pelo docente para uso na disciplina (`7011` e `7111`), esse intervalo precisou ser alterado. Durante a instalação, certifique-se de definir o `$PORT_RANGE` de modo que `$HTTP_PORT` e `$WS_PORT` estejam nele contidas.

Abaixo, faremos o download do script de instalação:

```shell
wget https://get.k3s.io -O k3s_install.
```

Caso as portas liberadas estejam fora do intervalo padrão, executar conforme abaixo, modificando o intervalo se necessário:

```shell
PORT_RANGE="7000-7200"
INSTALL_K3S_EXEC="server --service-node-port-range $PORT_RANGE" sh ./k3s_install.sh
```

Caso contrário, simplesmente executar o script baixado:

```shell
sh ./k3s_install.sh
```

Terminada a instalação, sobrescrevemos o arquivo em `KUBECONFIG` para permitir o correto funcionamento do `kubectl`:

```shell
echo "export KUBECONFIG=\$HOME/.kube/config" >> ~/.bashrc
source ~/.bashrc

mkdir $(dirname $KUBECONFIG) -p
sudo k3s kubectl config view --raw > "$KUBECONFIG"
chmod 600 "$KUBECONFIG"
```

## Criação dos Arquivos de Manifesto

Infelizmente, diferentemente do Docker Compose, o Kubernetes não permite, de forma fácil, o uso de variáveis de ambientes para modificar os próprios arquivos de manifesto (`*.yaml`). Como desejamos customizar algumas coisas, como as portas, os IPs, a própria imagem de Docker etc, faremos um workaround: na pasta `kubernetes/templates/`, encontram-se os manifestos "puros", com as variáveis de ambientes não configuradas (por exemplo, há linhas como: `nodePort: $HTTP_PORT`). 

Utilizando a ferramenta `envsubst` (nativa do Linux), iremos fazer a substituição dos nomes das variáveis pelos seus valores conforme definido no `config.env`. Para isso, há um script que irá carregar as variáveis de configuração e, para cada arquivo manifesto, executar a substituição e salvar em uma pasta separada. 

Uma variável usada que não está no `config.env` é a `$MICROSERVICE_IMAGE`, que define o nome da imagem, no Dockerhub, a ser utilizada nos microsserviços. Ela deve ter o nome que foi utilizado para fazer a publicação início deste texto. Abaixo, segue exemplo da execução do script utilizando a imagem de desenvolvimento:

```shell
# Altere conforme necessidade
MICROSERVICE_IMAGE="allangarcia2004/ssc0965:latest" sh ./scripts/replace_kubernetes_variables.sh
```

Agora, os arquivos de configuração prontos se encontram na pasta `kubernetes/replaced`. Portanto, devemos entrar na pasta:

```shell
cd ./kubernetes/replaced
```

> **Atenção:** Caso alguma variável seja alterada, deve-se executar novamente o `replace_kubernetes_variables.sh`.

## Implantação do Postgres e do Kafka

Criados os arquivos finais de manifesto, podemos aplicá-los:

```shell
# Deve-se estar na pasta kubernetes/replaced

# Cria um namespace para a aplicação
kubectl create namespace iot

# Criando um ConfigMap baseado nas configurações da aplicação
kubectl apply -n iot -f ./0_app_config.yaml

# Instalando o Kafka (e criando seus tópicos) e o Postgres
kubectl apply -n iot -f ./1_strimzi_install.yaml \
                     -f ./2_kafka_persistent_single.yaml \
                     -f ./3_topics.yaml \
                     -f ./4_postgres.yaml
```

Antes de continuar, use o comando abaixo e certifique-se que há ao menos um pod READY de cada um dos tipos: `kafka-cluster-kafka`, `kafka-cluster-zookeeper` e `postgres`. **Aviso:** isso pode demorar.

```shell
kubectl get -n iot pods --watch
```

Abaixo segue um exemplo dos containers em estado READY:

![](./image/example-wait.png)

## Implantação dos Microsserviços

Por fim, vamos inicializar os microsserviços:

```shell
kubectl apply -n iot -f ./5_microservice_deployments.yaml \
                     -f ./6_microservice_services.yaml
```

Pode-se, então, aguardar para que todos os pods novos estejam READY.

```shell
kubectl get -n iot pods --watch
```