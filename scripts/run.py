#!/usr/bin/python

import xlsxwriter
import csv
import client
import feeds
from members import Member
import groups
import pages

groups_ids  = ['324309874271040','206494919465453','255488514638473','334271300068285','263457997018425']
#groups_ids  = ['324309874271040'] # Use this for testing

pages_ids = ['202027666597795','293915470632663','476919592398799']
#pages_ids = ['202027666597795']


# entries 	= work_book.start_feeds_sheet()

fds 					= open("data/feeds.csv",'wt')
mbrs 					= open("data/members.csv",'wt')
distinct_mbrs = open("data/distinct_members.csv",'wt')

entries 								 = csv.writer(fds)
csv_mbrs_writer 				 = csv.writer(mbrs)
csv_distinct_mbrs_writer = csv.writer(distinct_mbrs)

# Headers
#
entries.writerow(("EntryID", "GroupID",
									"GroupName","MemberID","MemberName",
									"AssociatedID", "EntryType",
									"TimeStamp","ShareCount","LikeCount","CommentsCount","MediaCaption",
									"MessageOrCommentContent",
									"Description","HyperLink","OriginalMemberID",
									"OriginalMembersName","OriginalMembersMessage"))

csv_mbrs_writer.writerow(("MemberID",
										"MemberName",
										"GroupID",
										"GroupName"))
csv_distinct_mbrs_writer.writerow(("MemberID", "GroupsIDs"))

# entries.write()
# row = []

# worksheet = work_book.start_members_sheet()
# groups_feeds_data = feeds.get_all(groups_ids)
# pages_feeds_data = feeds.get_all(pages_ids
graph = client.graph_client()
for i_d in pages_ids + groups_ids:
	member = Member(graph, csv_mbrs_writer, i_d, i_d)
	member.extract()
	member.extract_distinct(csv_distinct_mbrs_writer)
# lost_data = 0
# try:
# 	pages.extract(groups_feeds_data, entries) # This is just writing to excel with few calls to the API
# 	pages.extract(pages_feeds_data, entries)
# except Exception, e:
# 	lost_data += 1
# print "Unable to import:",lost_data
# work_book.close()
fds.close()
mbrs.close()
distinct_mbrs.close()