from classes.message import Message


class Network(object):
    """Network class for Paxos simulation."""

    def __init__(self):
        """Initialiser for Network class."""
        self.q = []

    def queue_message(self, m: Message) -> list:
        """Adds Message m to back of queue.

        :param m: Message
        :type m: Message
        """
        self.q.append(m)
        return self.q
    
    def is_empty(self) -> bool:
        """Checks if queue is empty.
        """
        return len(self.q) == 0

    def extract_message(self) -> Message:
        """Returns first item from queue where m.src.failed == False and m.dst.failed == False."""
        try:
            # Get first item in self.q where m.src.failed == False and m.dst.failed == False
            message = next(filter(lambda m: m.src.failed is False and m.dst.failed is False, self.q))
        except StopIteration:
            # No messages available where m.src.failed == False and m.dst.failed == False
            return None
        # Find index of message in self.q
        index = self.q.index(message)
        # Remove message from self.q and return
        return self.q.pop(index)
