import pandas as pd
import psycopg2
from os import listdir
from statistics import mean, median, mode
import ScrapOlx
from datetime import datetime

def create_table(Tablename):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS {0} (Name TEXT, Price REAL, Location TEXT, Date DATE, UNIQUE(Name))".format(Tablename))
    conn.commit()
    conn.close()

def create_data_table():
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS mydata (item TEXT, date DATE, number_of_items REAL, mean_price REAL, median_price REAL, min_price REAL, max_price REAL, low_price REAL, high_price REAL, UNIQUE(date))")
    conn.commit()
    conn.close()

def ProcessFiles():
    create_data_table()
    for i in range(0, len(listdir("OlxOutputs/"))):
        print("Table "+str(i+1)+"/"+str(len(listdir("OlxOutputs/")))+" processed")#debug show processed pages
        create_table("Table_"+str(i))
        df = pd.DataFrame(pd.read_csv ("OlxOutputs/"+listdir("OlxOutputs/")[i],index_col=0))
        insertall(df,"Table_"+str(i))
        insert_my_data(item=str(ScrapOlx.base_url),
        date=str(listdir("OlxOutputs/")[i])[:-4],
        number_of_items= ViewSUM("Table_"+str(i))[0][0],
        mean_price= mean(ViewPrice("Table_"+str(i))),
        median_price=median(ViewPrice("Table_"+str(i))), 
        min_price=min(ViewPrice("Table_"+str(i))), 
        max_price=max(ViewPrice("Table_"+str(i))), 
        low_price=mean(sorted(ViewPrice("Table_"+str(i)))[:round(0.10*len(ViewPrice("Table_"+str(i))))]), 
        high_price=mean(sorted(ViewPrice("Table_"+str(i)))[round(0.10*len(ViewPrice("Table_"+str(i)))):]))

def ViewAll(Tablename):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM {0}".format(Tablename))
    item = cur.fetchall()
    conn.close()
    return item

def insert(Name,Price,Location,Date,Tablename):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO {4} (Name,Price,Location,Date) VALUES ('{0}','{1}','{2}','{3}') ON CONFLICT (Name) DO NOTHING".format(Name,Price,Location,Date,Tablename))
    conn.commit()
    conn.close()

def insertall(df,Tablename):
    for i in range(0, len(df)):
        insert(Name=df.iloc[i][0],Price=df.iloc[i][1],Location=df.iloc[i][2],Date=df.iloc[i][3],Tablename=Tablename)
        print (str(i)+"/"+str(len(df)))#debug show processed items

def insert_my_data(item, date, number_of_items, mean_price, median_price, min_price, max_price, low_price, high_price):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO mydata (item, date, number_of_items, mean_price, median_price, min_price, max_price, low_price, high_price) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}') ON CONFLICT (date) DO NOTHING".format(item, date, number_of_items, mean_price, median_price, min_price, max_price, low_price, high_price))
    conn.commit()
    conn.close()

def deleteall(Tablename):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("DELETE FROM {0}".format(Tablename))
    conn.commit()
    conn.close()

def ViewSUM(Tablename):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM {0}".format(Tablename))
    item = cur.fetchall()
    conn.close()
    return item

def ViewPrice(Tablename):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("SELECT price FROM {0}".format(Tablename))
    item = [i[0] for i in cur.fetchall()]
    conn.close()
    return item

def Acces_Data_Table(item):
    conn = psycopg2.connect("dbname=OlxDatabase user =postgres password =kashtan host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("SELECT {0} FROM mydata".format(item))
    item = [i[0] for i in cur.fetchall()]
    conn.close()
    return item
