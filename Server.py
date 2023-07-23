# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:00:14 2022

@author: Sherine
"""

import socket
import sys
import os
def strip_new_line_char(s):
    return s.strip('\n')
port=22222
s=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
s.bind((socket.gethostname(),22222))
s.listen(5)
print(f'[STARTING server via {port}]')
print("\nServer: ",s.getsockname())
try:
    conn ,addr=s.accept()
    print("Connected Successfully")
except:
    print("Unable to connect")
    sys.exit()
print(f'{conn} Connected')
connected_user=conn.recv(25).decode()
print('f{connected_user} is the connected user')
while True:
    user_choice=conn.recv(3).decode()
    if user_choice=='1':
        print(f'{connected_user} selected to encrypt a file')
    elif user_choice=='2':
        print(f'{connected_user} selected to decrypt a file')
    elif user_choice=='3':
        print(f'{connected_user} selected to transfer a file from server database')
        fc=conn.recv(50).decode()
        print(f'{connected_user} selected to download {fc}')
        filesize=os.path.getsize("./Server/"+fc)
        conn.send(str(filesize).encode())
        with open("./Server/"+fc,'rb') as fo:
            c=0
            while c<=filesize:
                data=fo.read(1024)
                if not data:
                    break
                conn.send(data)
                c+=len(data)
        msg=conn.recv(30).decode()
        print(msg)
    elif user_choice=='4':
        print(f'{connected_user} selected to transfer a file from client database')
        unf=conn.recv(25).decode()
        file_size=conn.recv(50).decode()
        print(f'{connected_user} is uploading {unf} file')
        with open('./Server/uploaded '+unf,'wb') as fo:
            c=0
            while c< int(file_size):
                data=conn.recv(1024)
                if not data:
                    break
                fo.write(data)
                c+=len(data)
        conn.send('File uploaded successfully'.encode())
    elif user_choice=='5':
        msg=conn.recv(30).decode()
        print(msg)
        break
s.close()