import sys
import urllib2 
import os
import numpy as np
import pandas as pd 
import pytz
import csv
from datetime import datetime
from dateutil import parser
from xml.dom.minidom import parse
from tabulate import tabulate 


link = "https://www.pokerstars.com/datafeed_global/tournaments/all.xml"
html = urllib2.urlopen(link)
htmll = html.read()
filez = open('export.xml','w')
filez.write(htmll)
filez.close()
filez = open('export.xml','r')
dom = parse(filez)


def findChildNodeByName(parent, name):
    for node in parent.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.localName == name:
            return node
    return None


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# Splitting buyin 
def splitbi(bi): 
	s = bi
	s = s.replace('$',' ')
	sfinal = s.split('+')
	biz = float(sfinal[0])
	rakez = float(sfinal[1])
	totalbiz = float(biz + rakez)
	return totalbiz


tours = dom.getElementsByTagName("tournament")
dic = []

for num, tour in enumerate(tours):
	name = findChildNodeByName(tour, 'name')
	chips = findChildNodeByName(tour, 'chips')
	bi = findChildNodeByName(tour, 'buy_in_fee')
	game = findChildNodeByName(tour, 'game')
	description = findChildNodeByName(tour, 'description')
	startd = findChildNodeByName(tour, 'start_date')
	if bi and chips and description and name and startd is not None: 
		time = parser.parse(getText(startd.childNodes))
		now = datetime.now(pytz.utc) # Getting UTC awareness --> subtract for difference in time 
		status = time - now # Get the time difference
		start_in = int(status.total_seconds() / 60)
		if '$' in getText(bi.childNodes).encode('utf-8') and (getText(game.childNodes).encode('utf-8') == "Hold'em"):
			totalbiz = splitbi(getText(bi.childNodes))
			dic.append({'Start':start_in,'Name':getText(name.childNodes).encode('utf-8'),'Buyin': totalbiz,'Chips':getText(chips.childNodes),'Description':getText(description.childNodes).encode('utf-8'),'TZ':time,})

df = pd.DataFrame(dic)
df.index.name = "Tournament"
print df[df.Name.str.contains('Gtd')].head(50).to_csv(path_or_buf ='testpoker.csv', sep = ';')


with open('testpoker.csv', 'rb') as outfile:
		reader = csv.reader(outfile, delimiter=';', quotechar = '|')
		for row in reader:
			print (' | '.join(row) + '\n')





