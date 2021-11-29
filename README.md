# Infraestrutura como código para exemplo de Datalake

## Ambiente

SÃ£o necessÃ¡rio os seguintes requisitos no ambiente de desenvolvimento:
- [Docker](https://docs.docker.com/get-docker/)
- [Python](https://www.python.org/)
- [pip](https://pt.wikipedia.org/wiki/Pip_(gerenciador_de_pacotes))
- [AWS CLI](https://aws.amazon.com/pt/cli/)

## AWS CLI

As permissÃµes para os ambientes de teste serÃ£o baseadas nas credenciais cadastradas do profile default configurado na maquina.

## Python e pip

Utilização para rodar testes unitários e ambiente de desenvolvimento

## Deploy
1. Instalação dos pacotes necessários para o projeto serverless presentes no package.json
    - `npm install`

2. Deploy do projeto serverless
    - `sls deploy --stage {stage}`
        > Stage igual a [dev], [staging] ou [prod].

## Modo de usar  

### Execução dos testes unitários necessários também para commit

1. Instalação dos pacotes necessários
    - `pip3 install moto`
    - `pip3 install boto3`
    - `pip3 install pytest`
    - `pip install pytest-cov`
    - `pip3 install awswrangler`
    - `pip3 install unittest`
    - `pip install pre-commit`

        > Neste momento a imagem **lambda** foi criada localmente no seu Docker.  

2. Execute testes. 
    - `pytest --cov=src test/conftest.py  `
        > Pytest com coverage.
    - `pytest --cov=src --html=test/report.html test/conftest.py`
        > Pytest com coverage e html report
    

coverage run --include=src/extract.py,src/process.py -m pytest test/conftest.py
coverage report --fail-under=70

coverage run -m pytest test/conftest.py
pre-commit install