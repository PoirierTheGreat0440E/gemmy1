require 'socket'
require 'colorize'

# Adresse d'écoute pour le serveur
$adresse = "127.0.0.1"
$adresse = ARGV[0] if ARGV[0].class.name != "NilClass"

# Port d'écoute pour le serveur
$port = 65000
$port = ARGV[1] if ARGV[1].class.name != "NilClass"

# Limite du nombre de clients
$limite = 10
$limite = ARGV[2] if ARGV[2].class.name != "NilClass"

# Array contenant les sockets des clients
CLIENTS_RECEPTION = Array.new
CLIENTS_ENVOI = Array.new

# On crée un serveur de sockets TCP et on le fait écouter
$serveur_reception = TCPServer.new($adresse,$port+1)
$serveur_envoi = TCPServer.new($adresse,$port)

print "Ouvert RECEPTION #{$adresse}:#{$port+1} ... \n"
print "Ouvert ENVOI #{$adresse}:#{$port} ... \n"
print "Nombre de clients : #{$limite} \n"


$limite.to_i.times do |chiffre|

  # ========================================================
  # On initialise les threads pour le serveur de réception...
  # ========================================================
  
  CLIENTS_RECEPTION[chiffre] =  Thread.new do
    
    Thread.current[:client_handle] = nil
    client = $serveur_reception.accept
    Thread.current[:client_handle] = client
    Thread.current[:index_envoi] = -1
    print "RECEPTION> Client #{chiffre} a rejoint le serveur ! \n".light_blue
    
    while message = client.gets

      match1 = /(id|mess):(\d)/.match(message)
      if match1.length > 0 
        if match1[1] == "id"
          Thread.current[:index_envoi] = match1[2].to_i
          CLIENTS_ENVOI[Thread.current[:index_envoi]][:index_reception] = chiffre
        end
      end

      print "RECEPTION #{chiffre}> #{message} \n".light_blue

    end
    print "RECEPTION> Client #{chiffre} a quitté le serveur ! \n".light_blue

  end

  # ========================================================
  # On initialise les threads pour le serveur d'envoi...
  # ========================================================
  
  CLIENTS_ENVOI[chiffre] =  Thread.new do
    
    Thread.current[:client_handle] = nil
    Thread.current[:index_reception] = -1

    client = $serveur_envoi.accept 
    Thread.current[:client_handle] = client
    print "ENVOI> Client #{chiffre} a rejoint le serveur ! \n".light_yellow

    # On envoie le numero du thread pour le renseigner au thread d'ecoute correspondant.
    Thread.current[:client_handle].puts chiffre

    while message = client.gets
            
      print "ENVOI #{chiffre}> #{message} ".light_yellow

      # Si le thread d'envoi est lié à un thread d'écoute...
      if Thread.current[:index_reception] != -1
        CLIENTS_RECEPTION[Thread.current[:index_reception]][:client_handle].puts "Depuis RECEPTION#{Thread.current[:index_reception]} : #{message}"
        if message.strip == "endfromclient"
          CLIENTS_RECEPTION[Thread.current[:index_reception]][:client_handle].puts "endcommunication"
          CLIENTS_RECEPTION[Thread.current[:index_reception]][:client_handle] = nil
          CLIENTS_RECEPTION[Thread.current[:index_reception]][:index_envoi] = -1
          CLIENTS_RECEPTION[Thread.current[:index_reception]].kill
          CLIENTS_ENVOI[chiffre][:index_reception] = -1
          CLIENTS_ENVOI[chiffre][:client_handle] = nil
          CLIENTS_ENVOI[chiffre].kill
        end
      end

    end

    print "ENVOI> Client #{chiffre} a quitté le serveur ! \n".light_yellow

  end
end

# Vide le serveur en éjectant tous les clients actifs...
def vider_serveur()
  
  CLIENTS_ENVOI.each_with_index do |thready,index|
    if thready[:client_handle] != nil and thready[:index_reception] != -1
      CLIENTS_RECEPTION[thready[:index_reception]][:client_handle].puts "endcommunication"
      CLIENTS_RECEPTION[thready[:index_reception]][:client_handle] = nil
      CLIENTS_RECEPTION[thready[:index_reception]][:index_envoi] = -1
      CLIENTS_RECEPTION[thready[:index_reception]].kill
      thready[:client_handle] = nil
      thready[:index_reception] = -1
      thready.kill
    else
      thready.kill
    end

  end

  CLIENTS_RECEPTION.each_with_index do |thready,index|
    thready.kill
  end

end



# Affiche tous les threads de clients du serveur
def montrer_threads()

  print "****** CLIENTS D'ENVOI ****** \n"
  CLIENTS_ENVOI.each_with_index do |thready,index|
    print("> #{index} : #{thready.status} / #{thready[:client_handle].to_s} / #{thready[:index_reception]} \n".light_yellow)
  end

  print "****** CLIENTS DE RECEPTION ****** \n"
  CLIENTS_RECEPTION.each_with_index do |thready,index|
    print("> #{index} : #{thready.status} / #{thready[:client_handle].to_s} / #{thready[:index_envoi]} \n".light_blue)
  end

end

# Fonction qui affiche toutes les commandes disponibles pour l'administrateur
def montrer_commande()
  print " kickall - Ejecte tous les clients du serveur sauf l'administrateur. \n"
  print " exit    - Ejecte tous les clients du serveur, y compris l'administrateur, et arrête le serveur. \n"
  print " help    - Affiche toutes les commandes et leurs descriptions. \n"
  print " clients - Affiche tous les threads de clients \n"
  print " refresh - Active tous les threads désactivés \n"
end

def arreter_serveur()
  print "Arret du serveur... \n"
  vider_serveur
  print "Serveur vidé."
  ADMIN_THREAD.kill
end

def rafraichir()

  $limite.to_i.times do |chiffre|
    
    if CLIENTS_RECEPTION[chiffre].status == false
      CLIENTS_RECEPTION[chiffre] =  Thread.new do
        Thread.current[:client_handle] = nil
        client = $serveur_reception.accept
        Thread.current[:client_handle] = client
        Thread.current[:index_envoi] = -1
        print "RECEPTION> Client #{chiffre} a rejoint le serveur ! \n".light_blue
        while message = client.gets
          match1 = /(id|mess):(\d)/.match(message)
          if match1.length > 0 
            if match1[1] == "id"
              Thread.current[:index_envoi] = match1[2].to_i
              CLIENTS_ENVOI[Thread.current[:index_envoi]][:index_reception] = chiffre
            end
          end
          print "RECEPTION #{chiffre}> #{message} \n".light_blue
        end
        print "RECEPTION> Client #{chiffre} a quitté le serveur ! \n".light_blue
      end
    end

    if CLIENTS_ENVOI[chiffre].status == false
      CLIENTS_ENVOI[chiffre] =  Thread.new do
        Thread.current[:client_handle] = nil
        Thread.current[:index_reception] = -1
        client = $serveur_envoi.accept 
        Thread.current[:client_handle] = client
        print "ENVOI> Client #{chiffre} a rejoint le serveur ! \n".light_yellow
        # On envoie le numero du thread pour le renseigner au thread d'ecoute correspondant.
        Thread.current[:client_handle].puts chiffre
        while message = client.gets
          print "ENVOI #{chiffre}> #{message} ".light_yellow
          # Si le thread d'envoi est lié à un thread d'écoute...
          if Thread.current[:index_reception] != -1
            CLIENTS_RECEPTION[Thread.current[:index_reception]][:client_handle].puts "Depuis RECEPTION#{Thread.current[:index_reception]} : #{message}"
            if message.strip == "endfromclient"
              CLIENTS_RECEPTION[Thread.current[:index_reception]][:client_handle].puts "endcommunication"
              CLIENTS_RECEPTION[Thread.current[:index_reception]][:client_handle] = nil
              CLIENTS_RECEPTION[Thread.current[:index_reception]][:index_envoi] = -1
              CLIENTS_RECEPTION[Thread.current[:index_reception]].kill
              CLIENTS_ENVOI[chiffre][:index_reception] = -1
              CLIENTS_ENVOI[chiffre][:client_handle] = nil
              CLIENTS_ENVOI[chiffre].kill
            end
          end
        end
        print "ENVOI> Client #{chiffre} a quitté le serveur ! \n".light_yellow
      end
    end

  #fin du times...
  end

end

# Un autre thread qui surveille les actions de l'administrateur du serveur
ADMIN_THREAD = Thread.new do
  loop do
    print("\nADMIN> ".light_red)
    commande = STDIN.gets
    case commande.strip
    when "help"
      montrer_commande
    when "clients"
      montrer_threads
    when "kickall"
      vider_serveur
    when "exit"
      arreter_serveur
    when "refresh"
      rafraichir
    else
      print("Commande inconnue.\n")
    end
  end
end

# On rejoint tous les threads qu'on a crée mdr...
CLIENTS_RECEPTION.each { |thready| thready.join  }
CLIENTS_ENVOI.each { |thready| thready.join }
ADMIN_THREAD.join

print "Fermeture des serveurs... \n"
$serveur_reception.close
$serveur_envoi.close


