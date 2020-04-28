# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:13:16 2020

@author: Niket Jain
"""


import pymongo

con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con["Celebrity_Details"]

table1=db["Actor"]

for actor in table1.find():
    print(actor)

    
table2=db["Actress"]
for actress in table2.find():
    print(actress)