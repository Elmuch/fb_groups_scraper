# Get page and group data
# 

import pdb
from urlparse import urlparse
from urlparse import parse_qs

class Page(object):
  """Page class"""
  def __init__(self, graph, feed, csv_writer):
    self.feed       = feed
    self.graph      = graph
    self.csv_writer = csv_writer    
  
  def get_post(self):    
    if 'actions' in self.feed:
      ids = []
      names = []
      share_count = 0
      likes_count = 0
      comments_count = 0
      msg_content = ""
      caption = ""
      description = ""
      entry_type = ""
      original_mbr_id = ""
      original_mbr_name = ""
      if self.feed['type'] == 'link':
        entry_type = "link"

      if (self.feed['type'] == 'video' or  self.feed['type'] == 'photo'):
        entry_type = "Post Media"

      if 'message' in self.feed and self.feed['type'] == 'status':
        entry_type = "Post message"
      if 'message' in self.feed:
        msg_content = self.feed['message'].encode('ascii', 'ignore')
      if 'caption' in self.feed:
        caption = self.feed['caption'].encode('ascii', 'ignore')
      if 'description' in self.feed:
        description = self.feed['description'].encode('ascii', 'ignore')
      if 'caption' in self.feed and self.feed['type'] == "status":
        entry_type = "Post Media"
      if ('shares' in self.feed):
        share_count = self.feed['shares']['count']

      if 'likes' in self.feed:
        likes_count = len (self.feed['likes']['data'])

      if 'comments' in self.feed:
        comments_count = len (self.feed['comments']['data'])

      if 'to' in self.feed:
        for post_to in self.feed['to']['data']:
          ids.append(post_to['id'])
          names.append(post_to['name'])
      else: # At this point, the post is made by the page (self)
          ids.append(self.feed['from']['id'])
          names.append(self.feed['from']['name'])
      hyper_link = self.feed['actions'][0]['link'].encode('ascii', 'ignore')

      # Lord of good code forgive me :)
      if 'status_type' in self.feed and self.feed['status_type'] == 'shared_story':
        url = self.feed['link']
        query = parse_qs(urlparse(url).query)
        if 'story_fbid' in query:
          story_fbid = query['story_fbid'][0]
          u_id = parse_qs(urlparse(url).query)['id'][0]
          data = self.graph.get(str(u_id) + "_"+ str(story_fbid))
          # pdb.set_trace()
          original_mbr_id = data['from']['id']
          original_mbr_name = data['from']['name']
        else: # Get the link and get the share data, this is the case when someone finds a link on
              # on the internet and shares it.''
          data = self.graph.get("?id="+url)
          original_mbr_id = self.feed['from']['id']
          original_mbr_name = self.feed['from']['name']

      self.csv_writer.writerow((self.feed['id'], str(ids), 
                      str(names), self.feed['from']['id'],
                      self.feed['from']['name'].encode('ascii', 'ignore'),"NA", entry_type,
                      self.feed['created_time'],share_count, likes_count,comments_count,caption,
                      msg_content, description,hyper_link, 
                      original_mbr_id, original_mbr_name))


  def get_likes(self):
    if 'likes' in self.feed:
      ids = []
      names = []
      if "to" in self.feed:
        for like_to in self.feed['to']['data']:
          ids.append(like_to['id'])
          names.append(like_to['name'])
      else: # At this point, the post is made by the page (self)
        ids.append(self.feed['from']['id'])
        names.append(self.feed['from']['name'])

      for like_data in  self.feed['likes']['data']:
        self.csv_writer.writerow(("NA", str(ids), 
                        str(names), like_data['id'],
                        like_data['name'].encode('ascii', 'ignore'),self.feed['id'], "SubPostLike",
                        "NA", "NA", "NA","NA","NA","NA", "NA","NA","NA","NA"))

  def get_comments(self):
    if 'comments' in self.feed:
      comments_count = 0
      for comment_data in self.feed['comments']['data']:
        ids = []
        names = []
        if "to" in self.feed:
          for post_to in self.feed['to']['data']:
            ids.append(post_to['id'])
            names.append(post_to['name'])
        else: 
          ids.append(self.feed['from']['id'])
          names.append(self.feed['from']['name'])
    
        replies = self.get_comments_replies(comment_data['id'])
        if replies['data'] != []:
          comments_count = len(replies['data']) 
        msg_content = comment_data['message'].encode('ascii', 'ignore')
        self.csv_writer.writerow((comment_data['id'], str(ids), 
                        str(names), comment_data['from']['id'],
                        comment_data['from']['name'].encode('ascii', 'ignore'),self.feed['id'], "SubPostComment",
                        comment_data['created_time'], "NA", comment_data['like_count'], "NA", "NA",
                        msg_content, "NA", "NA","NA","NA","NA","NA"))

  # Get comments of likes
  def get_comments_replies(self, comment_id):
    data = self.graph.get(comment_id + "/comments") # get replies
    if data['data'] != []:
      for comment_data in data['data']:
        ids = []
        names = []
        if 'to' in self.feed:
          for post_to in self.feed['to']['data']:
            ids.append(post_to['id'])
            names.append(post_to['name'])
        else: # At this point, the post is made by the page (self)
          ids.append(self.feed['from']['id'])
          names.append(self.feed['from']['name'])
        msg_content = comment_data['message'].encode('ascii', 'ignore')
        self.csv_writer.writerow((comment_data['id'], str(ids), 
                        str(names), comment_data['from']['id'],
                        comment_data['from']['name'].encode('ascii', 'ignore'), comment_id, "SubPostCommentReply",
                        comment_data['created_time'], "NA", comment_data['like_count'],"NA","NA",
                        msg_content, "NA", "NA","NA","NA","NA"))      
    
        if comment_data['like_count'] != 0:
          self.get_comments_replies_likes(comment_data)

    return data

  def get_comments_likes(self):
    if "comments" in self.feed:
      for comment in self.feed['comments']['data']:
        if comment['like_count'] != 0:
          data = self.graph.get(comment['id']+"?fields=likes")

          ids = []
          names = []
          if 'to' in self.feed:
            for like_to in self.feed['to']['data']:
              ids.append(like_to['id'])
              names.append(like_to['name'])
          else:
            ids.append(self.feed['from']['id'])
            names.append(self.feed['from']['name'])
          if 'likes' in data:
            for like_data in  data['likes']['data']:
              self.csv_writer.writerow(("NA", str(ids), 
                      str(names), like_data['id'],
                      like_data['name'].encode('ascii', 'ignore'),data['id'], "SubPostCommmentLike",
                      "NA", "NA", "NA","NA", "NA", "NA","NA","NA","NA"))

  def get_comments_replies_likes(self, comment_reply):
    if comment_reply['id'].find("_") == -1:
      data = self.graph.get(comment_reply['id']+"_"+comment_reply['id']+"?fields=likes") # Get the comment likes from a different API-endpoint
    else:
      data = self.graph.get(comment_reply['id']+"?fields=likes")
      names = []
      ids = []
      if 'to' in data:
        for like_to in comment_reply['to']['data']:
          ids.append(like_to['id'])
          names.append(like_to['name'])
      else: # At this point, the post is made by the page (self)
          ids.append(self.feed['from']['id'])
          names.append(self.feed['from']['name'])

    if 'likes' in data:
      for like_data in  data['likes']['data']:
        self.csv_writer.writerow(("NA", str(ids), 
                        str(names), like_data['id'],
                        like_data['name'].encode('ascii', 'ignore'),data['id'], "SubPostCommmentReplyLike",
                        "NA", "NA", "NA","NA", "NA", "NA","NA","NA","NA"))
  def extract(self):
    self.get_post()
    self.get_comments()
    self.get_likes()
