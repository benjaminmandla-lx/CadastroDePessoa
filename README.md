# Como Executar a Aplicação

## Requisitos

Antes de executar a aplicação, é necessário ter instalado:

* **Python 3.10 ou superior**
* **pip**
* **Git** (caso o projeto seja obtido através de um repositório)

A aplicação foi desenvolvida para Windows.

## 1. Abrir a pasta do projeto

Abra o terminal na pasta onde estão os arquivos do projeto.

A pasta deve conter, entre outros, os arquivos:

```text
main.py
database.py
validacoes.py
requirements.txt
```

no início da linha.

## 2. Atualizar o pip

Recomenda-se atualizar o gerenciador de pacotes:

```bash
python -m pip install --upgrade pip
```

## 3. Instalar as dependências

Execute:

```bash
pip install -r requirements.txt
```

Esse comando instalará automaticamente as bibliotecas necessárias para executar a aplicação.

## 4. Executar a aplicação

Após a instalação das dependências, execute:

```bash
python main.py
```

A janela da aplicação será aberta.

## 5. Banco de dados

O banco de dados SQLite é criado automaticamente pela aplicação na primeira execução.

Não é necessário criar o banco manualmente.

O arquivo gerado será:

```text
cadastro.db
```

## 6. Consulta de CEP

A função de consulta de CEP utiliza uma conexão com a internet.

Portanto, para utilizar essa funcionalidade, o computador deve estar conectado à internet.
