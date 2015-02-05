
# Members
# Get member data from groups and page
#!/usr/bin/env python

import client
import xlsxwriter
import pdb
import re
from urlparse import urlparse
from urlparse import parse_qs

def extract(worksheet, groups_ids, pages_ids=[]):
  print "--------importing members data-------------"
  graph = client.graph_client()

  members = {} # Holds all members across all the groups

  dups    = []
  imports = []
  group_lens = []
  feeds = []


  def get_page_data(imports, page_id): # This is going to happen from a different endpoint
    print "importing from page ID -", page_id
    name = graph.get(page_id)
    myuntil = ""
    nextuntil = ""
    same = False
    alldata = []
    pages_interactors = []

    while not same:
      myuntil = nextuntil
      data = graph.get(page_id + "/feed?limit=999999" + nextuntil)
      nextuntil = "&until=" + parse_qs(urlparse(data['paging']['next']).query)["until"][0]
      same = (myuntil == nextuntil)
      if not same:
        alldata += data['data']

    for feeder in alldata:
      if feeder['from']['id'] in pages_interactors: # Take care of duplicates
        continue

      pages_interactors.append(feeder['from']['id'])
      imports.append("")
      worksheet.writerow((feeder['from']['id'] ,feeder['from']['name'],
                          page_id, name['name']))

  def get_group_name(group_id, imports):
      data = graph.get(group_id+"/")
      worksheet.write(len(imports), 3, data['name'])

  def get_all(group_id):
      print "importing: %s" %(group_id)
      data = graph.get(group_id + "/members?")
      for member_data in data['data']:
        imports.append("")
        worksheet.write(len(imports), 1, member_data['name'])
        worksheet.write(len(imports), 0, member_data['id'])
        worksheet.write(len(imports), 2, group_id)
        get_group_name(group_id, imports)
        get_distinct(member_data)


  def get_distinct(member_data):
    if member_data['id'] in members: # If the id exists in the previous iteration
        members[member_data['id']].append(group_id) # push to the list
    else:
      members[member_data['id']] = [group_id]

  for group_id in groups_ids:
    get_all(group_id)

  for page_id in pages_ids:
    get_page_data(imports, page_id) # Getting data from the page is rather different from groups

  # dup_members = workbook.add_worksheet()
  # count = 0
  # dup_members.write(0, 0, "MemberID")
  # dup_members.write(0, 1, "GroupsIDs")

  # for member in members:
  #   if len(members[member]) > 1:
  #     count += 1
  #     dup_members.write(count, 0, member)
  #     dup_members.write(count, 1, str(members[member]))