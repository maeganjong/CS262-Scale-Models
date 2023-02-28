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

        # Connect to the other two machines
        self.client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client1.connect(ADDR1)

        self.client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client2.connect(ADDR2)
    
    def run(self):
        while True:
            action = random.randint(1,6)
            if action == 1:
                # send to client1

            elif action == 2:
                # send to client 2

            elif action == 3:
                # send to client 1 and 2

            else: 

            self.clock += 1
            logging.makeLogRecord(f'Sent messages at {self.clock} time at {time.now()}')


def main():
    # Determines which process we're working with - provides identifier for logging & communication
    parser = argparse.ArgumentParser(
                    description = 'Specify the process number it should take')
    parser.add_argument('--p', type=int)
    args = parser.parse_args()
    process = args.p

    # Establishes logging functionality
    logging.basicConfig(filename=f'{process}.log', encoding='utf-8', level=logging.DEBUG)
    ## Use: logging.debug('This message should go to the log file')
    
    model = Model()
    model.run()

main()