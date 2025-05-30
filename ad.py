# coding=utf-8
import sqlite3
import sys

import re
import math
from model import Model
import random
import webbrowser
from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely.geometry import Point
from faker import Faker
class Ad(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.create_function('sqrt', 1, math.sqrt)
        self.con.create_function('cos', 1, math.cos)
        self.con.create_function('pow', 2, math.pow)
        self.con.row_factory = sqlite3.Row
        sekf.fake = Faker()
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists ad(
        id integer primary key autoincrement,
        name text,
            lat text,
            lon text,
            description text
                    );""")
        self.con.commit()
        #self.con.close()
    def mymusicjournal(self):
        i=["violin","piano","guitar","trumpet","drums"]
        random_i = str(random.choice(i))
        minutes=str(random.randint(100, 200))
        return "wow, i must have practiced "+random_i+" "+minutes+"today!"
    def mysportjournal(self):
        list=["football","figure skating","tennis","rugby","rowing"]
        random_num = str(random.choice(list))
        return "wow, that was my record in "+random_num+" today:"
    def samecity(self):
        list=["f","m"]
        random_num = random.choice(list)
        i=["violin","piano","guitar","trumpet","drums"]
        random_i = random.choice(i)
        mytext="oh no"

        mycity=self.fake.city()
        if random_num == "f":
          concert="her"
          musician="her"
          music="she"
          myname=self.fake.first_name_female()
        elif random_num == "f":
          concert="his"
          musician="him"
          music="he"
          myname=self.fake.first_name_male()
        Faker.seed(0)
        mycountry=self.fake.country()
        mytext+=", "+myname+"'s concert is soon in my city,"+myname+" is from "+mycountry+", "+music+" is my favorite "+random_i+" player, and I want to go to "+concert+" concert so much. "+concert+" concert is in "+mycity+" in 1 week, I so much want to book the tickets to see "+musician+"."
        return mytext
    def getall(self):
        self.cur.execute("select * from ad")

        row=self.cur.fetchall()
        geolocator = Nominatim(user_agent="abcdefgh")

        yeah=[]
        for x in row:

            location = geolocator.reverse((x["lat"], x["lon"]), language='fr')
            y=dict(x)
            y["monlieu"]=location
            yeah.append(y)
           
        return yeah
    def deletebyid(self,myid):

        self.cur.execute("delete from ad where id = ?",(myid,))
        ad=self.cur.fetchall()
        self.con.commit()
        return None
    def getplacesnearby(self,text_ad,text_address):
        try:
            print("nearby")
            geolocator = Nominatim(user_agent="abcdefghij")
            location = geolocator.geocode(text_address)
            if location:
                startlat=location.latitude
                startlng=location.longitude
                sqlcommand2 = """SELECT id,name,description,lat,lon, sqrt( pow((69.1 * (lat - ?)), 2) + pow((69.1 * (? - lon) * cos(lat / 57.3)), 2)) AS distance FROM ad GROUP BY ad.id HAVING distance < 50 and (lower(title) like '%"+text_ad.replace(" ","%")+"%' or lower(description) like '%"+text_ad.replace(" ","%")+"%') ORDER BY distance;"""
                self.cur.execute(sqlcommand2,(startlat,startlng))
                rows=self.cur.fetchall()
                if rows and len(rows) > 0:
                    return {"rows":rows, "message":"des offres ont été trouvées"}
                else:
                    return {"rows":rows, "message":"aucune offre a été trouvée"}
            else:
                return {"rows":[], "message":"aucun lieu n'a été trouvé"}
        except Exception as e:
            return {"rows":[], "message":"il y a eu un probleme de connexion internet"}

    def getplacenamebyid(self,myid):
        self.cur.execute("select * from ad where id = ?",(myid,))
        row=dict(self.cur.fetchone())
        # Génère une coordonnée aléatoire sur terre
        lat, lon = row["lat"], row["lon"]
        print(f"Coordonnée trouvée : {lat}, {lon}")
        geolocator = Nominatim(user_agent="abcdefgh")
        location = geolocator.reverse((lat, lon), language='fr')
        return location
    def getbyid(self,myid):
        self.cur.execute("select * from ad where id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        ad=self.cur.fetchall()
        return row
    def create(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'envoyer' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          self.cur.execute("insert into ad (name,lat,lon,description) values (:name,:lat,:lon,:description)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["ad_id"]=myid
        azerty["notice"]="votre ad a été ajouté"
        return azerty




