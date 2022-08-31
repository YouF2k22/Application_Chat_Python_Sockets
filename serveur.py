import socket
import xml.etree.ElementTree as xml
import threading
import colorama
from colorama import Fore
colorama.init(autoreset=True)

banner = """                  
       _____ _____ _____ _____           
      |     |  |  |  _  |_   _|          
      |   --|     |     | | |            
      |_____|__|__|__|__| |_|                      
 _____ _____ _____ _____ _____ _____ 
|   __|   __| __  |  |  |   __| __  |
|__   |   __|    -|  |  |   __|    -|
|_____|_____|__|__|\___/|_____|__|__|
[+] Welcome to our simple chat application [+]
"""

tree = xml.parse("info.XML")
r = tree.getroot()

host = '127.0.0.1'
port = 51891
FORMAT = 'UTF-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(Fore.CYAN + banner)

clients = []
pseudonymes = []
dict = {}


def seperate(list):
    vers = []
    msg = []
    de = []
    indice = 0
    for i in list:
        if i == " ":
            indice = list.index(i)
            de = list[:indice - 1]
            list = list[indice + 1:]
            for i in list:
                if i != ">":
                    vers.append(i)
                else:
                    indice = list.index(i)
                    msg = list[indice + 1:]
                    break
            return de, convert(vers), msg


def convert(list):
    new = ""
    for x in list:
        new += x
    return new


def showmsg(list):
    msg = []
    de = []
    indice = 0
    for i in list:
        if i == ":":
            indice = list.index(i)
            de = list[:indice]
            msg = list[indice + 1:]
            return de, msg
        elif i == " ":
            indice = list.index(i)
            de = list[:indice]
            msg = list[indice + 1:]
            return de, msg


def broadcast(message):
    for i in message:
        if message.count(">".encode(FORMAT)) > 0:
            (x, y, z) = seperate(message.decode(FORMAT))
            if y in dict:
                dict[y].send("{}: {}".format(Fore.BLUE + x, z).encode(FORMAT))
                dict[x].send("{}: {}".format(Fore.BLUE + x, z).encode(FORMAT))
                # print(f"{Fore.BLUE}{x} a envoyé '{z}' en privé à {y}")
                break
            else:
                dict[x].send(f"{Fore.RED}'{y}' ne correspond à aucun client connecté! veuillez vérifier la liste et réessayer".encode(FORMAT))
                break
        else:
            (x, y) = showmsg(message.decode(FORMAT))
            # print(f"{x} a diffusé '{y}'")
            for client in clients:
                client.send(message)
            break


# Handling Messages From Clients
def handle(client, address):
    while True:
        index = clients.index(client)
        nickname = pseudonymes[index]
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            clients.remove(client)
            client.close()
            broadcast('{} left!'.format(Fore.RED + nickname).encode(FORMAT))
            print(Fore.RED + "Connexion avec {} s'est terminée.".format(str(address)))
            pseudonymes.remove(nickname)
            del dict[nickname]
            break


# registration function
def registration(name, paswd, fname, client):
    c = xml.Element("user")
    r.append(c)
    fullname = xml.SubElement(c, "fullname")
    fullname.text = fname
    nic = xml.SubElement(c, "nickname")
    nic.text = name
    pswd = xml.SubElement(c, "passwd")
    pswd.text = paswd
    tree = xml.ElementTree(r)
    with open("info.xml", "wb") as f:
        tree.write(f)
    client.send('CHATI'.encode(FORMAT))

# login function
def login(NAME, PSW):
    for u in r.findall('user'):
        np = u.find('nickname').text
        pp = u.find('passwd').text
        if np == NAME and pp == PSW:
            return True
    return False


# Receiving / Listening Function
def receive():
    while True:
        client, address = server.accept()
        # print(Fore.GREEN + "Connected with {}".format(str(address)))

        client.send('NICK'.encode(FORMAT))
        pseudonyme = client.recv(1024).decode(FORMAT)
        while True:
            client.send('MENU'.encode(FORMAT))
            menu = client.recv(1024).decode(FORMAT)
            if menu in ('i', 'I'):
                client.send(f"\n{Fore.BLUE}                  [+] INSCRIPTION [+]\n".encode(FORMAT))
                client.send('FNAME'.encode(FORMAT))
                fname = client.recv(1024).decode(FORMAT)
                client.send('INAME'.encode(FORMAT))
                name = client.recv(1024).decode(FORMAT)
                client.send('IPSW'.encode(FORMAT))
                psw = client.recv(1024).decode(FORMAT)
                registration(name, psw, fname, client)
                print(Fore.GREEN + "Connexion établie avec {}".format(str(address)))
                pseudonymes.append(pseudonyme)
                clients.append(client)
                dict[pseudonyme] = client
                print("Pseudonyme est {}".format(pseudonyme))
                broadcast(f"{Fore.GREEN}{pseudonyme} a rejoint!".encode(FORMAT))
                index = pseudonymes.index(pseudonyme)
                if len(pseudonymes) < 2:
                    client.send(f"\n{Fore.GREEN}Vous etes le premier a rejoindre cette session!".encode(FORMAT))
                    break
                else:
                    client.send(f"\nClients connectés : {' '.join(pseudonymes[:index])}".encode(FORMAT))
                break
            elif menu in ('a', 'A'):
                client.send(f"\n{Fore.BLUE}                [+] AUTHENTIFICATION [+]\n".encode(FORMAT))
                client.send('LNAME'.encode(FORMAT))
                name = client.recv(1024).decode(FORMAT)
                client.send('LPSW'.encode(FORMAT))
                psw = client.recv(1024).decode(FORMAT)
                login(name, psw)
                if login(name, psw):
                    client.send('CHATL'.encode(FORMAT))
                    print(Fore.GREEN + "Connexion établie avec {}".format(str(address)))
                    pseudonymes.append(pseudonyme)
                    clients.append(client)
                    dict[pseudonyme] = client
                    print("Pseudonyme est  {}".format(pseudonyme))
                    broadcast(f"{Fore.GREEN}{pseudonyme} a rejoint!".encode(FORMAT))
                    index = pseudonymes.index(pseudonyme)
                    if len(pseudonymes) < 2:
                        client.send(f"\n{Fore.GREEN}Vous etes le premier a rejoindre cette session!".encode(FORMAT))
                        break
                    else:
                        client.send(f"\nClients connectés : {' '.join(pseudonymes[:index])}".encode(FORMAT))
                    break
                else:
                    client.send(f"\n{Fore.RED}Vos informations sont incorrectes, veuillez réessayer!".encode(FORMAT))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client, address,))
        thread.start()


receive()
