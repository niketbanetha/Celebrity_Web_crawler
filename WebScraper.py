# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:13:16 2020

@author: Niket Jain
"""

import requests
from bs4 import BeautifulSoup
import re
import unidecode
import urllib
import json
import pymongo

con = pymongo.MongoClient("mongodb://localhost:27017/")
db = con["Celebrity_Details"]



site2=requests.get("https://en.wikipedia.org/wiki/List_of_Indian_film_actors")
site3=requests.get("https://en.wikipedia.org/wiki/List_of_Indian_film_actresses")

d=site2.text
d1=site3.text

b=BeautifulSoup(d,"html.parser")
b1=BeautifulSoup(d1,"html.parser")

data=b.find_all("div",{"class":"div-col columns column-width"})
data1=b1.find_all("div",{"class":"div-col columns column-width"})
   
actor=[]
for i in data:
    for j in i.find_all('a',{"href":re.compile('^/wiki/')}):
        actor.append(j["href"])
        
actress=[]
for i in data1:
    for j in i.find_all('a',{"href":re.compile('^/wiki/')}):
        actress.append(j["href"])




        
 
table1 = db["Actor"] 
#Actor
for i in actor:
        site=requests.get("https://en.wikipedia.org"+i)
                     
        if site.status_code !=200:
            continue
        site_text=site.text
        bs=BeautifulSoup(site_text, "lxml")
        bs1 = BeautifulSoup(site_text, 'html.parser')
        images = bs1.find_all('img', {'src':re.compile('.jpg')})
        dict1={}
        wins=""
        noms=""
        dict1["Name"]=i.replace('/wiki/','')
        if images!=[]:
            dict1["Image"]=images[0]["src"]
        else:
            dict1["Image"]="No Image"
        try:
            table_body=bs.find('table',{'class':'infobox biography vcard'})
            rows = table_body.find_all('tr')
        except AttributeError :
            #print(dict1)
            table1.insert_one(dict1)
            
        else:  
            for row in rows:
                cols=row.find_all('td')
                colsth=row.find_all('th')
                colsth=[x.text.strip() for x in colsth]
                cols=[x.text.strip() for x in cols]
                for k in row.find_all('a',{"href":re.compile('awards_and_nominations')}):
                        if re.findall("(awards)+",str(k["href"])):
                            #print(k["href"])
                            site4="https://en.wikipedia.org"+k["href"]
                            link=requests.get(site4)
                            link_text=link.text
                            bs3=BeautifulSoup(link_text,"html.parser")
                            win=bs3.find_all("td",{"class":"yes table-yes2","colspan":"2"}) 
                            nom=bs3.find_all("td",{"class":"no table-no2","colspan":"2"})
                            
                            if len(win)==0:
                                win=bs3.find_all("td",{"style":"text-align:center;;background:#9F9;"})
                            if len(nom)==0:
                                nom=bs3.find_all("td",{"style":"text-align:center;;background:#FDD;"})
                                
                for x,y in zip(colsth,cols):
                    dict1[unidecode.unidecode(x)]=unidecode.unidecode(y)
        
            if "Awards" in dict1.keys():     
                dict1.pop("Awards")
                if len(nom) == 0:
                    dict1["Award Nomination"]="0"
                else:
                    dict1["Awards Nomination"]=nom[0].text
                if len(win)==0:
                    dict1["Awards Win"]=0
                else:
                    dict1["Awards Win"]=win[0].text
            #print(dict1)
            table1.insert_one(dict1)

            


table2 = db["Actress"]
#Actress
for i in actress:
        site=requests.get("https://en.wikipedia.org"+i)
                     
        if site.status_code !=200:
            continue
        site_text=site.text
        bs=BeautifulSoup(site_text, "lxml")
        bs1 = BeautifulSoup(site_text, 'html.parser')
        images = bs1.find_all('img', {'src':re.compile('.jpg')})
        dict1={}
        dict1["Name"]=i.replace('/wiki/','')
        if images!=[]:
            dict1["Image"]=images[0]["src"]
        else:
            dict1["Image"]="No Image"
        
        try:
            table_body=bs.find('table',{'class':'infobox biography vcard'})
            rows = table_body.find_all('tr')
        except AttributeError :
            #print(dict1)
            table2.insert_one(dict1)
        else:  
            for row in rows:
                cols=row.find_all('td')
                colsth=row.find_all('th')
                colsth=[x.text.strip() for x in colsth]
                cols=[x.text.strip() for x in cols]
                for k in row.find_all('a',{"href":re.compile('awards_and_nominations')}):
                        if re.findall("(awards)+",str(k["href"])):
                           # print(k["href"])
                            site4="https://en.wikipedia.org"+k["href"]
                            link=requests.get(site4)
                            link_text=link.text
                            bs3=BeautifulSoup(link_text,"html.parser")
                            win=bs3.find_all("td",{"class":"yes table-yes2","colspan":"2"}) 
                            nom=bs3.find_all("td",{"class":"no table-no2","colspan":"2"})
                            
                            if len(win)==0:
                                win=bs3.find_all("td",{"style":"text-align:center;;background:#9F9;"})
                            if len(nom)==0:
                                nom=bs3.find_all("td",{"style":"text-align:center;;background:#FDD;"})
                                
                for x,y in zip(colsth,cols):
                    dict1[unidecode.unidecode(x)]=unidecode.unidecode(y)
        
            if "Awards" in dict1.keys():     
                dict1.pop("Awards")
                if len(nom) == 0:
                    dict1["Award Nomination"]="0"
                else:
                    dict1["Awards Nomination"]=nom[0].text
                if len(win)==0:
                    dict1["Awards Win"]=0
                else:
                    dict1["Awards Win"]=win[0].text
            print(dict1)
            table2.insert_one(dict1)

