#!/usr/bin/python

import csv
from scripts import (client, feeds,csv_write,members, pages)

# Feel free to change these to your own groups

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
csv_feeds_writer 	  = csv_write.CSVWriter(feeds_headers,"feeds")
csv_members_writer  = csv_write.CSVWriter(members_headers,"members")
csv_distinct_writer = csv_write.CSVWriter(distinct_members_headers,"distinct_members")

# Get all feeds, including paginations from fb
groups_feeds_data = feeds.get_all(groups_ids+pages_ids)

# Export all feeds to csv, or xls
for feed in groups_feeds_data:
	page = pages.Page(graph,feed,csv_feeds_writer.writer())
	page.extract()

# Member data in groups and pages 
for c_id in pages_ids + groups_ids:
	member = Member(graph, csv_members_writer.writer(), c_id, c_id)
	member.extract()
	member.extract_distinct(csv_distinct_writer.writer())

# Close the files 
csv_feeds_writer.close()
csv_members_writer.close()
csv_distinct_writer.close()