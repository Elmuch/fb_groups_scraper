
# Members
# Get member data from groups and page
#!/usr/bin/env python

import client
import xlsxwriter
import pdb
import csv
import re
from urlparse import urlparse
from urlparse import parse_qs

def extract(worksheet, groups_ids, pages_ids=[]):
  print "--------importing members data-------------"
  graph = client.graph_client()

  members = {}
  members_names = {}
  dups    = []
  imports = []
  group_lens = []
  feeds = []

  def get_page_data(page_id): # This is going to happen from a different endpoint
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
      worksheet.writerow((feeder['from']['id'] ,feeder['from']['name'].encode('ascii', 'ignore'),
                          page_id, name['name'].encode('ascii', 'ignore')))
      get_distinct(feeder['from']['id'],feeder['from']['name'],page_id, name['name'])

  def get_all(group_id):
    print "Importing from group ID-: %s" %(group_id)
    data = graph.get(group_id + "/members?")
    group_name = graph.get(group_id+"/")['name']
    for member_data in data['data']:
      worksheet.writerow((member_data['id'], member_data['name'].encode('ascii', 'ignore'),group_id, group_name.encode('ascii', 'ignore')))
      get_distinct(member_data['id'],member_data['name'], group_id, group_name)

  def get_distinct(member_id, member_name, group_id, group_name):
    if member_id in members: # If the id exists in the previous iteration
      members[member_id].append(group_id) 
      members_names[member_name].append(group_name)
    else:
      members[member_id] = [group_id]
      members_names[member_name] = [group_name]

  for group_id in groups_ids:
    get_all(group_id)

  for page_id in pages_ids:
    get_page_data(page_id) # Getting data from the page is rather different from groups

  f = open('data/disctint_members.csv', 'wt')
  dup_members = csv.writer(f)
  count = 0
  dup_members.writerow(("MemberID", 
                        "GroupsIDs"))
  # I wish I had an enumerable here!!
  for member in members:
    dup_members.writerow((member.encode('ascii', 'ignore'),members[member]))
  # for (mbr_id,  group_id), (mbr_nm, grp_nm) in zip(members.items(),members_names.items()):
  #   dup_members.writerow((mbr_id,group_id,mbr_nm.encode('ascii', 'ignore'),grp_nm))

  f.close