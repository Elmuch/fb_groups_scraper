require 'koala'
require 'byebug'

def export_comments
  @graph = Koala::Facebook::API.new("CAACEdEose0cBAIj1ehugwi7NwDb0sHYOKjjKwxbbZC8qyF7JfhAPlsGTaJdUmZBbRsGrlabhFFhS6oGglNTZBInSrdegyspsoCDhjLDwKmE3KGPYwNGV3YIopo15oGyAZCrv7TM6TVvvRyWfeHBpScQjMXJXYHfKYmfZB4EJJL7zOZBXKtTRV1z1IyWe3HeBVbYDmROV3HTiZBLQBW1vz8k7S1WFAZC1n68ZD")
  feed = @graph.get_connection("324309874271040","feed", :limit => 100000000)
  counter = 0
  f = File.open("r.txt","w")
  comments = []
  f << "-----------------------------------------------------------------------------------"
  feed.each do |comment|
      begin
        counter +=1
         f << comment["from"]["name"]+"|"+(comment["comments"]["data"][0]["message"])+"\n"
      rescue Exception => e
        counter -=1
        puts "there was problem exporting due to: \n#{e}"
      end
  end
  puts "Total exports: #{counter}"
end


# driver

export_comments