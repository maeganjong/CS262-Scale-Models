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

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)
        except:
            logging.debug('Failed to connect to server')
        
        print("Connected to server. Starting simulation.")

    
    '''Creates the message string per the designed wire protocol.'''
    def create_message(self, purpose, body, recipient=None, sender=None):
        data=PURPOSE + SEPARATOR + purpose
        if recipient and sender:
            data += SEPARATOR + RECIPIENT + SEPARATOR + recipient
            data += SEPARATOR + SENDER + SEPARATOR + sender
        if body:
            length = len(body)
            data += SEPARATOR + LENGTH + SEPARATOR + str(length)
            data += SEPARATOR + BODY + SEPARATOR + body
        
        return data

    '''Sends the message to the server per the designed wire protocol.'''
    def send(self, purpose, body, recipient=None, sender=None):
        msg = self.create_message(purpose, body, recipient, sender)
        try:
            encoded_message = msg.encode(FORMAT)
            if len(encoded_message) > MAX_BANDWIDTH:
                return False
            
            encoded_message = encoded_message.ljust(MAX_BANDWIDTH, b'0')
            self.client.send(encoded_message)
        except:
            raise ValueError
        
        return True

    
    def parse_message(self, full_message):
        split_message = full_message.split("/")
        parsed_message = {}
        i = 0
        while i < len(split_message):
            part = split_message[i]
            if BODY != part:
                parsed_message[part] = split_message[i+1]
                i += 1
            else:
                body = "/".join(split_message[i+1:])
                length = int(parsed_message[LENGTH])
                parsed_message[part] = body[:length]
                break
            i += 1
        
        return parsed_message
    

    def receive(self):
        try:
            full_message = self.client.recv(MAX_BANDWIDTH).decode(FORMAT)
            parsed_message = self.parse_message(full_message)

            return parsed_message
        
        except:
            return self.receive()


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
                pass
                
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
    # model.run()

main()