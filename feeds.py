#!/usr/bin/env python

from facepy import GraphAPI
import re
from urlparse import urlparse
from urlparse import parse_qs
import xlsxwriter
import time
import pdb

# import groups
# import facebook

access_token = "CAACEdEose0cBAI6VMehjoAXFZB1HKSRGAtkojCKtrn89L6yfVjNfUMfE8lfZCx4McVWjFvs09KLYK1o6eSCOSKRZAIzVxVPfBqsa4jXYsXiqMuZClQciA8C1bZBRMxdCsQcKDQ019EVVyIrhtZBgnZAHBIi2EFWtTpXyvMVsGJIjDbiA76KNoMRsmHlpGcZAQCIrwWsvZChPDN2PWSmB760R6PG30sDwDZCSMZD"
graph = GraphAPI(access_token)

# Get my latest posts per group
# groups  = ['324309874271040','206494919465453','255488514638473','334271300068285']
groups  = ['324309874271040']
feeds = []
for group_id in groups:
  myuntil = ""
  nextuntil = ""
  same = False
  alldata = []

  while not same:
    myuntil = nextuntil

    data = graph.get(group_id + "/feed?limit=999999" + nextuntil)
    nextuntil = "&until=" + parse_qs(urlparse(data['paging']['next']).query)["until"][0]

    same = (myuntil == nextuntil)
    if not same:
      alldata += data['data']
      feeds += alldata

  print "Total imports from GroupID: %s  %s" %(group_id, len(alldata))

print "Total imports from all the groups: " + str(len(feeds))

# Get the entry details
#
workbook = xlsxwriter.Workbook('feeds.xlsx')
worksheet = workbook.add_worksheet()
comments  = workbook.add_worksheet()

comments.write(0, 0, "EntryID")
comments.write(0, 1, "Comments")
comments.write(0, 2, "Likes")
comment_row = []
error_count = []
output = open("errors_logger.txt", "w")
def get_entries(entry_id):
  entries = workbook.add_worksheet()
  try:
    data = graph.get(entry_id + "/")
    time.sleep(1) # Lest we facebook's hit/second limit
    if 'comments' in data:
      for entry in  data['comments']['data']:
        print ("Imports count: " + str(len(comment_row)))
        comment_row.append("") # could use lambda here
        comments.write(len(comment_row), 0, entry_id)
        comments.write(len(comment_row), 1, entry['message'])
        comments.write(len(comment_row), 2, entry['like_count'])
    elif ('message' in data):
      comment_row.append("") # could use lambda here
      comments.write(len(comment_row), 0, entry_id)
      comments.write(len(comment_row), 1, data['message'])
    elif 'data' in data:
      output.write("entry_id %s is super weird\n" %(entry_id))
    else:
      comment_row.append("")
      comments.write(len(comment_row), 0, entry_id)
      comments.write(len(comment_row), 1, data['actions'][0]['link'])
      if 'likes' in data:
        comments.write(len(comment_row), 2, len(data['likes']['data']))
      else:
        comments.write(len(comment_row), 2, 0)

  except Exception, e:
    error_count.append("")
    print e
    output.write("Error while importing entry: %s of type- %s %s \n" %(entry_id, e, type(e)))
    # pdb.set_trace()
    # comments.write(0, 1, entry['likes'])

row = 0
worksheet.write(0, 0, "MemberName")
worksheet.write(0, 1, "MemberID")
worksheet.write(0, 2, "EntryType")
worksheet.write(0, 3, "EntryID")
worksheet.write(0, 4, "GroupID")
worksheet.write(0, 5, "GroupName")
worksheet.write(0, 6, "AssociatedID")


for feed in feeds:
  row += 1
  get_entries(feed['id'])
  worksheet.write(row, 0, feed['from']['name'])
  worksheet.write(row, 1, feed['from']['id'])
  worksheet.write(row, 2, feed['type'])
  worksheet.write(row, 3, feed['id'])
  worksheet.write(row, 4, feed['to']['data'][0]['id'])
  worksheet.write(row, 5, feed['to']['data'][0]['name'])

print "\n Total entries imported: %s Not imported: %s" %(len(feeds), len(error_count))
workbook.close()
output.close()





