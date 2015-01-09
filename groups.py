
# Groups
#
import pdb
import xlsxwriter
from facepy import GraphAPI
# It would be nice to get access_token dynamically"
access_token = "CAACEdEose0cBAOYGwZBENZA4mmccZCud6kOGzxkL9CZBTjyeKKZCZAaeypA1owU2gkCwKxJbxnHJrgDCmVImNtjduhBCdGheDZBD1BwNskZCUq2ZCl2ktHuhbaCw6dODxJhiaIP0uP3EtRTGEyMHIsmfZCrFyJzPdTbDy6knFB0ZAZAsGU0ufDX35wQrp0dwrdPW02LiZBklsr7kApyrU8crt1GTkoh2QHidmldEZD"
graph = GraphAPI(access_token)

groups  = ['324309874271040','206494919465453','255488514638473','334271300068285'] # This does not include pages, The api is handling this differently
members = {} # Holds all members across all the groups

# Just for counting but it would be better to use them for more stuff
dups    = []
imports = []
group_lens = []

workbook = xlsxwriter.Workbook('groups.xlsx')
worksheet = workbook.add_worksheet()
# output  = open("output.xls", "w")

def group_members_data(group_id):
  data = graph.get(group_id + "/members?")
  count = 0
  imports.append("")
  imports.append("")
  worksheet.write(len(imports), 0, "GroupID: %s" %(group_id))
  worksheet.write(len(imports), 1, "Number of members: %s" %(len(data['data'])))
  imports.append("")
  worksheet.write(len(imports), 0, "Name")
  worksheet.write(len(imports), 1, "ID")

  for member_data in data['data']:
    imports.append("")
    count += 1
    if member_data['id'] in members: # If the id exists in the previous iteration
      members[member_data['id']].append(group_id) # push to the list
      dups.append("")
      worksheet.write(len(imports), 0, member_data['name'])
      worksheet.write(len(imports), 1, member_data['id'])
    else:
      members[member_data['id']] = [group_id]
      worksheet.write(len(imports), 0, member_data['name'])
      worksheet.write(len(imports), 1, member_data['id'])

for group_id in groups:
  group_members_data(group_id)

# output.write("\nUsers in More than on group: \n")
dup_members = workbook.add_worksheet()
count = 0
dup_members.write(0, 0, "MemberID")
dup_members.write(0, 1, "GroupsIDs")
for member in members:
  if len(members[member]) > 1:
    count += 1
    dup_members.write(count, 0, member)
    dup_members.write(count, 1, str(members[member]))
    # output.write( "ID: %s     Groups: %s \n" %(member, members[member]))

# TODO move this to a printing util
worksheet.write(len(imports)+1, 0, len(group_lens))
# output.write("\nTotal imports: %s \n" %(len(imports)))
# output.write("Total distinct members: %s \n"  %(len(members)))
# output.write("Total number of members appearing in more than one group: %s \n" %(len(dups)))
workbook.close()

