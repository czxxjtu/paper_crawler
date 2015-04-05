# utf-8
import os
import json

from bs4 import BeautifulSoup
import re

__author__ = 'Choi'


dirName = "html"
dataArray = []


# Split Reference Data
def splitRefData(block):
    blockItem = block.select("p")
    referenceObject = {}
    referenceObject['author'] = []
    if blockItem.__len__() == 3:
        for idx, item in enumerate(blockItem):
            if idx == 0:
                tempArray = [x.strip() for x in item.text.split(', ')]
                for each in tempArray:
                    print each
                    referenceObject['author'].append(re.sub("^[0-9]+\.+\s", "", each))
            elif idx == 1:
                referenceObject['title'] = item.text
            elif idx == 2:
                referenceObject['journal'] = item.text
    dataObject['references'].append(referenceObject)


def splitAuthorData(block):
    blockItem = block.select("div.copy h3 a")
    for item in blockItem:
        dataObject['author'].append(item.text)


for f in os.listdir(dirName):
    # Load HTML file
    rawHtml = file(dirName + "/" + f, 'rb')
    soup = BeautifulSoup(rawHtml)
    rawHtml.close()

    dataObject = {}

    blockRef = soup.select("#references div.body")
    paperName = soup.select("#at-glance div.text h1")[0].text.replace(":", "").replace(",", "")
    dataObject['title'] = paperName
    dataObject['references'] = []

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