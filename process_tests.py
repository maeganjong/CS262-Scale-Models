from process import Model
from commands import *
from unittest.mock import MagicMock
from unittest.mock import patch
import model_pb2 as chat

# pytest process_tests.py

def test_initialization():
    """Test that the process is initialized correctly."""
    model = Model(0, test=True)
    assert model.process == 0
    assert model.clock == 0

    assert model.clock_speed > 0 and model.clock_speed <= 6
    assert model.max_internal_clock > 0 and model.max_internal_clock <= 10

    assert model.client1 == 1
    assert model.client2 == 2


def test_receive_no_message_send_client1():
    """Test that the process behaves correctly if it receives no message and chooses to send to client1."""
    model = Model(0, test=True)
    model.connection = MagicMock()
    model.connection.client_receive_message.return_value = chat.Note(sender=NO_MESSAGE)
    model.connection.client_send_message.return_value = MagicMock(return_value=MagicMock(text="Message Sent"))

    # Seed 2 causes the action to be 1 (send to client 1)
    model.run(test=True, seed=2)

    assert model.clock == 1
    assert model.connection.client_receive_message.call_count == 1
    assert model.connection.client_send_message.call_count == 1

    model.connection.client_send_message.assert_any_call(chat.Note(sender=0, recipient=1, logical_clock_time=1, length_queue=None))


def test_receive_no_message_send_client2():
    """Test that the process behaves correctly if it receives no message and chooses to send to client2."""
    model = Model(0, test=True)
    model.connection = MagicMock()
    model.connection.client_receive_message.return_value = chat.Note(sender=NO_MESSAGE)
    model.connection.client_send_message.return_value = MagicMock(return_value=MagicMock(text="Message Sent"))

    # Seed 14 causes the action to be 2 (send to client 2)
    model.run(test=True, seed=14)

    assert model.clock == 1
    assert model.connection.client_receive_message.call_count == 1
    assert model.connection.client_send_message.call_count == 1

    model.connection.client_send_message.assert_any_call(chat.Note(sender=0, recipient=2, logical_clock_time=1, length_queue=None))


def test_receive_no_message_send_both_clients():
    """Test that the process behaves correctly if it receives no message and chooses to send to both clients."""
    model = Model(0, test=True)
    model.connection = MagicMock()
    model.connection.client_receive_message.return_value = chat.Note(sender=NO_MESSAGE)
    model.connection.client_send_message.return_value = MagicMock(return_value=MagicMock(text="Message Sent"))

    # Seed 1 causes the action to be 3 (send to client 1 & 2)
    model.run(test=True, seed=1)

    assert model.clock == 1
    assert model.connection.client_receive_message.call_count == 1
    assert model.connection.client_send_message.call_count == 2

    model.connection.client_send_message.assert_any_call(chat.Note(sender=0, recipient=1, logical_clock_time=1, length_queue=None))
    model.connection.client_send_message.assert_any_call(chat.Note(sender=0, recipient=2, logical_clock_time=1, length_queue=None))


def test_receive_no_message_internal():
    """Test that the process behaves correctly if it receives no message and does nothing."""
    model = Model(0, test=True)
    model.connection = MagicMock()
    model.connection.client_receive_message.return_value = chat.Note(sender=NO_MESSAGE)
    model.connection.client_send_message.return_value = MagicMock(return_value=MagicMock(text="Message Sent"))

    # Seed 4 causes the action to be doing nothing (internal)
    model.run(test=True, seed=4)

    assert model.clock == 1
    assert model.connection.client_receive_message.call_count == 1
    assert model.connection.client_send_message.call_count == 0


def test_receives_message():
    """Test that the process behaves correctly if it receives a message."""
    model = Model(0, test=True)
    model.connection = MagicMock()
    model.connection.client_receive_message.return_value = chat.Note(sender=1, recipient=0, logical_clock_time=6, length_queue=None)
    model.connection.client_send_message.return_value = MagicMock(return_value=MagicMock(text="Message Sent"))

    model.run(test=True)

    assert model.clock == 7
    assert model.connection.client_receive_message.call_count == 1
    assert model.connection.client_send_message.call_count == 0
