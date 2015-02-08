#!/usr/bin/env python

import re
from urlparse import urlparse
from urlparse import parse_qs
import time
import xlsxwriter
import pdb
import json
import client

workbook = xlsxwriter.Workbook('data/data.xlsx')

def start_feeds_sheet():
	
	entries  = workbook.add_worksheet()

	entries.write(0, 0, "EntryID")
	entries.write(0, 1, "GroupID")
	entries.write(0, 2, "GroupName")
	entries.write(0, 3, "MemberID")
	entries.write(0, 4, "MemberName")
	entries.write(0, 5, "AssociatedID")
	entries.write(0, 6, "EntryType")
	entries.write(0, 9, "TimeStamp")
	entries.write(0, 10, "ShareCount")
	entries.write(0, 11, "LikeCount")
	entries.write(0, 12, "MessageOrCommentContent")
	entries.write(0, 13, "CommentsCount")
	entries.write(0, 14, "MediaCaption")
	entries.write(0, 15, "Description")
	entries.write(0, 16, "HyperLink")
	entries.write(0, 17, "OriginalMemberID")
	entries.write(0, 18, "OriginalMembersName")
	entries.write(0, 19, "OriginalMembersMessage")

	return entries

def start_members_sheet():
	worksheet = workbook.add_worksheet()
	worksheet.write(0, 0, "MemberID")
	worksheet.write(0, 1, "MemberName")
	worksheet.write(0, 2, "GroupID")
	worksheet.write(0, 3, "GroupName")

	return worksheet

def close():
	workbook.close()