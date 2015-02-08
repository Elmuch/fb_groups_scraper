#!/usr/bin/python

from urlparse import urlparse
from urlparse import parse_qs
import time
import xlsxwriter
import csv
import feeds
import members
import groups
import pages
# import work_book
import subprocess

groups_ids  = ['324309874271040','206494919465453','255488514638473','334271300068285','263457997018425']
# groups_ids  = ['324309874271040'] # Use this for testing

pages_ids = ['202027666597795','293915470632663','476919592398799']
#pages_ids = ['202027666597795']


# entries 	= work_book.start_feeds_sheet()

fds = open("data/feeds.csv",'wt')
mbrs = open("data/members.csv",'wt')

entries = csv.writer(fds)
worksheet = csv.writer(mbrs)

# Headers
#
entries.writerow(("EntryID", "GroupID",
									"GroupName","MemberID","MemberName",
									"AssociatedID", "EntryType",
									"TimeStamp","ShareCount","LikeCount","CommentsCount","MediaCaption",
									"MessageOrCommentContent",
									"Description","HyperLink","OriginalMemberID",
									"OriginalMembersName","OriginalMembersMessage"))

worksheet.writerow(("MemberID",
										"MemberName",
										"GroupID",
										"GroupName"))
# entries.write()
# row = []
# worksheet = work_book.start_members_sheet()
groups_feeds_data = feeds.get_all(groups_ids)
pages_feeds_data = feeds.get_all(pages_ids)


members.extract(worksheet, groups_ids, pages_ids)
lost_data = 0
try:
	pages.extract(groups_feeds_data, entries) # This is just writing to excel with few calls to the API
	pages.extract(pages_feeds_data, entries)
except Exception, e:
	lost_data += 1
print "Unable to import:",lost_data
# work_book.close()
fds.close()
mbrs.close()
