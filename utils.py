import threading
from commands import *

import grpc
import model_pb2 as chat
import model_pb2_grpc

from concurrent import futures

mutex_queue = threading.Lock()

class ChatServicer(model_pb2_grpc.ChatServicer):
    '''Initializes ChatServicer that sets up the datastructures to store user accounts and messages.'''
    def __init__(self):
        # List of Note message types
        self.message_queue = []

    '''Handles the clients receiving messages sent to them. Delivers the message to the clients then clears sent messages'''
    def client_receive_message(self, request, context):
        mutex_queue.acquire()
        print(self.message_queue)
        if (len(self.message_queue) == 0):
            mutex_queue.release()
            return chat.Note(sender=NO_MESSAGE, recipient=NO_MESSAGE, logical_clock_time=NO_MESSAGE, length_queue=NO_MESSAGE)
        else:
            message = self.message_queue.pop(0)
            message.length_queue = len(self.message_queue)
            mutex_queue.release()
            return message

    '''Handles the clients sending messages to other clients'''
    def client_send_message(self, request, context):
        mutex_queue.acquire()
        self.message_queue.append(request)
        mutex_queue.release()
        
        return chat.Text(text="Message sent!")
