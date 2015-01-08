#!/usr/bin/env python

from facepy import GraphAPI
import re
from urlparse import urlparse
from urlparse import parse_qs

# import facebook

access_token = "CAACEdEose0cBAHg92ixC5QSnZBoVhfPSAuQccXGHUqtXhQZAGbguciI3EnWducBoK9nxoyhZCL9vTMZBVe5oOhiZCMpcq3Xnuyw2Mh7L1pgMkY96yBOmWVejDnjZAGIafEelI12THM79vgW7aikvakFyht2uHMzcEYGmQt4ZANfP5vHKLG4QZClHNZAxB0pbcZACG1hQZB9mBW37IdD46BZBpZBRfPRJExQttLvgZD"
graph = GraphAPI(access_token)


# Get my latest posts

myuntil = ""
nextuntil = ""
same = False
alldata = []

while not same:
  myuntil = nextuntil
  myblob = graph.get('324309874271040/feed?limit=999999' + myuntil)
  print str(len(myblob['data'])) + " Records fetched."
  nextuntil = "&until=" + parse_qs(urlparse(myblob['paging']['next']).query)["until"][0]

  # print nextuntil
  same = (myuntil == nextuntil)

  # print myblob['data']
  if not same:
    alldata = alldata + myblob['data']

  # print myblob['paging']['next']
  # print query.fragment(1)

print str(len(alldata)) + " Recrords in total to parse."

for i in range(1,len(alldata)):
  print str(i) + ": " + str(alldata[i].keys())
  print alldata[i]['from']


#print temp['paging']['next']
#print temp['data'][0]['from']['id'] + ": " + temp['data'][0]['from']['name']







