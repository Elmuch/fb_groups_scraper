#!/usr/bin/env python
# Members
# Get member data from groups and page
import csv
from urlparse import urlparse
import pdb
from urlparse import parse_qs

class Member(object):
  """Member Base class"""
  
  __distinct_members = {}

  def __init__(self, graph, csv_writer, group_id="", page_id=""):
    self.group_id   = group_id 
    self.page_id    = page_id
    self.csv_writer = csv_writer
    self.graph      = graph

  def get_page_data(self): 
    print "importing from page ID -", self.page_id
    name = self.graph.get(self.page_id)
    myuntil = ""
    nextuntil = ""
    same = False
    alldata = []
    pages_interactors = []

    while not same:
      myuntil = nextuntil
      data = self.graph.get(self.page_id + "/feed?limit=999999" + nextuntil)
      nextuntil = "&until=" + parse_qs(urlparse(data['paging']['next']).query)["until"][0]
      same = (myuntil == nextuntil)
      if not same:
        alldata += data['data']

    for feeder in alldata:
      if feeder['from']['id'] in pages_interactors: # Take care of duplicates
        continue

      pages_interactors.append(feeder['from']['id'])
      self.csv_writer.writerow((feeder['from']['id'] ,feeder['from']['name'].encode('ascii', 'ignore'),
                          self.page_id, name['name'].encode('ascii', 'ignore')))
      self.__get_distinct(feeder['from']['id'],self.page_id)

  def get_group_data(self):
    print "Importing from group ID- %s" %(self.group_id)
    data = self.graph.get(self.group_id + "/members?")
    group_name = self.graph.get(self.group_id)['name']
    for member_data in data['data']:
      self.csv_writer.writerow((member_data['id'], member_data['name'].encode('ascii', 'ignore'),self.group_id, group_name.encode('ascii', 'ignore')))
      self.__get_distinct(feeder['from']['id'],self.group_id)
  
  def __get_distinct(self, member_id, c_id): # c_id is the collection id, page of group id
    if member_id in self.__distinct_members : # If the id exists in the previous iteration
      self.__distinct_members [member_id].append(c_id)
    else:
      self.__distinct_members [member_id] = [c_id]

  def extract_distinct(self, csv_writer): # NOTE: csv_writer here is not bound to the current object
    for member in self.__distinct_members:
      csv_writer.writerow((member.encode('ascii', 'ignore'),self.__distinct_members[member]))
    
  def extract(self):
    if self.page_id != "": 
      self.get_page_data()
    else:
      self.get_group_data()