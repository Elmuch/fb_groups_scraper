
import pdb
from facepy import GraphAPI

access_token = "CAACEdEose0cBALiisUv3ZAhgURRDF2qdVMRQ6tE4t6E8Gf27VbJZCpptiOqA34Vac8AjhnLbIs784m8TWQ0QPuDO5HI9hQQqHS6il9jGGSzASm7MTu3fXP3c7dytRPPlHV7ihnZCqf2wGd8gySwVcler55EE2zA5KQibQZA6Q4KBWqL2DppplsDzXH8x6PNuBmZAsI80lwAN3njtlYkOv82XIOOldQyIZD"
graph = GraphAPI(access_token)

def get_user_groups(user_id):
  data = graph.get(user_id + "/groups?")
  user_groups = []

  for u_id in data['data']:
    user_group.append(u_id['id'])

  return user_groups