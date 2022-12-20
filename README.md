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
2. Install dependencies - Instale as dependências
3. Install 32-bits JAVA - instale JAVA 32-bits
4. Install ReceitanetBX - instale ReceitanetBX
5. Get the digital certificates - Obtenha os certificados digitais
6. Get passwords for digital certificates - Obtenha as senhas dos certificados digitais
7. Obtain the path of the folder where the ReceitanetBX is installed - Obtenha o caminho da pasta onde está instalado o ReceitanetBX
8. Create environment variable - Criar variavel de ambiente
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
### 3. Install 32-bits JAVA
```
https://www.java.com/pt-BR/download/help/linux_install.html
```
---
### 4. Install ReceitanetBX
```
https://www.gov.br/receitafederal%22/pt-br/centrais-de-conteudo/download/receitanetbx/download-do-programa-receitanetbx-linux
```
When installing ReceitanetBX, the system will 'inform which is the path of the installed java?', The path of the 32bits java installed must be informed Exp: /usr/lib/jvm/jre-8u351-linux-i586/jre1.8.0_351/

Ao instalar o ReceitanetBX o sistema irá 'informar qual o caminho do java instalado?', Deve ser informado o caminho do java 32bits instalado Exp: /usr/lib/jvm/jre-8u351-linux-i586/jre1.8.0_351/

---
### 5. Get the digital certificates

Obtain a digital certificate to be able to start the robot

Obetenha um certificado digital para poder inicializar o robô

Create a folder in /opt with the name cert and add the certificate in this folder

Criar uma pasta no /opt com o nome cert e adcionar o certificado nesta pasta

### 6. Get passwords for digital certificates

Obtain the password of the digital certificate where it will be installed in the netbx recipe

Obetenha a senha do certificado digital onde será instalado no receitanetbx

### 7. Obtain the path of the folder where the ReceitanetBX is installed

When starting the installation of ReceitanetBX, it will inform you in which folder the program will be installed, obtain this path to be informed in the robot

Ao iniciar a instalação do ReceitanetBX o mesmo irá informar em que pasta irá ser feita a instalação do programa, obtenha esse caminho para ser informado no robo

### 8. Create environment variable

open the terminal
type export variablename="variablevalue"

abra o terminal
digite export nomedavariavel="valordavariavel"

certificate password - Senha do certificado
```
export CERT="SenhaCertificado"
```

Path where RevenuenetBX is installed - Caminho onde esta instalado o ReceitanetBX 
```
export RECEITANET="/home/wesley/Programas-RFB/ReceitanetBX/receitanetbx-gui-1.9.20.jar"
```


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