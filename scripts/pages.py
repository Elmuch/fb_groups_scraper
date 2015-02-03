import client
import xlsxwriter
import pdb
from urlparse import urlparse
from urlparse import parse_qs
import time


def extract(feeds, entries,row=[]):
  graph = client.graph_client()
  types = []
  def get_post(row, feed):
    if 'actions' in feed:
      row.append("")

      entries.write(len(row), 16, feed['actions'][0]['link'])
      entries.write(len(row), 0, feed['id'])
      
      if feed['type'] == 'link':
        entries.write(len(row), 6, "Link")

      if (feed['type'] == 'video') or (feed['type'] == 'photo'):
        entries.write(len(row), 6, "Post Media")

      if 'message' in feed and feed['type'] == 'status':
        entries.write(len(row), 6, "Post message")

      if 'caption' in feed:
        entries.write(len(row), 14, feed['caption'])
      if 'message' in feed:
        entries.write(len(row), 12, feed['message'])
        
      if 'description' in feed:
        entries.write(len(row), 15, feed['description'])

      ids = []
      names = []
      if 'to' in feed:
        for post_to in feed['to']['data']:
          ids.append(post_to['id'])
          names.append(post_to['name'])
      else: # At this point, the post is made by the page (self)
          ids.append(feed['from']['id'])
          names.append(feed['from']['name'])

      if 'likes' in feed:
        entries.write(len(row), 11, len(feed['likes']['data']))
      else:
        entries.write(len(row), 11, 0)

      if 'comments' in feed:
        entries.write(len(row), 13, len(feed['comments']['data']))
      else:
        entries.write(len(row), 13, 0)

      entries.write(len(row), 1, (str(ids)))
      entries.write(len(row), 2, (str(names)))
      entries.write(len(row), 3, feed['from']['id'])
      entries.write(len(row), 4, feed['from']['name'])
      entries.write(len(row), 9, feed['created_time'])

  def get_likes(row, feed):
    if 'likes' in feed:
      ids = []
      names = []
      if "to" in feed:
        for like_to in feed['to']['data']:
          ids.append(like_to['id'])
          names.append(like_to['name'])
      else: # At this point, the post is made by the page (self)
        ids.append(feed['from']['id'])
        names.append(feed['from']['name'])

      for like_data in  feed['likes']['data']:
        row.append("")
        entries.write(len(row), 1, (str(ids)))
        entries.write(len(row), 2, (str(names)))
        entries.write(len(row), 3, like_data['id'])
        entries.write(len(row), 4, like_data['name'])
        entries.write(len(row), 5, feed['id'])
        entries.write(len(row), 6, "SubPostLike")

  def get_comments(row, feed):
    if 'comments' in feed:
      for comment_data in feed['comments']['data']:
        row.append("")
        ids = []
        names = []
        if "to" in feed:
          for post_to in feed['to']['data']:
            ids.append(post_to['id'])
            names.append(post_to['name'])
        else: 
          ids.append(feed['from']['id'])
          names.append(feed['from']['name'])
    
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
        else: # At this point, the post is made by the page (self)
          ids.append(feed['from']['id'])
          names.append(feed['from']['name'])

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

  def get_comments_likes(feed):
    if "comments" in feed:
      for comment in feed['comments']['data']:
        if comment['like_count'] != 0:
          data = graph.get(comment['id']+"?fields=likes")

          ids = []
          names = []
          if 'to' in feed:
            for like_to in feed['to']['data']:
              ids.append(like_to['id'])
              names.append(like_to['name'])
          if 'likes' in data:
            for like_data in  data['likes']['data']:
              row.append("")
              entries.write(len(row), 1, (str(ids)))
              entries.write(len(row), 2, (str(names)))
              entries.write(len(row), 3, like_data['id'])
              entries.write(len(row), 4, like_data['name'])
              entries.write(len(row), 5, comment['id'])
              entries.write(len(row), 6, "SubPostCommentLike")

  def get_comments_replies_likes(comment_reply):
    if comment_reply['id'].find("_") == -1:
      data = graph.get(comment_reply['id']+"_"+comment_reply['id']+"?fields=likes") # Get the comment likes from a different API-endpoint
    else:
      data = graph.get(comment_reply['id']+"?fields=likes")
      names = []
      ids = []
      if 'to' in data:
        for like_to in comment_reply['to']['data']:
          ids.append(like_to['id'])
          names.append(like_to['name'])
      else: # At this point, the post is made by the page (self)
          ids.append(feed['from']['id'])
          names.append(feed['from']['name'])

    if 'likes' in data:
      for like_data in  data['likes']['data']:
        entries.write(len(row), 1, (str(ids)))
        entries.write(len(row), 2, (str(names)))
        entries.write(len(row), 3, like_data['id'])
        entries.write(len(row), 4, like_data['name'])
        entries.write(len(row), 5, comment_reply['id']) # Parent is the reply to a comment
        entries.write(len(row), 6, "SubPostCommentReplyLike")

  def get_shares(feed):
    if 'actions' in feed: 
      data = ""
      try:
        if 'status_type' in feed and feed['status_type'] == 'shared_story':
          url = feed['link']
          query = parse_qs(urlparse(url).query)
          if 'story_fbid' in query:
            story_fbid = query['story_fbid'][0]
            u_id = parse_qs(urlparse(url).query)['id'][0]
            data = graph.get(str(u_id) + "_"+ str(story_fbid))
            # pdb.set_trace()
            entries.write(len(row), 17, data['from']['id'])
            entries.write(len(row), 18, data['from']['name'])
            entries.write(len(row), 10, data['shares']['count']) # Note this is the original post
          else: # Get the link and get the share data, this is the case when someone finds a link on
                # on the internet and shares it.''
            data = graph.get("?id="+url)
            if 'shares' in data:
              entries.write(len(row), 10, data['shares']) # there are some issues here
            entries.write(len(row), 17, feed['from']['id'])
            entries.write(len(row), 18, feed['from']['name'])
            # is entry type here a link?
      except Exception, e:
        pdb.set_trace()


  for feed in feeds:
    print  "Importing Feed:", str(feed['id'])
    get_post(row, feed)
    get_shares(feed)
    get_comments(row, feed)
    get_likes(row,feed)
    get_comments_likes(feed)