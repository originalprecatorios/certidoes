# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os

class Mongo:
    
    def __init__(self, collection):
        self.BATCH_SIZE=10
        print(os.getenv('AMBIENTE'))
        if os.getenv('AMBIENTE') == "PROD":
            self.client = MongoClient(f"mongodb://{os.getenv('MONGO_USR')}:{os.getenv('MONGO_PWD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/?authSource={os.getenv('MONGO_AUTH_DB')}")
        else:
            self.client = MongoClient(f"mongodb://{os.getenv('MONGO_USR')}:{os.getenv('MONGO_PWD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}")   
        self.db = self.client[collection]
        self.col = ""
        
    def __del__(self):
        self.client.close()

    def _getcoll(self, p_coll):
        """
        'Seta' a collection
        :param p_coll: str
        """
        self.col = self.db[p_coll]

    def _return_query(self, p_query, p_fields = {}, limit=100, batch=True):
        """
        Retorna o cursor da consulta feita.
        :param p_query: dict
        return pymongo.cursor
        """
        if p_fields:
            return self.col.find(p_query, p_fields, no_cursor_timeout=True).limit(limit).batch_size(self.BATCH_SIZE)
        else:
            if batch:
                return self.col.find(p_query, no_cursor_timeout=True).batch_size(self.BATCH_SIZE)
            else:
                return self.col.find(p_query)

    def _add_many(self, p_dados):
        """
        Insere os dados de uma lista.
        """
        self.col.insert_many(p_dados)

    def _add_one(self, p_data):
        self.col.insert_one(p_data)

    def _upsert(self, p_dados, p_criterio):
        return self.col.update(p_criterio, p_dados, multi=True)

    def _update(self, p_dados, p_criterio):
        return self.col.update(p_criterio, p_dados)

    def _update_one(self, p_dados, p_creterio):
        return self.col.update_one(p_creterio, p_dados)

    def _return_aggregate(self, p_criterio, limit=100):

        return self.col.aggregate(p_criterio).batch_size(self.BATCH_SIZE)