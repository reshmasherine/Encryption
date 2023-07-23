# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:50:11 2022

@author: Sherine
"""

import os 
import socket
from Crypto import Random
from Crypto.Cipher import  AES
import sys
import getpass
class Encryptor:
    def __init__(self,key):
        self.key=key
    def pad(self,s):
        return s+ b"\0"* (AES.block_size-len(s)%AES.block_size)
    def encrypt(self,message,key,key_size=128):
        message=self.pad(message)
        iv=Random.new().read(AES.block_size)
        cipher=AES.new(key, AES.MODE_CBC,iv)
        return iv+cipher.encrypt(message)
    def encrypt_file(self,file_name):
        with open(file_name,'rb') as fo:
            plaintext=fo.read()
        enc=self.encrypt(plaintext,self.key)
        with open(file_name+".enc",'wb') as fo:
            fo.write(enc)
        os.remove(file_name)
        print(f'{file_name} is encrypted !')
    def decrypt(self,ciphertext,key):
        iv=ciphertext[:AES.block_size]
        cipher=AES.new(key,AES.MODE_CBC,iv)
        plaintext=cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")
    def decrypt_file(self,file_name):
        with open(file_name,'rb') as fo:
            ciphertext=fo.read()
        dec=self.decrypt(ciphertext, self.key)
        with open(file_name[:-4],'wb') as fo:
            fo.write(dec)
        os.remove(file_name)
        print(f'{file_name} is decrypted !')
key =b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc=Encryptor(key)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=22222
serv=input("Enter server IP address: ")
try:
    s.connect((serv,22222))
    print("Connected Successfully")
    print(f'Connected to {serv} via {port}')
except:
    print('Unable to connect')
    sys.excit()
def strip_new_line_char(s):
    return s.strip('\n')
#print(os.getcwd())
cond=True
while cond:
    ac_user=input("Do you have an account(Y/N)?\n")
    if ac_user=='Y' or ac_user=='y' or ac_user=='yes':
        with open('logindetails.txt','r') as file:
            dl=file.readlines()
            user_name=input('Enter your name: ')
            password=getpass.getpass('Enter your password: ')
            chk=user_name+' '+password
        if chk in map(strip_new_line_char,dl):
            print(f'Greetings {user_name}')
            cond=False
        else:
            print('Wrong credentials\n please try again')
    else:
        ch=int(input("Press 1 to become a new user\nPress 2 to exit\n"))
        if ch==2:
            cond=False
            sys.exit()
        else:
            un=input("Enter your name: ")
            pw=input("Enter your password: ")
            with open('logindetails.txt','a') as st:
                st.write('\n')
                st.write(un+' '+pw)
            print('You are a new user now !\n Please restart to use')
            cond=False
            sys.exit()
s.send(user_name.encode())
while True:
   with open('menu details.txt','r') as fo:
       for i in map(strip_new_line_char,fo.readlines()):
           print(i)
   choice=input("Please enter your choice:\n")
   s.send(choice.encode())
   if choice=='1':
       file_name=input("Enter file to be encrypted (along with format)\n")
       enc.encrypt_file(file_name)
       print('Your file has been encrypted and saved')
   elif choice=='2':
       file_name=input("Enter the file to be decrypted (along with format)\n")
       enc.decrypt_file(file_name)
       print("Your file has been decrypted and saved")
   elif choice=='3':
       l=os.listdir(path="E:\Semester 5\PP\Project AES and FT\Server")
       print("\nFiles present in Server directory:\n")
       for i in l:
           print(i)
       file_choice=input('Enter your file choice:\n')
       s.send(file_choice.encode())
       file_size=s.recv(50).decode()
       with open("./Client/downloaded "+file_choice,'wb') as fo:
           c=0
           while c< int(file_size):
               data=s.recv(1024)
               if not data:
                   break
               fo.write(data)
               c+=len(data)
       print('File downloaded successfully')
       s.send("File downloaded successfully".encode())
   elif choice=='4':
       l=os.listdir(path="E:\Semester 5\PP\Project AES and FT\Client")
       print("\nFiles present in Client directory:\n")
       for i in l:
           print(i)
       file_choice=input("\nEnter file to be uploaded\n")
       s.send(file_choice.encode())
       file_size=os.path.getsize("./Client/"+file_choice)
       s.send(str(file_size).encode())
       with open("./Client/"+file_choice,'rb') as uf:
           c=0
           while c< file_size:
               data=uf.read(1024)
               if not data:
                   break
               s.send(data)
               c+=len(data)
       msg=s.recv(50).decode()
       print(msg)
   elif choice=='5':
       msg='The client has exited!'
       s.send(msg.encode())
       print('\nThe client has exited')
       break
s.close()
      
        
        
        
    
         