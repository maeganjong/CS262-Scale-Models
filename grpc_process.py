from commands import *
import grpc
import model_pb2 as chat
import model_pb2_grpc
import logging
import argparse 
import random
import socket
import time
from datetime import datetime

class Model:   
    '''Instantiates the ChatClient and runs the user experience of cycling through chat functionalities.'''
    def __init__(self, process):
        self.process = process
        self.clock_speed = random.randint(1,6)
        print("Clockspeed ", self.clock_speed)
        logging.info(f"Clockspeed: {self.clock_speed}")

        self.clock = 0
        self.client1 = (process + 1) % 3
        self.client2 = (process + 2) % 3
        
        self.connection = None
        try:
            self.connection = model_pb2_grpc.ChatStub(grpc.insecure_channel(f"{SERVER}:{PORT}"))
        except Exception as e:
            logging.debug('Failed to connect to server')

        print("Connected to server. Starting simulation.")

    def run(self):
        while True:
            # Check if there's a message in the queue
            message = self.connection.client_receive_message(chat.Text(text=str(self.process)))
            
            # If there's no message in the queue
            if message.sender == NO_MESSAGE:
                self.clock += 1
                action = random.randint(1,10)

                # Send to client 1
                if action == 1:
                    output = self.connection.client_send_message(chat.Note(sender=self.process, recipient=self.client1, logical_clock_time=self.clock, length_queue=None))
                    print(output.text)
                    logging.info(f'Sent message to {self.client1} at {self.clock} logical time & at {datetime.now().time()}')
                # Send to client 2 
                elif action == 2:
                    output = self.connection.client_send_message(chat.Note(sender=self.process, recipient=self.client2, logical_clock_time=self.clock, length_queue=None))
                    print(output.text)
                    logging.info(f'Sent message to {self.client2} at {self.clock} logical time & at {datetime.now().time()}')
                # Send to client 1 & 2
                elif action == 3:
                    output1 = self.connection.client_send_message(chat.Note(sender=self.process, recipient=self.client1, logical_clock_time=self.clock, length_queue=None))
                    print(output1.text)
                    output2 = self.connection.client_send_message(chat.Note(sender=self.process, recipient=self.client2, logical_clock_time=self.clock, length_queue=None))
                    print(output2.text)

                    logging.info(f'Sent message to {self.client1} and {self.client2} at {self.clock} logical time & at {datetime.now().time()}')
                else:
                    logging.info(f'Internal event at {self.clock} logical time & at {datetime.now().time()}')
                
                
            # If there's a message in the queue
            else:
                self.clock = max(self.clock, message.logical_clock_time) + 1
                logging.info(f'Receive messsage from {message.sender} at {self.clock} logical time & at {datetime.now().time()}. Message queue length: {message.length_queue}')

            time.sleep(60/self.clock_speed)
def main():
    # Determines which process we're working with - provides identifier for logging & communication
    parser = argparse.ArgumentParser(
                    description = 'Specify the process number it should take')
    parser.add_argument('--p', type=int)
    args = parser.parse_args()

    # int 0, 1, 2
    process = args.p
    if process in [0, 1, 2]:
        # Establishes logging functionality
        logging.basicConfig(filename=f'{process}.log', encoding='utf-8', level=logging.DEBUG, filemode="w")
        
        model = Model(process)
        model.run()
    else:
        print("Must include a tag --p with the process number from 0 to 2")

main()