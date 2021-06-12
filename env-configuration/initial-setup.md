curl -s "https://get.sdkman.io" | bash

source "$HOME/.sdkman/bin/sdkman-init.sh"

sdk version -> mostar a versao instalada

sdk install java 8.0.292.hs-adpt -> Instalar Java (de preferencia a versão 8)
java -version -> verifica a versão do java

sdk install scala 3.0.0 (Instalar Scala)
scala -version -> verifica a versão do scala

https://spark.apache.org/downloads.html -> fazer download do Apache Spark

Ir pelo terminal até a pasta onde o Apache Spark foi salvo

tar xvf spark-2.4.8-bin-hadoop2.7.tgz -> descompactar (Mac ou Linux)

ls -lha | grep spark -> para conferir se baixou

sudo cp -r spark-2.4.8-bin-hadoop2.7 /etc -> copiar pasta do Spark para o diretório /etc
cd /etc
ls -lha | grep spark -> para conferir se foi copiado

cd /etc
sudo ln -s spark-2.4.8-bin-hadoop2.7 spark

cd
vim .bash_profile ou vim .bashrc

Adicionar:
export SPARK_HOME=/etc/spark
export PATH=$SPARK_HOME/bin:$PATH

source .bash_profile -> para ativar as configuraçoes

spark-shell -> acessa o spark para conferir se está OK