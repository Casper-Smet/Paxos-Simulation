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
        self.q.append(m)
        return self.q

    def extract_message(self):
        """[summary]
        """
        return self.q.pop(0) if len(self.q) > 0 else None


if __name__ == "__main__":
    q = Queue()
    q.queue_message(Message(1, 2, "PROPOSE"))
    q.queue_message(Message(2, 1, "ACCEPTED"))
    print(q.extract_message())
