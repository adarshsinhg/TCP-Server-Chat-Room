import socket
import threading

nickname = input("Choose your nickname: ")
if nickname == 'admin':
    password = input("Enter password fo admin: ")
# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 80))

stop_thread = False


def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_meassage = client.recv(1024).decode('ascii')
                if next_meassage == 'Password':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("connection was refused! wrong password!")
                        stop_thread = True
                elif next_meassage == 'BAN':
                    print('connection refused because of ban')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/ban'):
                    client.send(
                        f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/unban'):
                    client.send(
                        f'UNBAN {message[len(nickname)+2+7:]}'.encode('ascii'))

            else:
                print("commands can only be executed by the admin only")
        else:
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
