from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random
import logging
from commands import *
import grpc
import model_pb2 as chat
import model_pb2_grpc
import logging
import random
import time
from datetime import datetime

 
class Model:   
    '''Instantiates the ChatClient and runs the user experience of cycling through chat functionalities.'''
    def __init__(self, config, max_clock_speed = 6, max_internal_clock = 10, test=False):
        self.connection = None
        print("HERE?")
        try:
            self.connection = model_pb2_grpc.ChatStub(grpc.insecure_channel(f"{config[0]}:{config[1]}"))
        except Exception as e:
            logging.debug('Failed to connect to server')
        pass

    def init_machine(config):
        HOST = str(config[0])
        PORT = int(config[1])
        print("Starting Server on Port:", PORT)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            start_new_thread(receiver, (conn,))
    

    def machine(config):
        config.append(os.getpid())
        init_thread = Thread(target=init_machine, args=(config,))
        init_thread.start()

        # Add delay to initialize the server-side logic on all processes
        time.sleep(5)

        # Extensible to multiple senders
        #prod_thread = Thread(target=sender, args=(config[2],))
        #prod_thread.start()

        while True:
            pass


    # def receiver(conn):
    #     print("Receiver accepted connection: " + str(conn)+"\n")
    #     msg_queue = []

    #     sleepVal = 0.900
    #     while True:
    #         time.sleep(sleepVal)
    #         data = conn.recv(1024)
    #         print("msg received\n")
    #         dataVal = data.decode('ascii')
    #         print("msg received:", dataVal)
    #         msg_queue.append(dataVal)
    

    # def sender(portVal):
    #     host= "127.0.0.1"
    #     port = int(portVal)
    #     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    #     sleepVal = 0.500
    #     try:
    #         s.connect((host,port))
    #         print("Sender successfully connected to port " + str(portVal) + "\n")

    #         while True:
    #             codeVal = str(1)
    #             time.sleep(sleepVal)
    #             s.send(codeVal.encode('ascii'))
    #             print("msg sent", codeVal)
        
    #     except socket.error as e:
    #         print ("Error connecting sender: %s" % e)
 
 
if __name__ == '__main__':
    localHost= "127.0.0.1"

    port1 = 2056
    port2 = 3056
    port3 = 4056
    
    config1=[localHost, port1, port2,]
    client1 = Model(config1)
    p1 = Process(target=client1.run, args=(config1,))

    config2=[localHost, port2, port3]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1]
    p3 = Process(target=machine, args=(config3,))
 

    p1.start()
    p2.start()
    p3.start()
    

    p1.join()
    p2.join()
    p3.join()
