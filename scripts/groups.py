import client
import xlsxwriter
import pdb
from urlparse import urlparse
from urlparse import parse_qs
import time


def extract(feeds, entries):
  graph = client.graph_client()

  def get_post(feed):
    ids = []
    names = []
    share_count = 0
    likes_count = 0
    comments_count = 0
    msg_content = ""
    caption = ""
    description = ""
    entry_type = ""
    original_mbr_id = 0, 
    original_mbr_name = "maasai"
    if feed['type'] == 'link':
      entry_type = "link"

    if (feed['type'] == 'video') or (feed['type'] == 'photo'):
      entry_type = "Post Media"

    if 'message' in feed and feed['type'] == 'status':
      entry_type = "Post message"
    if 'message' in feed:
      msg_content = feed['message'].encode('ascii', 'ignore')
    if 'caption' in feed:
      caption = feed['caption'].encode('ascii', 'ignore')
    if 'description' in feed:
      description = feed['description'].encode('ascii', 'ignore')

    if ('shares' in feed):
      share_count = feed['shares']['count']

    if 'likes' in feed:
      likes_count = len(feed['likes']['data'])

    if 'comments' in feed:
      comments_count = len(feed['comments']['data'])

    if 'to' in feed:
      for post_to in feed['to']['data']:
        ids.append(post_to['id'])
        names.append(post_to['name'])
    else: # At this point, the post is made by the page (self)
        ids.append(feed['from']['id'])
        names.append(feed['from']['name'])
    hyper_link = feed['actions'][0]['link'].encode('ascii', 'ignore')
 
    entries.writerow((feed['id'], str(ids), 
                    str(names),feed['from']['id'],
                    feed['from']['name'].encode('ascii', 'ignore'),"NA", entry_type,
                    feed['created_time'],share_count, likes_count,comments_count,caption,
                    msg_content, description,hyper_link, 
                    original_mbr_id, original_mbr_name))

  def get_likes(feed):
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
        entries.writerow(("NA", str(ids), 
                        str(names), like_data['id'],
                        like_data['name'].encode('ascii', 'ignore'),feed['id'], "SubPostLike",
                        "NA", "NA", "NA","NA","NA","NA", "NA","NA","NA","NA"))

  def get_comments(feed):
    if 'comments' in feed:
      comments_count = 0
      for comment_data in feed['comments']['data']:
        ids = []
        names = []
        if "to" in feed:
          for post_to in feed['to']['data']:
            ids.append(post_to['id'])
            names.append(post_to['name'])
        else: 
          ids.append(feed['from']['id'])
          names.append(feed['from']['name'])
    
        replies = get_comments_replies(comment_data['id'])
        if replies['data'] != []:
          comments_count = len(replies['data']) 
        msg_content = comment_data['message'].encode('ascii', 'ignore')
        entries.writerow((comment_data['id'], str(ids), 
                        str(names), comment_data['from']['id'],
                        comment_data['from']['name'].encode('ascii', 'ignore'),feed['id'], "SubPostComment",
                        comment_data['created_time'], "NA", comment_data['like_count'], "NA", "NA",
                        msg_content, "NA", "NA","NA","NA","NA","NA"))

  # Get comments of likes
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
        msg_content = comment_data['message'].encode('ascii', 'ignore')
        entries.writerow((comment_data['id'], str(ids), 
                        str(names), comment_data['from']['id'],
                        comment_data['from']['name'].encode('ascii', 'ignore'), comment_id, "SubPostCommentReply",
                        comment_data['created_time'], "NA", comment_data['like_count'],"NA","NA",
                        msg_content, "NA", "NA","NA","NA","NA"))      
    
        if comment_data['like_count'] != 0:
          get_comments_replies_likes(comment_data)

    return data

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
          else:
            ids.append(feed['from']['id'])
            names.append(feed['from']['name'])
          if 'likes' in data:
            for like_data in  data['likes']['data']:
              entries.writerow(("NA", str(ids), 
                      str(names), like_data['id'],
                      like_data['name'].encode('ascii', 'ignore'),data['id'], "SubPostCommmentLike",
                      "NA", "NA", "NA","NA", "NA", "NA","NA","NA","NA"))

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
        entries.writerow(("NA", str(ids), 
                        str(names), like_data['id'],
                        like_data['name'].encode('ascii', 'ignore'),data['id'], "SubPostCommmentReplyLike",
                        "NA", "NA", "NA","NA", "NA", "NA","NA","NA","NA"))

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
    get_post(feed)
    # get_shares(feed)
    get_comments(feed)
    get_likes(feed)
    get_comments_likes(feed)