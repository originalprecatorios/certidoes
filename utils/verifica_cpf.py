from crypto import db
import os 
from bd.class_mongo import Mongo


mongo = Mongo(os.getenv('MONGO_USER_PROD'), os.getenv('MONGO_PASS_PROD'), os.getenv('MONGO_HOST_PROD'), os.getenv('MONGO_PORT_PROD'), os.getenv('MONGO_DB_PROD'), os.getenv('MONGO_AUTH_DB_PROD'))
mongo._getcoll('certidao')

users  = list(mongo.returnQuery())

for usr in users:
    try:
        if type(usr['cpf']) is bytes:
            usr['cpf'] = db.decrypt(usr['cpf'])
        if type(usr['rg']) is bytes:
            usr['rg'] = db.decrypt(usr['rg'])
        if usr['rg'].find('.') >= 0:
            usr['rg'] = usr['rg'].replace('.','')

        if usr['cpf'] == '943.787.898-68':
            print()  
    except:
        pass