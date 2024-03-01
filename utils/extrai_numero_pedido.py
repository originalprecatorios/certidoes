from bd.class_mongo import Mongo
import os
import pandas as pd
from xlwt import Workbook

wb = Workbook()

mongo = Mongo(os.getenv('MONGO_USER_PROD'), os.getenv('MONGO_PASS_PROD'), os.getenv('MONGO_HOST_PROD'), os.getenv('MONGO_PORT_PROD'), os.getenv('MONGO_DB_PROD'), os.getenv('MONGO_AUTH_DB_PROD'))  
mongo._getcoll('certidao')

arr = {"$and": [
        {"data_pedido_52": {"$exists": True}},
        {"numero_pedido_52": {"$exists": True}},
        {"data_pedido_6": {"$exists": True}},
        {"numero_pedido_6": {"$exists": True}},
        {"data_expedicao": {"$gte": '2023-05-26', "$lte": '2023-06-01'}}
    ]}
response = list(mongo.returnBusca(arr))
dados = []
linha = 1
sheet1 = wb.add_sheet('certidao')
sheet1.write(0, 0, 'id')
sheet1.write(0, 1, 'nome')
sheet1.write(0, 2, 'numero pedido 6')
sheet1.write(0, 3, 'data pedido 6')
sheet1.write(0, 4, 'numero pedido 52')
sheet1.write(0, 5, 'data pedido 52')
sheet1.write(0, 6, 'data expedicao')  
for ord in response:
    sheet1.write(linha, 0, '{}'.format(ord['_id']))
    sheet1.write(linha, 1, '{}'.format(ord['nome']))  
    sheet1.write(linha, 2, '{}'.format(ord['numero_pedido_6']))  
    sheet1.write(linha, 3, '{}'.format(ord['data_pedido_6']))
    sheet1.write(linha, 4, '{}'.format(ord['numero_pedido_52']))
    sheet1.write(linha, 5, '{}'.format(ord['data_pedido_52']))
    sheet1.write(linha, 6, '{}'.format(ord['data_expedicao']))
    linha +=1
wb.save("{}.xls".format('certidao'))