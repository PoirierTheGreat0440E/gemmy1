require 'socket'

client = TCPSocket.new "127.0.0.1", 3333
message = String.new

loop do

  print message.dump , "\n"

  # On envoi un message
  print ">>>  "
  envoi = gets 
  client.puts envoi

  message = client.gets.strip

  break if message == "fincommu"

end

print "Fermeture du client ! \n"
client.close

