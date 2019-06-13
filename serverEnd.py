import socket
import select
import threading
import time
import rsa
import pickle
from stegano import lsb
import random




ss = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 
host=socket.gethostname()
port=9999
addr=(host,port)
ss.bind(addr)
ss.listen(5)
print('runing server')

fd_name={}
SL=[]
SL.append(ss)




while True:
    r,w,e=select.select(SL,[],[])
    for temp in r:
        if temp is ss:  #name
                connection,address = temp.accept()
                print('new connection address:',address)
                SL.append(connection)


                (p,te)=pickle.loads(connection.recv(1024))
                (bob_pub,bob_priv,info)=te
                #name=connection.recv(1024).decode('utf-8')
                #(bob_pub,bob_priv,info)=pickle.loads(connection.recv(1024))
                name= rsa.decrypt(info, bob_priv)


                fd_name[connection]=name.decode('utf8')
                print(name.decode('utf8'))
                #print(SL)
                ###
        else:
            disconnect=False
            try:
                #
                #thetime=time.asctime( time.localtime(time.time()) )
                #data=temp.recv(1024).decode('utf-8')
                data=temp.recv(100000000)

                
                #data=thetime+'\n'+fd_name[temp]+':'+data+'\n\n'
            except socket.error:
                    data=fd_name[temp]+' leave the room\n'
                    disconnect=True
#禁止离开
            if disconnect:#leave
                    SL.remove(temp)
                    print(data)
                    for other in SL:
                        if other!=ss and other!=temp:
                            try:
                                other.send(data.encode('utf-8'))
                            except Exception(e):
                                print(e)                    
                    del fd_name[temp]

            else:
                #print(data)
                
                (p,te)=pickle.loads(data)
                print(p)
                if p!=3 and p!=8:
                    for other in SL:
                        if other!=ss:
                            try:
                                other.send(data)
                                #other.send(data.encode('utf-8'))
                            except Exception(e):
                                print(e)    
                elif p==3:
                    ran=random.randrange(1,len(SL),1)
                    other=SL[ran]
                    try:
                        other.send(data)
                        #other.send(data.encode('utf-8'))
                    except Exception(e):
                        print(e)
                elif p==8:
                    ran=random.randrange(1,len(SL),1)
                    other=SL[ran]
                    try:
                        other.send(data)
                        #other.send(data.encode('utf-8'))
                    except Exception(e):
                        print(e)


                
