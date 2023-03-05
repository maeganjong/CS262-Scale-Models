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
    def __init__(self, config, max_clock_speed = 6, max_internal_clock = 3, test=False):
        self.process = config["process_id"]
        # Set up logging
        logging.basicConfig(filename=f'{self.process}.log', encoding='utf-8', level=logging.DEBUG, filemode="w")

        self.max_internal_clock = max_internal_clock
        self.clock_speed = random.randint(1, max_clock_speed)
        print("Clockspeed ", self.clock_speed)
        logging.info(f"Clockspeed: {self.clock_speed}")

        self.clock = 0
        self.client1 = config["recipient1"]
        self.client2 = config["recipient2"]

        self.message_queue = []

        if test:
            #  Does not connect to server if test
            return
        
        self.connection = None
        try:
            port = config["port"]
            self.connection = model_pb2_grpc.ChatStub(grpc.insecure_channel(f"{SERVER}:{port}"))
        except Exception as e:
            logging.debug('Failed to connect to server')
        
        self.recipient1_connection = None
        try:
            port = config["recipient1"]
            self.recipient1_connection = model_pb2_grpc.ChatStub(grpc.insecure_channel(f"{SERVER}:{port}"))
        except Exception as e:
            logging.debug('Failed to connect to first recipient')
        
        self.recipient2_connection = None
        try:
            port = config["recipient2"]
            self.recipient2_connection = model_pb2_grpc.ChatStub(grpc.insecure_channel(f"{SERVER}:{port}"))
        except Exception as e:
            logging.debug('Failed to connect to second recipient')

        print("Connected to server. Starting simulation.")


    def run(self, test=False, seed=10):
        if test:
            # Seed randomness if it's a test
            random.seed(seed)
        
        while True:
            print("here!!")
            # Check if there's a message in the queue
            message = self.connection.client_receive_message(chat.Text(text=str(self.process)))
            
            # If there's no message in the queue
            if message.sender == NO_MESSAGE:
                self.clock += 1
                action = random.randint(1, self.max_internal_clock)

                # Send to client 1
                if action == 1:
                    output = self.recipient1_connection.client_send_message(chat.Note(sender=self.process, recipient=self.client1, logical_clock_time=self.clock, length_queue=None))
                    print(output.text)
                    logging.info(f'Sent message to {self.client1} at {self.clock} logical time & at {datetime.now().time()}')
                # Send to client 2 
                elif action == 2:
                    output = self.recipient2_connection.client_send_message(chat.Note(sender=self.process, recipient=self.client2, logical_clock_time=self.clock, length_queue=None))
                    print(output.text)
                    logging.info(f'Sent message to {self.client2} at {self.clock} logical time & at {datetime.now().time()}')
                # Send to client 1 & 2
                elif action == 3:
                    output1 = self.recipient1_connection.client_send_message(chat.Note(sender=self.process, recipient=self.client1, logical_clock_time=self.clock, length_queue=None))
                    print(output1.text)
                    output2 = self.recipient2_connection.client_send_message(chat.Note(sender=self.process, recipient=self.client2, logical_clock_time=self.clock, length_queue=None))
                    print(output2.text)

                    logging.info(f'Sent message to {self.client1} and {self.client2} at {self.clock} logical time & at {datetime.now().time()}')
                else:
                    logging.info(f'Internal event at {self.clock} logical time & at {datetime.now().time()}')
                
                
            # If there's a message in the queue
            else:
                self.clock = max(self.clock, message.logical_clock_time) + 1
                logging.info(f'Receive messsage from {message.sender} at {self.clock} logical time & at {datetime.now().time()}. Message queue length: {message.length_queue}')
            
            print('here??')
            if test:
                # Only run the loop once if it's a test
                return
            
            # time.sleep(60/self.clock_speed)

