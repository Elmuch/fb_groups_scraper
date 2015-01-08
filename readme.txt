Installing depencies:
  pip install facepy
  pip install facebook

Get your token here:
  https://developers.facebook.com/tools/explorer/

Accounts for testing:
  hotmail
  Joey Lamothe
  jlamlam@hotmail.com
  12JLam!@12345
  US
  10158
  Jan 1 1990
  jlamlam@openmailbox.org


Task 2015-01-07

> > Can you tell me *how many individuals in each group* and *how many total
> > distinct individuals across all groups* there are in each of the groups?
> > By individuals, I mean anybody who contributed, liked, posted or
> > interacted in any way or who became a member but never contributed.
> >
> > Please share the code, and let me know how many hours it takes. You can
> > also *use my FB identity*, see the attachment. You will have to *like
> > the MYESS page*, it's not a group.
> >
> > 1-Elangata Wuas Youth Association - public group - 324309874271040
> > 2-Kajiado County Congress (Lelero e Maa) - public group
> > 3-Torosei Elites Association - public group
> > 4-Loodokilani Ward Development Forum - public group
> > 5-Activistas Kajiado Chapter - public group
> > 6-Maasai Youth Empowerment Strategic Scheme (MYESS) - society/culture
> > website (page that you can like)


# Group logic
#
import pdb
from facepy import GraphAPI

access_token = "CAACEdEose0cBAEqQEZBYrqSJVNaanDIHotZB4cTNZBWwlQ23lMI7oUplHpGi47tLvKevy5MDz6b9wHFgRCxIQKf5ZCTvdvAZAwz5Un6YuZAf6sUXXRZAcVlBXIN3Q6NmYPZC4Inejm3K7qseQZBmdNN4rBZCULJXS4CUPI385PZA5NsDLyWkvk6DSiUadGhGCShb1Yr4i0X1ZBmBSlhpZC531sPg4M51WW9IISYMZD"
graph = GraphAPI(access_token)

groups = ['293915470632663','324309874271040','206494919465453','255488514638473','334271300068285']

def get_group_data(group_id):
  data = graph.get(group_id+"/members")

  print "Group ID: %s Number of members: %d" %(group_id, len(data['data']))
  # for member_data in data['data']:
  #   print("Name: %s, ID: %s" %(member_data['name'], member_data['id']))
  # # pdb.set_trace()

def get_distint_members():
  pass


  # driver

  # individuals per group
  # distinct groups
  # each individuals activities
# for group_id in groups:
get_group_data('293915470632663')
