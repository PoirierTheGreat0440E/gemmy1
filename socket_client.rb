require 'socket'

# L'adresse de destination
adresse = "127.0.0.1"
adresse = ARGV[0] if ARGV[0].class.name != "NilClass"

# Le port de destination 
port = 65000
port = ARGV[1] if ARGV[1].class.name != "NilClass"

print "Client se connecte à #{adresse}:#{port}"
client = TCPSocket.new adresse , port
message = String.new

loop do

  print message.dump , "\n"

  # On envoi un message
  print ">>>  "
  envoi = STDIN.gets 
  client.puts envoi

  message = client.gets.strip

  break if message == "fincommu"

end

print "Fermeture du client ! \n"
client.close

