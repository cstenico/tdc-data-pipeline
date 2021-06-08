# tdc-data-pipeline
Código utilizado na palestra do TDC Connection, junho 2021


## Setup do Apache Airflow localmente

https://airflow.apache.org/docs/apache-airflow/stable/start/local.html
Utilize versão de python abaixo de 3.9 dado o suport do airflow
Utilizei Python 3.7 :)

Defina o local de instalação
> export AIRFLOW_HOME=~/airflow

Inicialize o banco de dados do Airflow
>airflow db init

Crie um usuário admin
> airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
    
Configure seu airflow.cfg
. Em AIRFLOW_HOME, abra airflow.cfg no seu editor de preferência

1. Pasta de DAG
Aponte a pasta de DAG para seu diretório de DAG colocando o caminho completo na linha:
>#The folder where your airflow pipelines live, most likely a
>#subfolder in a code repository. This path must be absolute.
> dags_folder = /Users/....

Inicialize o servidor na porta 8080 (login e senha são admin e senha definida no passo acima)
> airflow webserver --port 8080

Dê start no scheduler em uma nova página do terminal
> airflow scheduler

Usuários de Mac OS X: devem definir a seguinte variável de ambiente no terminal para permitir a execução dos processos do Airflow. 
> export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
