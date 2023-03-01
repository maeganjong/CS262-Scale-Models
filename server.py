import socket 
import threading
import re
from commands import *

mutex_queue1 = threading.Lock()
mutex_queue2 = threading.Lock()
mutex_queue3 = threading.Lock()

class ChatServer:
    def __init__(self, test=False):
        if not test:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(ADDR)

        self.message_queue_1 = {} # {timestamp: message}
        self.message_queue_2 = {} # {timestamp: message}
        self.message_queue_3 = {} # {timestamp: message}

        self.client_addr_1 = None
        self.client_addr_2 = None
        self.client_addr_3 = None


    '''Handles the clients sending messages to other clients. Assumes recipient is already registered.'''
    def record_chat_message(self, conn, sender, recipient, msg):
        # mutex_unsent_messages.acquire()
        # self.unsent_messages[recipient].append((sender, msg))
        # mutex_unsent_messages.release()
        # self.send(conn, NOTIFY, "Message sent!")
        pass # TODO
    

    '''Handles the clients receiving messages sent to them. Delivers the message to the clients then clears sent messages'''
    def send_unsent_messages(self, conn, addr):
        # for recipient in self.unsent_messages:
        #     messages = self.unsent_messages[recipient]

        #     if recipient in self.active_accounts:
        #         recipient_addr = self.active_accounts[recipient]
        #         if recipient_addr == addr:
        #             print("waiting for mutex")
        #             mutex_unsent_messages.acquire()
        #             print("got mutex")
        #             for message in messages:
        #                 text = message[0] + " sends: " + message[1]
        #                 self.send(conn, NOTIFY, text)
        #             self.unsent_messages[recipient] = []
        #             print("mutex released")
        #             mutex_unsent_messages.release()

        #             # Assumes user is only logged into one terminal
        #             self.send(conn, NO_MORE_DATA, " ")
        pass # TODO
    

    '''Creates the message to be parsed according to the designed wire protocol'''
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
    
    '''Sends the message to the client.'''
    def send(self, conn, purpose, body, recipient=None, sender=None):
        msg = self.create_message(purpose, body, recipient, sender)
        try:
            encoded_message = msg.encode(FORMAT)
            if len(encoded_message) > MAX_BANDWIDTH:
                return False
            
            encoded_message = encoded_message.ljust(MAX_BANDWIDTH, b'0')
            conn.send(encoded_message)
        except:
            raise ValueError
        
        return True

    '''Receives and parses the message from clients per the designed wire protocol.'''
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
        print(parsed_message)
        return parsed_message
    

    '''Return a dictionary representation of the message'''
    def receive(self, conn):
        try:
            full_message = conn.recv(MAX_BANDWIDTH).decode(FORMAT)
            return self.parse_message(full_message)
        except:
            return self.receive(conn)
    

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
    

    # Only handles 3 clients
    # TODO: can we assume that it just handles this many?
    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while threading.active_count() < 4:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
            if self.client_addr_1 == None:
                self.client_addr_1 = addr
            elif self.client_addr_2 == None:
                self.client_addr_2 = addr
            else:
                self.client_addr_3 = addr


chat_server = ChatServer()
print("[STARTING] server is starting...")
chat_server.start()