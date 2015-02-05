#!/usr/bin/python

from urlparse import urlparse
from urlparse import parse_qs
import time
import xlsxwriter
import csv
import feeds
# import members
import groups
import pages
import pdb
# import work_book
import subprocess
from facepy import GraphAPI
def graph_client(token="CAACEdEose0cBAISItVLNm6ILR37s7ZBkbXDliKu2cQlDILQk1qZCQcZBF7dpE43IwWCMZAwZAuYEq8equ0WJ3hU3eK8wjgVEPiYHiFZC38rgGvzUhsxDkRSHgqZCbN0Q7J7ikP1NKG52ZCVoPq14xhZCUhO6czbn6OQJKujUZAAkb29xmUCZBZCZCZCDfAjdnYZCovjwodoiZCEdxVmdsnSnGAHIIZBrC"):
	return GraphAPI(token)

graph = graph_client()

end = False	

while end != True:
	print graph.oauth_token
	try:
		groups_ids  = ['324309874271040','206494919465453','255488514638473','334271300068285','263457997018425']
		#groups_ids  = ['324309874271040'] # Use this for testing

		pages_ids = ['202027666597795','293915470632663','476919592398799']
		#pages_ids = ['202027666597795']


		# entries 	= work_book.start_feeds_sheet()

		fds = open("data/feeds.csv",'wt')
		members = open("data/members.csv",'wt')

		entries = csv.writer(fds)
		worksheet = csv.writer(members)

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
		groups_feeds_data = feeds.get_all(graph, groups_ids)
		pages_feeds_data = feeds.get_all(graph, pages_ids)


		# members.extract(worksheet, groups_ids, pages_ids)

		pages.extract(graph, groups_feeds_data, entries) # This is just writing to excel with few calls to the API
		end = pages.extract(graph, pages_feeds_data, entries)

		# work_book.close()
	except Exception, e:
		print e 
		token = raw_input("\n\n Enter another token! ")
		graph = graph_client(token)
		
fds.close()
worksheet.close()
	