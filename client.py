import socket
import threading
import maskpass
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

banner = """                     
               _____ _____ _____ _____           
              |     |  |  |  _  |_   _|          
              |   --|     |     | | |            
              |_____|__|__|__|__| |_|                                         
         _____ __    _____ _____ _____ _____ 
        |     |  |  |     |   __|   | |_   _|
        |   --|  |__|-- --|   __| | | | | |  
        |_____|_____|_____|_____|_|___| |_|  
              [+] Welcome clients [+]
"""

print(Fore.CYAN + banner)
print(Fore.LIGHTBLUE_EX + "\n------------------------ MENU ------------------------\n")
pseudonyme = input("Veuillez choisir votre Pseudonyme : ")

FORMAT = 'UTF-8'
host = '127.0.0.1'
port = 51891

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'NICK':
                client.send(pseudonyme.encode(FORMAT))
            elif message == 'MENU':
                menu = input("\nInscription ou Authentification (i/a): ")
                client.send(menu.encode(FORMAT))
            elif message == 'FNAME':
                fname = input("Entrez votre nom et prénom: ")
                client.send(fname.encode(FORMAT))
            elif message == 'INAME':
                name = input("\nChoisissez votre nom d'utilisateur: ")
                client.send(name.encode(FORMAT))
            elif message == 'IPSW':
                pwd = maskpass.askpass(prompt="\nChoisissez votre mot de passe:", mask="*")
                client.send(pwd.encode(FORMAT))
            elif message == 'LNAME':
                NAME = input("Entrez votre nom d'utilisateur: ")
                client.send(NAME.encode(FORMAT))
            elif message == 'LPSW':
                PWD = maskpass.askpass(prompt="\nEntrez votre mot de passe:", mask="*")
                client.send(PWD.encode(FORMAT))
            elif message == 'CHATI':
                print(Fore.BLUE + "\n      Votre inscription a été effectué avec succès!")
                print(Fore.LIGHTBLUE_EX + "\n------------------------ CHAT ------------------------\n")
                print(f"{Fore.BLUE}>>>> syntax d'un message privé : {Fore.RED}pseudonyme>message{Fore.BLUE} <<<<")
                print(Fore.BLUE + Style.DIM + "         les messages privés sont en bleu        \n")
                # start Thread for writing
                write_thread = threading.Thread(target=write,)
                write_thread.start()
            elif message == 'CHATL':
                print(Fore.BLUE + "\n--------------------- BIENVENUE! ---------------------")
                print(Fore.LIGHTBLUE_EX + "\n------------------------ CHAT ------------------------\n")
                print(f"{Fore.BLUE}>>>> syntax d'un message privé : {Fore.RED}pseudonyme>message{Fore.BLUE} <<<<")
                print(Fore.BLUE + Style.DIM + "         les messages privés sont en bleu        \n")
                # start Thread for writing
                write_thread = threading.Thread(target=write, )
                write_thread.start()
            else:
                print(message)
        except:
            print(Fore.RED + "Une erreur est survenue!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(pseudonyme, input(''))
        client.send(message.encode(FORMAT))


# Starting Threads For Listening
receive_thread = threading.Thread(target=receive)
receive_thread.start()

