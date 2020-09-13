# chat_client.py

import sys
import socket
import select
import urllib3

from getpass import _raw_input
from requests import get
from re import search
 
def chat_client():
    
    def GET_IP():
        try:
            try:
                r = get("https://es.geoipview.com/")
                data = r.text
                r.close()
                del (r)
                patron1 = r"([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})"
                x = search(patron1, data)
                if x:
                	ip = x[0]
                else:
                	ip = ""
                return ip
            except:
                print("Error de conexion")
                exit(0)
        except ValueError:
            return 1

    print("\033[3J\033[H\033[2J")
    if(len(sys.argv) < 2) :
        print ('Usage : python chat_client.py hostname port')
        sys.exit()

    host = get("https://raw.githubusercontent.com/desmonHak/client.py/master/host").text
    x = search(r"[0-9]*\.tcp\.ngrok\.io", host)
    if x:
        host = str(x.group())
    else:
        host = _raw_input("direcion tcp a conectarse: ")
    
    x = search("[0-9]*\n", get("https://raw.githubusercontent.com/desmonHak/client.py/master/host").text)
    if x:
        port = list(x.group())
        port.pop(len(port)-1)
        port = "".join(port)
        port = int(port)
        
    try:
        nick = str(sys.argv[len(sys.argv)-1])
    except IndexError:
        print("ingrese un nick por favor")
        exit(0)
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print ('No se puedo establecer conexion')
        sys.exit()
     
    print ('Conectado. Puedes empezar a enviar mensajes')
    print("\033]2;{}\007".format("Client: "+str(nick)))
     
    while True:
        socket_list = [sys.stdin, s]
         
        ready_to_read, ready_to_write, in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                data = sock.recv(4096).decode()
                
                if not data :
                    print('\nDesconectado desde el server')
                    sys.exit()
                else :
                    print (">> "+str(data))
            
            else :
                # user entered a message
                msg = _raw_input(">> ")
                if msg == "clear":
                    print("\033[3J\033[H\033[2J")
                elif msg[:4] == "exit":
                    s.close()
                    sys.exit(0)
                else:
                    mensaje = "({})[{}]>: ".format("90.130.89.173", nick) + str(msg)
                    s.send(mensaje.encode())
                 

if __name__ == "__main__":

    sys.exit(chat_client())
