
from groups import graph

def get_user_groups(user_id):
  data = graph.get(user_id + "/groups")
  # pdb.set_trace()
  user_groups = []

  for u_id in data['data']:
    user_groups.append(u_id['id'])

  return user_groups

print get_user_groups("me")
#   def distinct_members(members):
#   return  [x for x in members if members.count(x) == 1]

# def in_more_than_1_group(lis):
#   seen = set()
#   seen_add = seen.add
#   # adds all elements it doesn't know yet to seen and all other to seen_twice
#   seen_twice = set( x for x in lis if x in seen or seen_add(x) )
#   # turn the set into a list (as requested)
#   return list( seen_twice )