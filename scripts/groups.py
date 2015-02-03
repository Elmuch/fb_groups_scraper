
# Groups
#
#!/usr/bin/env python

import client
import xlsxwriter
import pdb

def extract(feeds, entries, row=[]):
  graph = client.graph_client()
  types = []

  def get_comments(row, feed):
    if 'comments' in feed:
      for comment_data in feed['comments']['data']:
        row.append("")
        ids = []
        names = []
        for post_to in feed['to']['data']:
          ids.append(post_to['id'])
          names.append(post_to['name'])
    
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
        for post_to in feed['to']['data']:
          ids.append(post_to['id'])
          names.append(post_to['name'])

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
      for like_to in comment_reply['to']['data']:
        ids.append(like_to['id'])
        names.append(like_to['name'])

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
    row.append("")
    print feed['type']
    if feed['id'] == "324309874271040_796616113707078":
      pdb.set_trace()

    # if 'link' in feed:
    #     print feed['link']

    entries.write(len(row), 15, feed['actions'][0]['link'])
    entries.write(len(row), 0, feed['id'])

    # Get the post type
    if 'caption' in feed or feed['type'] == 'photo':
      entries.write(len(row), 6, "Post media")
      if 'caption' in feed:
        entries.write(len(row), 14, feed['caption'])
    elif 'message' in feed:
        entries.write(len(row), 6, "Post message")
        entries.write(len(row), 12, feed['message'])
    else:
      entries.write(len(row), 6, "Post media") # This has been a photo all along but I dont want to assume.

    ids = []
    names = []
    for post_to in feed['to']['data']:
      ids.append(post_to['id'])
      names.append(post_to['name'])

    if 'likes' in feed:
      entries.write(len(row), 11, len(feed['likes']['data']))
    else:
      entries.write(len(row), 11, 0)

    if 'comments' in feed:
      entries.write(len(row), 13, len(feed['comments']['data']))
    else:
      entries.write(len(row), 13, 0)

    if 'description' in feed:
      pdb.set_trace() # pretty sure there is no description key in the feed dict

    entries.write(len(row), 1, (str(ids)))
    entries.write(len(row), 2, (str(names)))
    entries.write(len(row), 3, feed['from']['id'])
    entries.write(len(row), 4, feed['from']['name'])
    entries.write(len(row), 9, feed['created_time'])

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
        
  def get_likes(row, feed):
    if 'likes' in feed:
      ids = []
      names = []
      for like_to in feed['to']['data']:
        ids.append(like_to['id'])
        names.append(like_to['name'])

      for like_data in  feed['likes']['data']:
        row.append("")
        entries.write(len(row), 1, (str(ids)))
        entries.write(len(row), 2, (str(names)))
        entries.write(len(row), 3, like_data['id'])
        entries.write(len(row), 4, like_data['name'])
        entries.write(len(row), 5, feed['id'])
        entries.write(len(row), 6, "SubPostLike")


  def get_shares(feed):
     # parse_qs(urlparse(url).query)['story_fbid']
     # parse_qs(urlparse(url).query)['id']
    # if "status_type" == "shared_story"
    # if 'shares' in feed:
    # Get the count here
    data = ""
    # pdb.set_trace()
    try:
      if 'link' in feed:
        url = feed['link']
        story_fbid = parse_qs(urlparse(url).query)['story_fbid'][0]
        u_id = parse_qs(urlparse(url).query)['id'][0]
        data = graph.get(str(u_id) + "_"+ str(story_fbid))
        entries.write(len(row), 16, data['from']['id'])
        entries.write(len(row), 17, data['from']['name'])

      if 'message' in data:
        entries.write(len(row), 18, data['message'])
    except Exception, e:
      print e 
      pdb.set_trace

  for feed in feeds:
    print  "Importing Feed:", str(feed['id'])
    get_post(row, feed)
    get_shares(feed)
    get_comments(row, feed)
    get_likes(row,feed)
    get_comments_likes(feed)

  # print types
