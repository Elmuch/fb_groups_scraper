
# Group logic
#
import pdb
from facepy import GraphAPI
import users

access_token = "CAACEdEose0cBALiisUv3ZAhgURRDF2qdVMRQ6tE4t6E8Gf27VbJZCpptiOqA34Vac8AjhnLbIs784m8TWQ0QPuDO5HI9hQQqHS6il9jGGSzASm7MTu3fXP3c7dytRPPlHV7ihnZCqf2wGd8gySwVcler55EE2zA5KQibQZA6Q4KBWqL2DppplsDzXH8x6PNuBmZAsI80lwAN3njtlYkOv82XIOOldQyIZD"
graph = GraphAPI(access_token)

groups  = ['324309874271040','206494919465453','255488514638473','334271300068285']
members = {}
dups = {}

def get_group_data(group_id):
  data = graph.get(group_id+"/members?")
  count = 0

  print "\n ------------------------------------------------- \n"
  print "Group ID: %s Number of members: %d \n" %(group_id, len(data['data']))

  for member_data in data['data']:
    x.append(member_data['id'])
    count += 1

    if member_data['id'] in members:
      if member_data['id'] in dups:
        print users.get_user_groups(member_data['id'])
      else:
        dups[member_data['id']] = group_id
        # print("DUP [ %s Name: %s,      ID: %s" %( count, member_data['name'], member_data['id']))
    else:
      members[member_data['id']] = group_id
      # print(" %s Name: %s,      ID: %s" %( count, member_data['name'], member_data['id']))

def distinct_members(members):
  return  [x for x in members if members.count(x) == 1]

def in_more_than_1_group(lis):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in lis if x in seen or seen_add(x) )
  # turn the set into a list (as requested)
  return list( seen_twice )

for group_id in groups:
  get_group_data(group_id)

print "\n Total imports: " + str(len(x))

print dups

# not_distinct = in_more_than_group(members)

# print (str(members) + "\n \n" + str(not_distinct))

# print unique(members)

