#!/usr/bin/env python

from urlparse import urlparse
from urlparse import parse_qs
import client
 

def get_all(collection):
  print "-----------------Importing feeds---------------"
  try:
    graph = client.graph_client()
    feeds = []
    for c_id in collection: # why is id a reserve word????????????????
      myuntil = ""
      nextuntil = ""
      same = False
      alldata = []

      while not same:
        myuntil = nextuntil
        print "Feeds count: ", str(len(alldata))
        data = graph.get(c_id + "/feed?limit=999999" + nextuntil)
        nextuntil = "&until=" + parse_qs(urlparse(data['paging']['next']).query)["until"][0]
        same = (myuntil == nextuntil)
        if not same:
          alldata += data['data']
          feeds += alldata

      print "\n \nTotal imports from GroupID: %s  %s" %(c_id, len(alldata))
    print "Total imports from all the groups: " + str(len(feeds))
  except Exception, e:
    print e 
  # cache_feed(feeds)
  return feeds


  #############################################################


