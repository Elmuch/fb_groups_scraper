
import re
from urlparse import urlparse
from urlparse import parse_qs
import time
import xlsxwriter
import pdb
import client

graph = client.graph_client()

# Get my latest posts per group
# groups  = ['324309874271040','206494919465453','255488514638473','334271300068285']
groups  = ['324309874271040'] # Use this for testing, otherwise use the four groups, remember to uncomment  time.sleep(1)
pages = ['202027666597795']

feeds = []
for group_id in pages:
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
comments.write(0, 1, "EntryType")
comments.write(0, 2, "Post")
comments.write(0, 3, "Likes")
comments.write(0, 4, "Comments")
comments.write(0, 5, "likes")
comments.write(0, 6, "likes_count")
comments.write(0, 7, "Link")
comment_row = []
error_count = []
output = open("errors_logger.txt", "w") # For logging the errors
posi = [0]

def get_likes(data, col):
  if 'likes' in data:
    likes = []
    for like in data['likes']['data']:
      likes.append(str(like['id']))
      comments.write(len(comment_row), col, str(likes))

def get_comments(entry_id, data):
  count = 0
  for entry in  data['comments']['data']:
    count +=1
    comments.write(len(comment_row) , 4, entry['message'])
    comments.write(len(comment_row) , 6, entry['like_count']) # we will have to parse from the page here to get the ones who commented
    if entry['id'].find("_") == -1:
      comments_data = graph.get(entry_id + "_" + entry['id'] + "?fields=likes") # Get the comment likes from a different API-endpoint
    else:
      comments_data = graph.get(entry['id']+"?fields=likes")
    get_likes(comments_data, 5)
    comment_row.append("") # Couldad use lambda here

  posi.append(count)

def get_id_and_link(entry_id, data):
  comment_row.append("")
  comments.write(len(comment_row), 0, entry_id)
  if 'actions' in data:
      comments.write(len(comment_row), 7, data['actions'][0]['link']) # the link

def get_caption(data): # This might be uncessary but I thought of including it.
  if 'caption' in data:
    comments.write(len(comment_row), 2, data['caption']) # Note, it get imported onto the posts column

def get_entries(entry_id):
  print ("Importing Feed: %s" %(entry_id))
  print "rows count" + str(len(comment_row))
  try:
    data = graph.get(entry_id + "/")
    # time.sleep(1) # Lest we facebook's hit/second limit, one second is too long. Ideal way is to set a timer and a delay. multi-thread??

    if 'comments' in data and 'message' in data:
      get_id_and_link(entry_id, data)
      comments.write(len(comment_row), 2, data['message']) # Empty cells should be equal the number of comments
      comments.write(len(comment_row), 1, 'message')
      get_likes(data, 3)
      get_comments(entry_id, data)

    elif 'comments' in data: # This is a case with video posts or photos
      get_id_and_link(entry_id, data)
      comments.write(len(comment_row), 1, 'media')
      get_caption(data)
      get_likes(data, 3)
      get_comments(entry_id, data)

    elif ('message' in data): # This is a post (message) with no comments
      get_id_and_link(entry_id, data)
      comments.write(len(comment_row), 1, 'media')
      comments.write(len(comment_row), 2, data['message'])
      get_likes(data, 3)
    elif 'data' in data: # I saw this once, may be I was delirious.. but if it gets logged, handle it!
      output.write("entry_id %s is super weird\n" %(entry_id))

    else: # A media post with no message or comments
      get_id_and_link(entry_id, data)
      comments.write(len(comment_row), 1, 'media')
      get_caption(data)
      get_likes(data, 3)

  except Exception, e:
    error_count.append("")
    print e
    output.write("Error while importing entry: %s of type- %s %s \n" %(entry_id, e, type(e))) # Log the error, if there is situation unhandled
    # pdb.set_trace()

row = 0
worksheet.write(0, 0, "MemberName")
worksheet.write(0, 1, "MemberID")
worksheet.write(0, 2, "EntryID")
worksheet.write(0, 3, "GroupID")   # This is a list, because of tags, Hence a representative of all tagged
worksheet.write(0, 4, "GroupName") # This is a list, because of tags, Hence a representative of all tagged
worksheet.write(0, 5, "AssociatedID")


for feed in feeds:
  row += 1
  get_entries(feed['id'])
  worksheet.write(row, 0, feed['from']['name'])
  worksheet.write(row, 1, feed['from']['id'])
  worksheet.write(row, 2, feed['id'])

  names, ids = [], []
  if 'to' in feed:
    for tag in feed['to']['data']:
      names.append(tag['name'])
      ids.append(str(tag['id']))
    worksheet.write(row, 3, str(ids))
    worksheet.write(row, 4, str(names))

print "\n Total entries imported: %s Not imported: %s" %(len(feeds), len(error_count))
output.write("\n Total total logged: %s" %(len(error_count)))

workbook.close()
output.close()





