import logging
from process import Model
import argparse
from multiprocessing import Process
from commands import *
import threading
from commands import *
from new_process import Model

import grpc
import model_pb2 as chat
import model_pb2_grpc

from concurrent import futures

from utils import ChatServicer
from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random
import logging

def run_server(config):
    ip = SERVER
    port = config["port"]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_servicer = ChatServicer()
    model_pb2_grpc.add_ChatServicer_to_server(chat_servicer, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    # Sleep to make sure all processes are set up properly
    time.sleep(5)

    model = Model(config)
    start_new_thread(model.run, (model,))
    server.wait_for_termination()


if __name__ == '__main__':
    # Set up process configs
    ports = [2056, 3056, 4056]

    config1 = {"process_id": 0, "port": ports[0], "recipient1": ports[1], "recipient2": ports[2]}
    p1 = Process(target=run_server, args=(config1,))

    config2 = {"process_id": 1, "port": ports[1], "recipient1": ports[2], "recipient2": ports[0]}
    p2 = Process(target=run_server, args=(config2, ))

    config3= {"process_id": 2, "port": ports[2], "recipient1": ports[0], "recipient2": ports[1]}
    p3 = Process(target=run_server, args=(config3,))

    # Starts the processes
    p1.start()
    print("[STARTING] server 1 is starting...")

    p2.start()
    print("[STARTING] server 2 is starting...")

    p3.start()
    print("[STARTING] server 3 is starting...")
    
