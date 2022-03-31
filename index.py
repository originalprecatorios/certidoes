#!/usr/bin/python3
from time import time
from db.class_mongo import Mongo
import os, time
from myclass.robo import Robo

def _import():
    try:
        with open('/files/files_csv/certidoes.csv','r') as file:
            linha = file.read()
            quebra = linha.split("\n")
            mongo_datas = Mongo('certidoes')
            mongo_datas._getcoll('dados_busca')
            for l in quebra:
                if l:
                    itens = l.split(";")
                    mongo_datas._add_one({'nome': itens[0],'cpf':itens[1],'rg':itens[2].replace('.',"").replace("-",""),'nascimento':itens[3],'mae':itens[4],'genero':itens[6]})
                    print("INCLUIDO...")
            del mongo_datas
            os.remove("/files/files_csv/certidoes.csv")

            robo = Robo()
            robo._process()
            del robo
            
    except Exception as e:
        pass
        #print("..." + str(e))

while True:
    _import()
    time.sleep(300)
