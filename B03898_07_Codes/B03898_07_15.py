"""
README
======
This file contains Python codes.
======
"""

import datetime as dt
import pymongo

client = pymongo.MongoClient("localhost", 27017)
ticks_db = client.ticks_db
aapl_collection = ticks_db.aapl

tick = {"ticker": "aapl",
        "time": dt.datetime(2014, 11, 17, 10, 0, 0),
        "open": 115.58,
        "high": 116.08,
        "low": 114.49,
        "last": 114.96,
        "vol": 1900000}

tick_id = aapl_collection.insert(tick)
print tick_id
print ticks_db.collection_names()

print aapl_collection.find_one()
print aapl_collection.find_one({"time": dt.datetime(2014, 11, 17, 10, 0, 0)})

from bson.objectid import ObjectId
print aapl_collection.find_one({"_id": \
	ObjectId("548490486d3ba7178b6c36ba")})

aapl_collection.remove()

aapl_collection.insert([tick,
                       {"ticker": "aapl",
                        "time": dt.datetime(2014, 11, 17, 10, 1, 0),
                        "open": 115.58,
                        "high": 116.08,
                        "low": 114.49,
                        "last": 115.00,
                        "vol": 2000000},
                       {"ticker": "aapl",
                        "time": dt.datetime(2014, 11, 17, 10, 2, 0),
                        "open": 115.58,
                        "high": 116.08,
                        "low": 113.49,
                        "last": 115.00,
                        "vol": 2100000}])

print aapl_collection.count()
print aapl_collection.find({"open": 115.58}).count()

for aapl_tick in aapl_collection.find():
   print aapl_tick

cutoff_time = dt.datetime(2014, 11, 17, 10, 2, 0)
for tick in aapl_collection.find(
       {"time": {"$lt": cutoff_time}}).sort("time"):
   print tick 

sorted_ticks = aapl_collection.find().sort(
    [("time", pymongo.DESCENDING)])
for tick in sorted_ticks:
    print tick 

   