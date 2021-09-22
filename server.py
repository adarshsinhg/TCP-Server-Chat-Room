import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 80))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            # Broadcasting Messages
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('command was refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('UNBAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_unban = msg.decode('ascii')[6:]
                    unban_user(name_to_unban)
                    print(f'{name_to_unban} was unbanned!')
                else:
                    client.send('command was refused!'.encode('ascii'))       
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('Password'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != '1234':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('you were kicked by admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))
def unban_user (name):
     with open("bans.txt", "r+") as f:
       
      data = f.readlines()
      f.truncate(0)
      f.close()
      
# open file in write mode
     
     with open("bans.txt", "w") as f:
      
          for line in data :
          
        # condition for data to be deleted
           if line != name+'\n': 
            f.write(line)
     broadcast(f'{name} was unbanned by an admin!'.encode('ascii'))




    


print("server is listening...")
receive()
