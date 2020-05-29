from message import Message


class Queue(object):
    """Queue class for Paxos simulation."""

    def __init__(self):
        """Initialiser for Queue class."""
        self.q = []

    def queue_message(self, m: Message):
        """[summary]

        :param m: [description]
        :type m: Message
        """
        pass

    def extract_message(self):
        """[summary]
        """
        pass
