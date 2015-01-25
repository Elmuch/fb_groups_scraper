#!/usr/bin/env python

import re
from urlparse import urlparse
from urlparse import parse_qs
import time
import xlsxwriter
import pdb
import json
import client

def extract(workbook, groups,pages=[]):
  print "-----------------Importing feeds---------------"
  graph = client.graph_client()

  def get_all_feeds():
    feeds = []
    for group_id in pages+groups:
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
    # cache_feed(feeds)
    return feeds

  feeds = get_all_feeds()

  #############################################################

  entries  = workbook.add_worksheet()

  entries.write(0, 0, "EntryID")
  entries.write(0, 1, "GroupID")
  entries.write(0, 2, "GroupName")
  entries.write(0, 3, "MemberID")
  entries.write(0, 4, "MemberName")
  entries.write(0, 5, "AssociatedID")
  entries.write(0, 6, "EntryType")
  entries.write(0, 7, "SharedParentID")
  entries.write(0, 8, "SeenCount")
  entries.write(0, 9, "TimeStamp")
  entries.write(0, 10, "ShareCount")
  entries.write(0, 11, "LikeCount")
  entries.write(0, 12, "MessageOrCommentContent")
  entries.write(0, 13, "CommentsCount")
  entries.write(0, 14, "MediaCaption")
  entries.write(0, 15, "HyperLink")

  row = []

  def get_comments(row, feed):
    if 'comments' in feed:
      for comment_data in feed['comments']['data']:
        row.append("")
        ids = []
        names = []
        if 'to' in feed:
          for post_to in feed['to']['data']:
            ids.append(post_to['id'])
            names.append(post_to['name'])
        else: # if there is no to, then this is a page feed which was posted by the page itself
          names.append(u'Maa Youth Empowerment Strategic Scheme')
          ids.append(pages[0])
        get_comments_replies(comment_data['id'])
        entries.write(len(row), 1, (str(ids)))
        entries.write(len(row), 2, (str(names)))
        entries.write(len(row), 5, feed['id'])
        entries.write(len(row), 0, comment_data['id'])
        entries.write(len(row), 3, comment_data['from']['id'])
        entries.write(len(row), 4, comment_data['from']['name'])
        entries.write(len(row), 6, "SubPostComment")
        entries.write(len(row), 9, comment_data['created_time'])
        entries.write(len(row), 11, comment_data['like_count'])
        entries.write(len(row), 12, comment_data['message'])

  def get_comments_replies(comment_id):
    data = graph.get(comment_id + "/comments") # get replies
    if data['data'] != []:
      for comment_data in data['data']:
        ids = []
        names = []
        if 'to' in feed:
          for post_to in feed['to']['data']:
            ids.append(post_to['id'])
            names.append(post_to['name'])
        else: # if there is no to, then this is a page feed which was posted by the page itself
          names.append(u'Maa Youth Empowerment Strategic Scheme')
          ids.append(pages[0])

        entries.write(len(row), 1, (str(ids)))
        entries.write(len(row), 2, (str(names)))
        entries.write(len(row), 5, feed['id'])
        entries.write(len(row), 0, comment_data['id'])
        entries.write(len(row), 3, comment_data['from']['id'])
        entries.write(len(row), 4, comment_data['from']['name'])
        entries.write(len(row), 5, comment_id) # AssociatedID will be parent comment ID
        entries.write(len(row), 6, "SubPostCommentReply")
        entries.write(len(row), 9, comment_data['created_time'])
        entries.write(len(row), 11, comment_data['like_count'])
        entries.write(len(row), 12, comment_data['message'])
        row.append("")

        if comment_data['like_count'] != 0:
          get_comments_replies_likes(comment_data)


  def get_comments_replies_likes(comment_reply):
    if comment_reply['id'].find("_") == -1:
      data = graph.get(comment_reply['id']+"_"+comment_reply['id']+"?fields=likes") # Get the comment likes from a different API-endpoint
    else:
      data = graph.get(comment_reply['id']+"?fields=likes")
      names = []
      ids = []
    if 'to' in comment_reply:
      for like_to in comment_reply['to']['data']:
        ids.append(like_to['id'])
        names.append(like_to['name'])
    else: # if there is no to, then this is a page feed which was posted by the page itself
      names.append(u'Maa Youth Empowerment Strategic Scheme')
      ids.append(pages[0])

    if 'likes' in data:
      for like_data in  data['likes']['data']:
        entries.write(len(row), 1, (str(ids)))
        entries.write(len(row), 2, (str(names)))
        entries.write(len(row), 3, like_data['id'])
        entries.write(len(row), 4, like_data['name'])
        entries.write(len(row), 5, comment_reply['id']) # Parent is the reply to a comment
        entries.write(len(row), 6, "SubPostCommentReplyLike")
        row.append("")


  def get_post(row, feed):
    if 'actions' in feed: # eliminate irrelevant
      row.append("")
      entries.write(len(row), 15, feed['actions'][0]['link'])
      if 'caption' in feed or 'picture' in feed or feed['type'] == 'photo': # This is only of identifying media entries
        entries.write(len(row), 6, "Post media")
        if 'caption' in feed:
          entries.write(len(row), 14, feed['caption'])
      elif 'message' in feed or 'description' in feed:
          entries.write(len(row), 6, "Post message")
      else:
        entries.write(len(row), 6, "Unknown") # This has been a photo all along but I dont want to assume.

      entries.write(len(row), 0, feed['id'])
      ids = []
      names = []
      if 'to' in feed:
        for post_to in feed['to']['data']:
          ids.append(post_to['id'])
          names.append(post_to['name'])
      else: # if there is no to, then this is a page feed which was posted by the page itself
        names.append(u'Maa Youth Empowerment Strategic Scheme')
        ids.append(pages[0])
        entries.write(len(row), 1, str(ids))
        entries.write(len(row), 2, str(names))

      if 'likes' in feed:
        entries.write(len(row), 11, len(feed['likes']['data']))
      else:
        entries.write(len(row), 11, 0)

      entries.write(len(row), 1, (str(ids)))
      entries.write(len(row), 2, (str(names)))
      entries.write(len(row), 3, feed['from']['id'])
      entries.write(len(row), 4, feed['from']['name'])
      entries.write(len(row), 5, "N/A") # Posts do not have associatedID, it would be self.
      entries.write(len(row), 9, feed['created_time'])
      if 'message' in feed:
        entries.write(len(row), 12, feed['message'])
      if 'description' in feed:
        entries.write(len(row), 12, feed['description'])

      if 'comments' in feed:
        entries.write(len(row), 13, len(feed['comments']['data']))
      else:
        entries.write(len(row), 13, 0)


  def get_comments_likes(feed, entry_type = ""):
    if "comments" in feed:
      for comment in feed['comments']['data']:
        if comment['like_count'] != 0:
          if feed['id'].find("_") == -1:
            data = graph.get(feed['id']+"_"+comment['id']+"?fields=likes") # Get the comment likes from a different API-endpoint
          else:
            data = graph.get(comment['id']+"?fields=likes")

          ids = []
          names = []
          if 'to' in feed:
            for like_to in feed['to']['data']:
              ids.append(like_to['id'])
              names.append(like_to['name'])
          else: # if there is no to, then this is a page feed which was posted by the page itself
            names.append(u'Maa Youth Empowerment Strategic Scheme')
            ids.append(pages[0])
          if 'likes' in data:
            for like_data in  data['likes']['data']:
              row.append("")
              # entries.write(len(row), 0, "N/A") # Like has no ID
              entries.write(len(row), 1, (str(ids)))
              entries.write(len(row), 2, (str(names)))
              entries.write(len(row), 3, like_data['id'])
              entries.write(len(row), 4, like_data['name'])
              entries.write(len(row), 5, comment['id'])
              entries.write(len(row), 6, "SubPostCommentLike")
              # entries.write(len(row), 9, "N/A") # no created_time for a like
              # entries.write(len(row), 11, "N/A")
              # entries.write(len(row), 12, "N/A")

  def get_likes(row, feed):
    if 'likes' in feed:
      ids = []
      names = []
      if 'to' in feed:
        for like_to in feed['to']['data']:
          ids.append(like_to['id'])
          names.append(like_to['name'])
      else: # if there is no to, then this is a page feed which was posted by the page itself
        names.append(u'Maa Youth Empowerment Strategic Scheme')
        ids.append(pages[0])
        entries.write(len(row), 1, str(ids))
        entries.write(len(row), 2, str(names))

      for like_data in  feed['likes']['data']:
        row.append("")
        # entries.write(len(row), 0, "N/A") # Like has no ID
        entries.write(len(row), 1, (str(ids)))
        entries.write(len(row), 2, (str(names)))
        entries.write(len(row), 3, like_data['id'])
        entries.write(len(row), 4, like_data['name'])
        entries.write(len(row), 5, feed['id'])
        entries.write(len(row), 6, "SubPostLike")
        # entries.write(len(row), 9, "N/A") # no created_time for a like
        # entries.write(len(row), 11, "N/A")
        # entries.write(len(row), 12, "N/A")

  for feed in feeds:
    print  "Importing Feed:", str(feed['id'])
    get_post(row, feed)
    get_comments(row, feed)
    get_likes(row,feed)
    get_comments_likes(feed)
