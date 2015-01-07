require 'koala'
require 'byebug'

def export_comments
  @graph = Koala::Facebook::API.new("CAACEdEose0cBAJJCsLLdZCxaxXqVCvuaLQxOVmTQ8DqfNzCeMGz2XE6JU6DvvIqFIZAo1C8NcALhyULxu43oUhkUU6Jbpe8bqJv0qIS1tH8LjXff9OzIfbjvWl2PXvXOoe3MZBy0WYpcI9ZAMcZAC1QFl2vLY760z9hXqpTmH0xgkn0laZBMa3ZBDurhldp3sDXnntvZBlckQSCViFzAnhqv")
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