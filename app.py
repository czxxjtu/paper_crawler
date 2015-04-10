# coding=utf-8
import os
import json

from bs4 import BeautifulSoup
import re

__author__ = 'Choi'


dirName = "html"
dataArray = []


def splitRefData(block):
    blockItem = block.select("p")
    print blockItem
    if blockItem.__len__() == 0:
        print "Null"
    elif blockItem.__len__() == 3:
        for idx, item in enumerate(blockItem):
            if idx == 0:
                tempString = ""
            elif idx == 1:
                tempString = tempString + item.text + ", "
            elif idx == 2:
                tempString = tempString + item.text
    elif blockItem.__len__() == 1:
        for item in blockItem:
            tempString = re.sub("[0-9]+\. ", "", item.text)
    elif blockItem.__len__() == 2:
        for idx, item in enumerate(blockItem):
            if idx == 0:
                tempString = re.sub("[0-9]+\. ", "", item.text) + ", "
            elif idx == 1:
                tempString = tempString + item.text

    tempArray = []
    _tempArray = re.split(',|\.', tempString)
    for item in _tempArray:
        tempArray.append(item.lstrip())
    outArray = [{
        "string": "",
        "length": 0
    }, {
        "string": "",
        "length": 0
    }]
    isLeft = True

    for item in tempArray:
        if item == outArray[0].get("string") or item == outArray[1].get("string"):
            print item + " / " + outArray[0].get("string") + " / " + outArray[1].get("string")
            continue
        if isLeft:
            if item.__len__() > outArray[0].get("length"):
                outArray.pop(0)
                outArray.append({
                    "string": item,
                    "length": item.__len__()
                })
        elif not isLeft:
            if item.__len__() > outArray[1].get("length"):
                outArray.pop(1)
                outArray.append({
                    "string": item,
                    "length": item.__len__()
                })
        if outArray[0].get("length") < outArray[1].get("length"):
            isLeft = True
        elif outArray[0].get("length") > outArray[1].get("length"):
            isLeft = False

        outString = outArray[0].get("string")
        outString = re.sub("^\u201c", "", outString)
        outString = re.sub("\u201d$", "", outString)

    dataObject['references'].append(outString)


def splitAuthorData(block):
    blockItem = block.select("div.copy h3 a")
    for item in blockItem:
        dataObject['author'].append(item.text)


for f in os.listdir(dirName):
    dataObject = {}

    # Load HTML file
    rawHtml = file(dirName + "/" + f, 'rb')
    print "==========================" + rawHtml.name
    dataObject['file'] = rawHtml.name
    soup = BeautifulSoup(rawHtml)
    rawHtml.close()



    blockRef = soup.select("#references div.body")
    paperName = soup.select("#at-glance div.text h1")[0].text.replace(",", "")#.replace(":", "")

    # title
    dataObject['title'] = paperName
    dataObject['references'] = []

    # date
    if soup.select("#dt_conf_date"):
        dataObject['date'] = re.sub("^\n", "", re.sub("\n$", "", soup.select("#dt_conf_date")[0].text))
    elif soup.select("#dt_dop"):
        dataObject['date'] = re.sub("^\n", "", re.sub("\n$", "", soup.select("#dt_dop")[0].text))
    elif soup.select("#dt_date"):
        dataObject['date'] = re.sub("^\n", "", re.sub("\n$", "", soup.select("#dt_date")[0].text))
    else:
        dataObject['date'] = "none"

    # Reference
    for item in blockRef:
        splitRefData(item)

    # Abstract
    blockAbstract = soup.select("#at-glance div.text p")[0].text
    dataObject['abstract'] = blockAbstract

    # Article
    # blockArticle = soup.select("#article")[0].text.replace("{", "").replace("}", "").replace("[", "").replace("]", "")
    # dataObject['article'] = re.sub("\W|_^\s", "", blockArticle)

    # Author
    dataObject['author'] = []
    blockAuthor = soup.select("#authors")
    splitAuthorData(blockAuthor[0])

    dataArray.append(dataObject)

fileJson = file("output/output.json", 'w')
fileJson.write(json.dumps(dataArray))
fileJson.close()