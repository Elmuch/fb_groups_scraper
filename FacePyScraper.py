#!/usr/bin/env python

from facepy import GraphAPI
import re
from urlparse import urlparse
from urlparse import parse_qs

# import facebook

access_token = "CAACEdEose0cBAKkisdz1VZCnTUnWXwuhCZAEZAtxrM3b2yoeovjasMUzxBodeAN8ZAzl12eNJX1fZA48CSBscnnD1SoO8oIkYs8TUBc2mAEm4fIZC9Hncx5Af8LZByHSXm5atrMW7npYSSyn83pqWUMbJZBUjBNZBvxZA5mxXiijCDo5DKUZAdwNVeqsj4gwZAZCZAGGyZCuImMPW86hwuKV2UNcQYVxSCRkG95RsAZ"
graph = facepy.GraphAPI(access_token)


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







