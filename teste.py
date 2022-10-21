'''from pymongo import CursorType
from pymongo import MongoClient
import time
import pymongo

db = MongoClient("mongodb://original:bp3f6QTU58dbY3sP@200.194.172.112:27017/?authSource=admin") 
coll = db['monitora']
teste = coll['certidao']
cursor = teste.find(cursor_type=pymongo.CursorType.TAILABLE_AWAIT,oplog_replay=True).sort('$natural', pymongo.ASCENDING).limit(-1)
while cursor.alive:
    try:
        doc = cursor.next()
        print (doc)
    except StopIteration:
        time.sleep(1)'''


import time

import pymongo

client = pymongo.MongoClient('mongodb://original:bp3f6QTU58dbY3sP@200.194.172.112:27017/?authSource=admin')
oplog = client.local.oplog.rs
first = oplog.find().sort('$natural', pymongo.ASCENDING).limit(-1).next()
print(first)
ts = first['ts']

while True:
    # For a regular capped collection CursorType.TAILABLE_AWAIT is the
    # only option required to create a tailable cursor. When querying the
    # oplog, the oplog_replay option enables an optimization to quickly
    # find the 'ts' value we're looking for. The oplog_replay option
    # can only be used when querying the oplog. Starting in MongoDB 4.4
    # this option is ignored by the server as queries against the oplog
    # are optimized automatically by the MongoDB query engine.
    cursor = oplog.find({'ts': {'$gt': ts}},
                        cursor_type=pymongo.CursorType.TAILABLE_AWAIT,
                        oplog_replay=True)
    while cursor.alive:
        for doc in cursor:
            ts = doc['ts']
            print(doc)
        # We end up here if the find() returned no documents or if the
        # tailable cursor timed out (no new documents were added to the
        # collection for more than 1 second).
        time.sleep(1)

