
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import locale
import calendar
from iteration_utilities import unique_everseen

locale.setlocale(locale.LC_ALL, '')

Title = str(time.localtime()[0])+"_"+str(time.localtime()[1])+"_"+str(time.localtime()[2])
Today = str(time.localtime()[0])+"-"+str(time.localtime()[1])+"-"+str(time.localtime()[2])
Yesterday = str(time.localtime()[0])+"-"+str(time.localtime()[1])+"-"+str(time.localtime()[2]-1)
Months= {month: index for index, month in enumerate(calendar.month_abbr) if month}
base_url = "https://www.olx.pl/elektronika/gry-konsole/gry/q-ghost-of-tsushima-ps4/"


def LastPage(): # Find Last Page Number
    Site_Get=requests.get(base_url)
    Site_Content=Site_Get.content
    Content_Soup=BeautifulSoup(Site_Content,"html.parser")
    var2=Content_Soup.find("div",{"class":"pager rel clr"})

    if var2 == None:
        return 2 # if only one page exists return 2 as range ignores last index
    else:
        return int(var2.find_all("span",{"class":"item fleft"})[-1].text.replace("\n",""))+1 # Last page number + 1 as range ignores last index

def scrapit():
    l = []
    for page in range(1,LastPage()): # LEARN TO HANDLE NR OF SITES
        
        Site_Get=requests.get(base_url+"?page="+str(page))
        Site_Content=Site_Get.content
        soup=BeautifulSoup(Site_Content,"html.parser")
        var=soup.find_all("tr",{"class":"wrap"})
        
        for i in range (0,int(len(var))-1):
            d = {}
            try:
                d["Name"]= var[i].find("h3",{"class":"lheight22 margintop5"}).text.replace("\n","")
            except:
                d["Name"]= "None"

            try:
                d["Price"]= var[i].find("p",{"price"}).text.replace("\n","").replace("zł","").replace(",",".").replace(" ","")
            except:
                d["Price"]= "None"

            try:
                d["Location"]= var[i].find("td",{"class":"bottom-cell"}).find_all("small",{"class":"breadcrumb x-normal"})[0].text.replace("\n","")
            except:
                d["Location"]= "None"

            try:
                date_var = var[i].find("td",{"class":"bottom-cell"}).find_all("small",{"class":"breadcrumb x-normal"})[1].text.replace("\n","")

                if "dzisiaj" in date_var:
                    d["Date"]= date_var.replace(date_var,Today)
                
                elif "wczoraj" in date_var:
                    d["Date"]= date_var.replace(date_var,Yesterday)

                else:
                    for i in list(Months.keys()):
                        if date_var.split()[1] == i:
                            d["Date"]= str(str(time.localtime()[0])+"-"+str(int(list(Months.keys()).index(i))+1)+"-"+date_var.split()[0])
            except:
                d["Date"]= "None"

            if list(d.values())[1] != "Zamienię":
                l.append(d)      
            else:
                pass
        print (str(page)+"/"+str(LastPage()-1)+" pages proccessed")   
    df= pd.DataFrame(l)
    df["Price"] = df["Price"].astype(float)

    pricetohigh = df['Price'] < 300
    pricetolow = df['Price'] > 60

    df = df[pricetohigh & pricetolow]
    print (df)
    
    df.to_csv("OlxOutputs/"+str(Title)+".csv")
#l = list(unique_everseen(l)) # Remove duplicates in the list
