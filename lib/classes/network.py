from classes.message import Message


class Network(object):
    """Network class for Paxos simulation."""

    def __init__(self):
        """Initialiser for Network class."""
        self.q = []

    def queue_message(self, m: Message):
        """Adds Message m to back of queue.

        :param m: Message
        :type m: Message
        """
        self.q.append(m)
        return self.q
    
    def is_empty(self):
        """Checks if queue is empty.
        """
        return len(self.q) == 0

    def extract_message(self):
        """Returns first item from queue."""
        return self.q.pop(0) if not self.is_empty() else None
