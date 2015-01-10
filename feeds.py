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

access_token = "CAACEdEose0cBAG2IIhcw27TGPnbq9I3aYcLzAFRrxcfIqkA4IM4NRF8wG3uKdMB2SlTSRaeNeR1Yy4tecmGpqY4IuSqsNT6aUhmuv8Itwhf852mI9gaieFe93SVhc6YJPa79uel65KhSbymhfYPPZA5GOP5znwZA1XT1eAnG8jxvW2Bf29aMASuZBijAJ0BoSZAUHnGAZBxRez92C87ZBSQQ1SpZB1Tn6oZD"
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
comments.write(0, 1, "Post")
comments.write(0, 2, "Likes")
comments.write(0, 3, "Comments")
comments.write(0, 4, "likes_count")
comments.write(0, 5, "Link")
comment_row = []
error_count = []
output = open("errors_logger.txt", "w")

# Some abstraction

def get_entries(entry_id):
  entries = workbook.add_worksheet()
  try:
    data = graph.get(entry_id + "/")
    # time.sleep(1) # Lest we facebook's hit/second limit
    if 'comments' in data and 'message' in data:
      comment_row.append("")
      comments.write(len(comment_row), 0, entry_id)
      comments.write(len(comment_row), 1, data['message']) # Empty cells should be equal the number of comments
      comments.write(len(comment_row), 5, data['actions'][0]['link']) # the link

      if 'likes' in data:
        # pdb.set_trace()
        likes = []
        for like in data['likes']['data']:
          likes.append(like['id'])
        comments.write(len(comment_row), 2, str(likes))

      for entry in  data['comments']['data']:
        print ("Imports count: " + str(len(comment_row)))
        comment_row.append("") # Could use lambda here
        comments.write(len(comment_row), 3, entry['message'])
        comments.write(len(comment_row), 4, entry['like_count']) # we will have to parse from the page here to get the ones who commented.

    elif 'comments' in data: # This is a case with video posts or photos
      comment_row.append("")
      if 'caption' in data: # yet to know which type have captions.
        comments.write(len(comment_row), 1, data['caption'])

      if 'likes' in data:
        likes = []
        for like in data['likes']['data']:
          likes.append(like['id'])
        comments.write(len(comment_row), 2, str(likes))

      comments.write(len(comment_row), 0, entry_id)
      comments.write(len(comment_row), 5, data['actions'][0]['link']) # the link
      for entry in  data['comments']['data']:
        print ("Imports count: " + str(len(comment_row)))
        comment_row.append("") # could use lambda here
        comments.write(len(comment_row), 3, entry['message'])
        comments.write(len(comment_row), 4, entry['like_count'])

    elif ('message' in data): # This is a post (message) with no comments
      comment_row.append("")
      if 'likes' in data:
        likes = []
        for like in data['likes']['data']:
          likes.append(like['id'])
        comments.write(len(comment_row), 2, str(likes))

      comments.write(len(comment_row), 0, entry_id)
      comments.write(len(comment_row), 5, data['actions'][0]['link']) # the link
      comments.write(len(comment_row), 1, data['message'])
      # How do we find likes here?
    elif 'data' in data:
      # I saw this once, may be I was delirious.. but if gets logged, handle it!
      output.write("entry_id %s is super weird\n" %(entry_id))
    else: # A media post with no message or comments
      comment_row.append("")
      comments.write(len(comment_row), 0, entry_id)
      comments.write(len(comment_row), 5, data['actions'][0]['link'])

      if 'caption' in data:
        comments.write(len(comment_row), 1, data['caption'])
      if 'likes' in data:
        likes = []
        for like in data['likes']['data']:
          likes.append(like['id'])
        comments.write(len(comment_row), 2, str(likes))

  except Exception, e:
    error_count.append("")
    print e
    output.write("Error while importing entry: %s of type- %s %s \n" %(entry_id, e, type(e))) # Log the error, if there is situation unhandled situation
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





