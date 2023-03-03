import threading
from commands import *

import grpc
import model_pb2 as chat
import model_pb2_grpc

from concurrent import futures

mutex_queue0 = threading.Lock()
mutex_queue1 = threading.Lock()
mutex_queue2 = threading.Lock()

class ChatServicer(model_pb2_grpc.ChatServicer):
    '''Initializes ChatServicer that sets up the datastructures to store message queues.'''
    def __init__(self):
        # List of Note message types
        self.message_queue_0 = [] 
        self.message_queue_1 = [] 
        self.message_queue_2 = [] 

    '''Handles the processes receiving messages sent to them. Delivers the message to the process then deletes it from the queue'''
    def client_receive_message(self, request, context):
        # Determines the process requesting to receive its messages
        recipient = int(request.text)

        # Handles each recipient's case, modifying respective data structures
        if recipient == 0:
            mutex_queue0.acquire()
            # If the queue is empty, notify process
            if (len(self.message_queue_0) == 0):
                mutex_queue0.release()
                return chat.Note(sender=NO_MESSAGE, recipient=NO_MESSAGE, logical_clock_time=NO_MESSAGE, length_queue=NO_MESSAGE)
            # If the queue has a message, dequeues and sends to process
            else:
                message = self.message_queue_0.pop(0)
                message.length_queue = len(self.message_queue_0)
                mutex_queue0.release()
                return message
        elif recipient == 1:
            mutex_queue1.acquire()
            # If the queue is empty, notify process
            if (len(self.message_queue_1) == 0):
                mutex_queue1.release()
                return chat.Note(sender=NO_MESSAGE, recipient=NO_MESSAGE, logical_clock_time=NO_MESSAGE, length_queue=NO_MESSAGE)
            # If the queue has a message, dequeues and sends to process
            else:
                message = self.message_queue_1.pop(0)
                message.length_queue = len(self.message_queue_1)
                mutex_queue1.release()
                return message
        elif recipient == 2:
            mutex_queue2.acquire()
            # If the queue is empty, notify process
            if (len(self.message_queue_2) == 0):
                mutex_queue2.release()
                return chat.Note(sender=NO_MESSAGE, recipient=NO_MESSAGE, logical_clock_time=NO_MESSAGE, length_queue=NO_MESSAGE)
            # If the queue has a message, dequeues and sends to process
            else:
                message = self.message_queue_2.pop(0)
                message.length_queue = len(self.message_queue_2)
                mutex_queue2.release()
                return message

    '''Handles the processes sending messages to other processes'''
    def client_send_message(self, request, context):
        recipient = request.recipient
        if recipient == 0:
            mutex_queue0.acquire()
            self.message_queue_0.append(request)
            mutex_queue0.release()
        elif recipient == 1:
            mutex_queue1.acquire()
            self.message_queue_1.append(request)
            mutex_queue1.release()
        elif recipient == 2:
            mutex_queue2.acquire()
            self.message_queue_2.append(request)
            mutex_queue2.release()
        
        return chat.Text(text="Message sent!")


"""Class for running server backend functionality."""
class ServerRunner:
    """Initialize a server instance."""
    def __init__(self, ip = "localhost"):
        self.ip = SERVER
        self.port = PORT

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.chat_servicer = ChatServicer()

    """Function for starting server."""
    def start(self):
        model_pb2_grpc.add_ChatServicer_to_server(self.chat_servicer, self.server)
        self.server.add_insecure_port(f"[::]:{self.port}")
        self.server.start()
        self.server.wait_for_termination()

    """Function for stopping server."""
    def stop(self):
        self.server.stop(grace=None)
        self.thread_pool.shutdown(wait=False)
