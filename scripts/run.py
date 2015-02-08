#!/usr/bin/python

import csv
import client
import feeds
from csv_write import CSVWriter
from members import Member
from pages import Page

#groups_ids  = ['324309874271040','206494919465453','255488514638473','334271300068285','263457997018425']
groups_ids  = ['324309874271040'] # Use this for testing

#pages_ids = ['202027666597795','293915470632663','476919592398799']
pages_ids = ['202027666597795']

# Scrapper client 
graph = client.graph_client() 

feeds_headers = ("EntryID", "GroupID",
									"GroupName","MemberID","MemberName",
									"AssociatedID", "EntryType",
									"TimeStamp","ShareCount","LikeCount",
									"CommentsCount","MediaCaption",
									"MessageOrCommentContent",
									"Description","HyperLink","OriginalMemberID",
									"OriginalMembersName","OriginalMembersMessage")
members_headers = ("MemberID","MemberName",
										"GroupID","GroupName")
distinct_members_headers= ("MemberID", "GroupsIDs")

# init csv writer
csv_feeds_writer 	  = CSVWriter(feeds_headers,"feeds").writer()
csv_members_writer  = CSVWriter(members_headers,"members").writer()
csv_distinct_writer = CSVWriter(distinct_members_headers,"distinct_members").writer()

# Get all feeds, including paginations from fb
groups_feeds_data = feeds.get_all(groups_ids+pages_ids)

# Export all feeds to csv, or xls
for feed in groups_feeds_data:
	page = Page(graph,feed,csv_feeds_writer)
	# try:
	page.extract()
	# except Exception, e: # I am assumming the error here is token expiring
	# 	print e
 #  	token = raw_input("\nEnter New token ")
 #  	graph = client.graph(token)
 #  	continue

# Member data in groups and pages 
for c_id in pages_ids + groups_ids:
	member = Member(graph, csv_members_writer, c_id, c_id)
	member.extract()
	member.extract_distinct(csv_distinct_writer)

# Close the files 
csv_feeds_writer.close()
csv_members_writer.close()
csv_distinct_members_writer.close()