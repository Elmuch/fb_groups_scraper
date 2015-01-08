
# Groups
#
import pdb
from facepy import GraphAPI

# It would be nice to get access_token dynamically
access_token = "CAACEdEose0cBADuR2GZAN4DuzSd5yZAvnyM9BDGl0cRwW9G4NZBg6w3EC0uiFLbzFyrzSwRBHCnAntPWHPY72FFpZARKDh5nRBxvXrfRNRoBc7TanQATKG6Ts10uWCKLzZB3XnnAI4FiseZBhg6Xq3KnlPZB1CZADvVRRKctMkEbmgMCdbFWg3x50OzaeMSmUPLy8zJAk78G40zDoRV5eut0M0ImH9Ctgc4ZD"
graph = GraphAPI(access_token)

groups  = ['324309874271040','206494919465453','255488514638473','334271300068285'] # This does not include pages, The api is handling this differently
members = {} # Holds all members across all the groups

# Just for counting but it would be better to use them for more stuff
dups    = []
imports = []
output = open("output.xls", "w")

def group_members_data(group_id):
  data = graph.get(group_id+"/members?")
  count = 0

  output.write("\n ------------------------------------------------- \n")
  output.write("Group ID: %s Number of members: %s \n" %(group_id, len(data['data'])))

  for member_data in data['data']:
    imports.append("")
    count += 1

    if member_data['id'] in members:
        members[member_data['id']].append(group_id)
        dups.append("")
    else:
      members[member_data['id']] = [group_id]
      output.write(" %s Name: %s,      ID: %s \n" %( count, member_data['name'], member_data['id']))

for group_id in groups:
  group_members_data(group_id)

output.write("\nUsers in More than on group: \n")
for member in members:
  if len(members[member]) > 1:
   output.write( "ID: %s     Groups: %s \n" %(member, members[member]))

# TODO move this to a printing util
output.write("\nTotal imports: %s \n" %(len(imports)))
output.write("Total distinct members: %s \n"  %(len(members)))
output.write("Total number of members appearing in more than one group: %s \n" %(len(dups)))

output.close()

