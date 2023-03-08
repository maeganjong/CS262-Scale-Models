from server import ChatServicer
from commands import *

# pytest server_tests.py

from unittest.mock import MagicMock
from unittest.mock import patch
import model_pb2 as chat

def test_initialization():
    """Test that the server is initialized correctly."""
    server = ChatServicer()

    # Checks that all message queues are empty initially
    assert len(server.message_queue_0) == 0
    assert len(server.message_queue_1) == 0
    assert len(server.message_queue_2) == 0


def test_client_receive_message():
    """Test that the server behaves correctly when returning a message to a process."""
    context = MagicMock()
    request = MagicMock()
    request.text = "0"

    server = ChatServicer()

    # Checks that the server returns a NO_MESSAGE response when there are no messages in the queue
    response = server.client_receive_message(request, context)
    assert response.sender == NO_MESSAGE
    assert response.recipient == NO_MESSAGE
    assert response.logical_clock_time == NO_MESSAGE
    assert response.length_queue == NO_MESSAGE

    # Checks that the server returns the correct message when there is at least one message in the queue
    msg = chat.Note(sender=0, recipient=0, logical_clock_time=0, length_queue=None)
    server.message_queue_0.append(msg)
    response = server.client_receive_message(request, context)
    assert response == msg
    assert len(server.message_queue_0) == 0


def test_client_send_message():
    """Test that the server behaves correctly when sending a message to a process."""
    context = MagicMock()
    request = MagicMock()

    server = ChatServicer()

    # Checks that the server sends the message to recipient 0
    request.recipient = 0
    server.client_send_message(request, context)
    assert len(server.message_queue_0) == 1
    assert len(server.message_queue_1) == 0
    assert len(server.message_queue_2) == 0

    # Checks that the server sends the message to recipient 1
    request.recipient = 1
    server.client_send_message(request, context)
    assert len(server.message_queue_0) == 1
    assert len(server.message_queue_1) == 1
    assert len(server.message_queue_2) == 0

    # Checks that the server sends the message to recipient 2
    request.recipient = 2
    server.client_send_message(request, context)
    assert len(server.message_queue_0) == 1
    assert len(server.message_queue_1) == 1
    assert len(server.message_queue_2) == 1
