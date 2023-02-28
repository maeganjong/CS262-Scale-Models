import logging
import argparse 
import random
import socket
from commands import *
import time
# take from args of which process it is - to know its address?

class Model():
    def __init__(self, process):
        self.process = process
        self.clock_speed = random.randint(1,6)
        self.clock = 0

        self.addr_self = ADDR+process
        self.addr_one = ADDR+(process+1)%3
        self.addr_two = ADDR+(process+2)%3

        # ASSIGN ADDR1 for actual process 1

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr_self)

        ## Have this be behind a user input before running
        # Connect to the other two machines
        self.client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client1.connect(self.addr_one)

        self.client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client2.connect(self.addr_two)
    
    def run(self):
        while True:
            action = random.randint(1,6)
            if action == 1:
                # send to client1
                self.client1.send()

            elif action == 2:
                # send to client 2
                self.client2.send()

            elif action == 3:
                # send to client 1 and 2
                self.client1.send()
                self.client2.send()

            else: 

            self.server.receive()
            self.clock += 1
            time.sleep(60/self.clock_speed)
            logging.makeLogRecord(f'Sent messages at {self.clock} time at {time.now()}')


def main():
    # Determines which process we're working with - provides identifier for logging & communication
    parser = argparse.ArgumentParser(
                    description = 'Specify the process number it should take')
    parser.add_argument('--p', type=int)
    args = parser.parse_args()
    # int 1, 2, or 3
    process = args.p

    # Establishes logging functionality
    logging.basicConfig(filename=f'{process}.log', encoding='utf-8', level=logging.DEBUG)
    ## Use: logging.debug('This message should go to the log file')
    
    model = Model(process)
    model.run()

main()