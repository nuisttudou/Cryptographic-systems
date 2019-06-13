import socket
import select
import threading
import time
import rsa
import pickle
from stegano import lsb
from LSBSteg import LSBSteg
import cv2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


global bob_pub
global bob_priv
global my_pub
global my_priv


(bob_pub, bob_priv) = rsa.newkeys(512)


(my_priv,my_pub)= rsa.newkeys(512)


def lis(s):
    my=[s]
    while True:
        r,w,e=select.select(my,[],[])
        if s in r:
            try:
                global bob_pub
                global bob_priv
                (p,te)=pickle.loads(s.recv(100000000))
                if p==1:
                    (bob_pub,bob_priv,info)=te
                    temp= rsa.decrypt(info, bob_priv)
                    print(temp.decode('utf8')+"\n\n")
                elif p==2:
                    # print(lsb.reveal("lena_hide.png")+"\n\n")
                    print(lsb.reveal(te)+"\n\n")
                elif p==3:
                    (bob_pub,bob_priv,info)=te
                    temp= rsa.decrypt(info, bob_priv)
                    print(temp.decode('utf8')+"\n\n")
                elif p==4:
                    
                    crypto = rsa.encrypt(te,bob_pub)
                    s.send(pickle.dumps((55,(bob_pub,bob_priv,crypto))))
                elif p==55:
                    (bob_pub,bob_priv,info)=te
                    temp= rsa.decrypt(info, bob_priv)
                    print(temp.decode('utf8')+"\n\n")
                elif p==5:
                    (my_priv,my_pub,info)=te
                    temp= rsa.decrypt(info,my_pub)
                    print(temp.decode('utf8')+"\n\n")
                elif p==6:
                    (bob_pub,bob_priv,cipher_data,encrypted_aes_key)=te
                    cipher = AES.new(rsa.decrypt(encrypted_aes_key, bob_priv), AES.MODE_ECB)
                    plain_data = unpad(cipher.decrypt(cipher_data), AES.block_size)
                    cv2.imwrite('receiced6.png', pickle.loads(plain_data))
                    print('Image received6. \n')
                elif p==7:
                    steg = LSBSteg(te)
                    orig_im = steg.decode_image()
                    cv2.imwrite("recovered7.png", orig_im)
                    print('Image received7. \n')
                elif p==8:
                    (bob_pub,bob_priv,cipher_data,encrypted_aes_key)=te
                    cipher = AES.new(rsa.decrypt(encrypted_aes_key, bob_priv), AES.MODE_ECB)
                    plain_data = unpad(cipher.decrypt(cipher_data), AES.block_size)
                    cv2.imwrite('receiced8.png', pickle.loads(plain_data))
                    print('Image received8. \n')
                elif p==9:
                    aes_key = rsa.randnum.read_random_bits(128)
                    cipher = AES.new(aes_key, AES.MODE_ECB)
                    cipher_data = cipher.encrypt(pad(pickle.dumps(cv2.imread(te.decode('utf8'))), AES.block_size))
                    encrypted_aes_key = rsa.encrypt(aes_key, bob_pub)
                    s.send(pickle.dumps((99,(bob_pub,bob_priv,cipher_data,encrypted_aes_key))))
                elif p==99:
                    (bob_pub,bob_priv,cipher_data,encrypted_aes_key)=te
                    cipher = AES.new(rsa.decrypt(encrypted_aes_key, bob_priv), AES.MODE_ECB)
                    plain_data = unpad(cipher.decrypt(cipher_data), AES.block_size)
                    cv2.imwrite('receiced99.png', pickle.loads(plain_data))
                    print('Image received99. \n')
                elif p==10:
                    (my_priv,my_pub,cipher_data,encrypted_aes_key)=te
                    cipher = AES.new(rsa.decrypt(encrypted_aes_key, my_pub), AES.MODE_ECB)
                    plain_data = unpad(cipher.decrypt(cipher_data), AES.block_size)
                    cv2.imwrite('receiced10.png', pickle.loads(plain_data))
                    print('Image received10 \n')
                        
            except socket.error:
                print('socket is error')
                exit()
            
def talk(s):
    while True:
        try:
            pan=int(input('1:rsa 2:LSB 3:不经意 4:零知识 5:签名 6:image rsa 7:image lsb'))
            
            info=input('>>>')##
        except Exception(e):
            print('can\'t input')
            exit()
        try:
            
            global bob_pub
            global bob_priv
            global my_pub
            global my_priv
            if pan==1:
                #global bob_pub
                #global bob_priv
                crypto = rsa.encrypt(info.encode('utf8'),bob_pub)
                #secret = lsb.hide("lena.png",crypto)
                #s.send(pickle.dumps((bob_pub,bob_priv,crypto)))
                s.send(pickle.dumps((1,(bob_pub,bob_priv,crypto))))
                #s.send(info.encode('utf-8'))
            elif pan==2:
                secret=lsb.hide("lena.png",info)
                # secret = lsb.hide("lena.png", info)
                # secret.save("lena_hide.png")
                # s.send(pickle.dumps((2,"")))
                s.send(pickle.dumps((2,secret)))
            elif pan==3:#不经意

                crypto = rsa.encrypt(info.encode('utf8'),bob_pub)
                s.send(pickle.dumps((3,(bob_pub,bob_priv,crypto))))
            elif pan==4:#零知识
                s.send(pickle.dumps((4,info.encode('utf8'))))    
            elif pan==5:#签名
                #global bob_pub
                #global bob_priv
                crypto = rsa.encrypt(info.encode('utf8'),my_priv)
                #secret = lsb.hide("lena.png",crypto)
                #s.send(pickle.dumps((bob_pub,bob_priv,crypto)))
                s.send(pickle.dumps((5,(my_priv,my_pub,crypto))))
                #s.send(info.encode('utf-8'))
            elif pan==6:
                aes_key = rsa.randnum.read_random_bits(128)
                cipher = AES.new(aes_key, AES.MODE_ECB)
                cipher_data = cipher.encrypt(pad(pickle.dumps(cv2.imread(info)), AES.block_size))
                encrypted_aes_key = rsa.encrypt(aes_key, bob_pub)
                s.send(pickle.dumps((6,(bob_pub,bob_priv,cipher_data,encrypted_aes_key))))
            elif pan==7:
                steg = LSBSteg(cv2.imread("carrier.png"))
                new_im = steg.encode_image(cv2.imread(info))
                s.send(pickle.dumps((7,new_im)))
            
            elif pan==8:#不经意
                aes_key = rsa.randnum.read_random_bits(128)
                cipher = AES.new(aes_key, AES.MODE_ECB)
                cipher_data = cipher.encrypt(pad(pickle.dumps(cv2.imread(info)), AES.block_size))
                encrypted_aes_key = rsa.encrypt(aes_key, bob_pub)
                s.send(pickle.dumps((8,(bob_pub,bob_priv,cipher_data,encrypted_aes_key))))

            elif pan==9:#零知识
                s.send(pickle.dumps((9,info.encode('utf8'))))
            elif pan==10:#签名
                aes_key = rsa.randnum.read_random_bits(128)
                cipher = AES.new(aes_key, AES.MODE_ECB)
                cipher_data = cipher.encrypt(pad(pickle.dumps(cv2.imread(info)), AES.block_size))
                encrypted_aes_key = rsa.encrypt(aes_key, my_priv)
                s.send(pickle.dumps((10,(my_priv,my_pub,cipher_data,encrypted_aes_key))))
        except Exception(e):
            print(e)
            exit()

            
ss=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=socket.gethostname()
addr=(host,9999)
try:
    ss.connect(addr)
    print('welcome.please enter your name.....')
except Exception(e):
            print('connection failed')
            exit()
t=threading.Thread(target=lis,args=(ss,))
t.start()
t1=threading.Thread(target=talk,args=(ss,))
t1.start()
    


