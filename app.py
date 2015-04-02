# utf-8
import os
import json

from bs4 import BeautifulSoup

__author__ = 'Choi'


dirName = "html"

def splitRefData(block):
    blockItem = block.select("p")
    if blockItem.__len__() == 3:
        for idx, item in enumerate(blockItem):
            fileRef.write(item.text.encode('utf8') + "\n")
        fileRef.write("\n")


for f in os.listdir(dirName):
    # Load HTML file
    rawHtml = file(dirName + "/" + f, 'rb')
    soup = BeautifulSoup(rawHtml)
    rawHtml.close()

    blockRef = soup.select("#references div.body")
    paperName = soup.select("#at-glance div.text h1")[0].text.replace(":", "").replace(",", "")

    # Reference
    fileRef = file("output/" + paperName + "_reference.txt", 'w')

    for item in blockRef:
        splitRefData(item)

    fileRef.close()

    # Abstract
    blockAbstract = soup.select("#at-glance div.text p")[0].text
    fileAbstract = file("output/" + paperName + "_abstract.txt", 'w')
    fileAbstract.write(blockAbstract)
    fileAbstract.close()