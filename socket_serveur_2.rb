require 'socket'
require 'colorize'

# Port d'écoute pour le serveur
PORT = 3333

# Limite du nombre de clients
LIMITE = 10

# Array contenant les sockets des clients
CLIENTS = Array.new

# On crée un serveur de sockets TCP et on le fait écouter
serveur = TCPServer.new("127.0.0.1",PORT)
print "Le serveur TCPSocket écoute au port #{PORT} ... \n"

LIMITE.times do |chiffre|

  CLIENTS[chiffre] = Thread.new do
    
    Thread.current[:client_handle] = nil
    client = serveur.accept
    Thread.current[:client_handle] = client
    print "Client #{chiffre} a rejoint le serveur ! \n"
    
    while message = client.gets
      
      print "#{chiffre}> #{message} "

      if message.strip == "sortie"
        client.puts "fincommu"
        CLIENTS[chiffre] = nil
        Thread.current[:client_handle] = nil
        break
      end

      client.puts "recu!"

    end
    print "Client #{chiffre} a quitté le serveur ! \n"
  end

end

# Force tous les clients à quitter le serveur, provoquant l'arrêt de ce dernier.
def vider_serveur()
  CLIENTS.each_with_index do |thready| 
      thready[:client_handle].puts "fincommu" if thready[:client_handle] != nil
  end
end

# Fonction qui affiche toutes les commandes disponibles pour l'administrateur
def montrer_commande()
  print " kickall - Ejecte tous les clients du serveur sauf l'administrateur. \n"
  print " exit    - Ejecte tous les clients du serveur, y compris l'administrateur, et arrête le serveur. \n"
  print " help    - Affiche toutes les commandes et leurs descriptions. \n"
end

# Un autre thread qui surveille les actions de l'administrateur du serveur
ADMIN_THREAD = Thread.new do
  loop do
    print("ADMIN> ".light_red)
    commande = gets
    case commande.strip
    when "kickall"
      vider_serveur
    when "exit"
      arreter_serveur
    when "help"
      montrer_commande
    when ""
    else
      print("Commande inconnue.\n")
    end
  end
end

# Fonction pour quitter le serveur et arrèter le serveur
def arreter_serveur()
  print "Arret du serveur ! \n"
  #puts ADMIN_THREAD.class
  vider_serveur
  CLIENTS.each { |thready| thready.kill  }
  ADMIN_THREAD.kill
end

# On rejoint tous les threads qu'on a crée mdr...
CLIENTS.each { |thready| thready.join  }
ADMIN_THREAD.join

print "Fermeture du serveur... \n"
serveur.close


