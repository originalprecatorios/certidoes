<p align="center">
</p>

<h1 align="center">
	<img src="https://www.python.org/static/community_logos/python-logo-inkscape.svg"  alt="Logo"  width="240"><br><br>
    Robô Certidões - Robot Certificates
</h1>

<div>
    <p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/static/v1?label=Language&message=Python&color=blue&style=for-the-badge&logo=Python" alt="Language: Python">
    </a>
    <a href="https://www.mongodb.com/home">
        <img src="https://img.shields.io/static/v1?label=Language&message=MongoDB&color=gree&style=for-the-badge&logo=MongoDB" alt="Language: MongoDB">
    </a>
    <a href="https://www.rabbitmq.com/">
        <img src="https://img.shields.io/static/v1?label=Language&message=RabbitMQ&color=orange&style=for-the-badge&logo=RabbitMQ" alt="Language: RabbitMQ">
    </a>
    <a href="https://www.mysql.com">
        <img src="https://img.shields.io/static/v1?label=Language&message=MySQL&color=blue&style=for-the-badge&logo=MySQL" alt="Language: MySQL">
    </a>
    </p>
</div>

## Table of Contents

<p align="center">
 <a href="#about">About</a> •
 <a href="#features">Features</a> •
 <a href="#revised-concepts">Revised Concepts</a> • 
 <a href="#installation">Installation</a> • 
 <a href="#getting-started">Get Started</a> • 
 <a href="#technologies">Technologies</a> • 
</p>

## 📌About

<div>
    <p align="center">
    <em>
        - Construção de um robô que solicita ou baixar certidões
        - Construction of a robot that requests or downloads certificates
    </em>
    </p>
</div>

## 🚀Features

- Manipulação do google,baixar certificados automaticamente,envia email solicitando certificado.
- Google manipulation, download certificates automatically, send email requesting certificate.

## 👓Revised Concepts

- Selenium
- Pymongo
- Pymysql
- RabbitMQ
- Twocaptcha

## 📕Installation

**You must have already installed**
- [Python3](https://www.python.org/)
- [Pip](https://pip.pypa.io/en/stable/installation/)

**Recommendations**
- Eu recomendo usar o VSCode como IDE de desenvolvimento
- I recommend using VSCode as a development IDE


**Let's divide it into 3 steps.**
1. Clone this repository - Clonar este repositório
2. Install dependencies - Instale as dependênciass
3. Create environment variable - Criar variavel de ambiente
4. Download and configure chromedriver and geckodriver - Baixar e configurar chromedriver e geckodriver
  ---
### 1. Clone this repository
```
git clone https://github.com/originalprecatorios/receitanetbx.git
```
---
### 2. Install the dependencies
```
pip install -r /path/to/requirements.txt
```
---

### 3. Create environment variable

open the terminal
type export variablename="variablevalue"

abra o terminal
digite export nomedavariavel="valordavariavel"

captcha password - Senha do captcha
```
export CAPTCHA="SenhaCAPTCHA"
```

SMTP
```
export SMTP_PORT=587
export SMTP_SERVE="smtp.office365.com"
export SMTP_USER="user"
export SMTP_PASS="password"
```

MONGO
```
MONGO_HOST_PROD="000.000.000.000"
MONGO_PORT_PROD=27017
MONGO_USER_PROD="user"
MONGO_PASS_PROD="password"
MONGO_AUTH_DB_PROD="admin"
MONGO_DB_PROD='database'
```

Website links - Links dos sites
```
export PAGE_URL="https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

export PAGE_URL_MUN="https://duc.prefeitura.sp.gov.br/certidoes/forms_anonimo/frmConsultaEmissaoCertificado.aspx"

export PAGE_URL_CONTRIBUINTE="https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf?param=150304"

export PAGE_URL_FEDERAL="https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir"

export PAGE_URL_CRIMINAL_1="https://esaj.tjsp.jus.br/sco/abrirCadastro.do"

export PAGE_URL_TRTSP="https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao"

export PAGE_URL_TST="https://cndt-certidao.tst.jus.br/inicio.faces"

export PAGE_URL_TRT15="https://trt15.jus.br/servicos/certidoes/certidao-eletronica-de-acoes-trabalhistas-ceat"

export PAGE_URL_TRF3_JUS="https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao"

export PAGE_URL_ESAJ_B_NOME_CPF="https://esaj.tjsp.jus.br/cpopg/open.do"

export PAGE_URL_PROTESTO="https://protestosp.com.br/consulta-de-protesto"

export PAGE_URL_PROTESTO2="https://site.cenprotnacional.org.br/"

export PAGE_URL_PJE_TRF3="https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

export PAGE_URL_DEBITO_TRABALHISTA="http://www.tst.jus.br/certidao1"

export PAGE_URL_TJ="https://esaj.tjsp.jus.br/cpopg/search.do"

export PAGE_URL_SSP="https://www.ssp.sp.gov.br/servicos/atestado.aspx"

export VERSION=89
```

### 4. Download and configure chromedriver and geckodriver
```
Download chromedriver geckodriver as per installed version of both browsers - 
Fazer o download do geckodriver chromedriver conforme a verção instalada de ambos os navegadores 
https://chromedriver.chromium.org/downloads
https://github.com/mozilla/geckodriver/releases
```

```
Extract and copy the files to the /usr/local/bin/ folder -
Extrair e copiar os arquivos para a pasta /usr/local/bin/
```
---

## 🎮Getting Started

1. Open vscode or terminal - Abra o vscode ou terminal

2. start debugging in main.py file - iniciar a depuração no arquivo main.py

## 🌐Technologies

<p align="center">

- [Python](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/home)
- [MySQL](https://www.mysql.com/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [2captcha](https://2captcha.com/?from=15605423&gclid=Cj0KCQiA14WdBhD8ARIsANao07iIhQkPbx80Ccimj8v6XRP2UsbRYf4m7fYQSJJV-N_D4KqJoGnC-dQaAlk2EALw_wcB)