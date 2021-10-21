
from abc import ABCMeta, abstractmethod
import sys
from bs4 import BeautifulSoup 
import re
import urllib.request
import xlwt
import requests
from PIL import Image
from io import BytesIO
import json

from xlwt.Worksheet import Worksheet
import b

def getData(baseurl):
    findLink = re.compile(r'<a href="(.*?)">')
    findImgSrc = re.compile(r'<img.*src="(.*?)".*/>',re.S)
    findTitle = re.compile(r'<span class="title">\s*(.*)\s*</span>')
    findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
    findJudge = re.compile(r'<span>([0-9]*)人评价</span>')
    findInq = re.compile(r'<span\s*class="inq"\s*>(.*?)</span>')
    findBd = re.compile(r'<p class="">(.*?)</p>',re.S)
    datalist=list()
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")
        resultSet = soup.find_all('div',class_="item")
        for item in resultSet:
            data=[]
            itemstr = str(item)
            itemstr =itemstr.replace(u'\xa0',u' ')
            link=re.findall(findLink,itemstr)[0]
            src = re.findall(findImgSrc,itemstr)[0]
            title = ''.join(re.findall(findTitle,itemstr))
            rating = re.findall(findRating,itemstr)[0]
            judge = re.findall(findJudge,itemstr)[0]
            inq = ''.join(re.findall(findInq,itemstr))
            bd = re.findall(findBd,itemstr)[0].strip()
            data.append(link)
            data.append(src)
            data.append(title)
            data.append(rating)
            data.append(judge)
            data.append(inq)
            data.append(bd)
            datalist.append(data)
    return datalist

def saveData(savepath,datalist):
    workbook = xlwt.Workbook(encoding="utf-8")
    Worksheet = workbook.add_sheet('sheet')
    i=0
    j=0
    for data in datalist:
        for info in data:
            Worksheet.write(i,j,info)
            j=j+1
        i=i+1
        j=0
    workbook.save(savepath)
    pass

def askURL(url):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
    request=urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def main():
    baseUrl = "https://movie.douban.com/top250?start="
    datalist = getData(baseUrl)
    xlsPath=".\\top250.xls"
    saveData(xlsPath,datalist)

if __name__=="__main__":
    main()

