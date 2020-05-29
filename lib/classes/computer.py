from message import Message


class Computer(object):
    """Computer class for Paxos simulation."""

    acs = []
    props = []

    def __init__(self, number, failed=False):
        """Initialiser for Computer class."""
        self.number = number
        self.failed = failed

    def deliver_message(self, m: Message):
        """[summary]

        :param m: [description]
        :type m: Message
        """
        pass


class Proposer(Computer):
    """Proposer class for Paxos simulation. Inherits Computer class."""

    def __init__(self, *args, **kwargs):
        """Initialiser for Proposer class."""
        super().__init__(*args, **kwargs)
        self.props.append(self)


class Acceptor(Computer):
    """Acceptor class for Paxos simulation. Inherits Computer class."""

    def __init__(self, *args, **kwargs):
        """Initialiser for Acceptor class."""
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    a = Acceptor(1)
    print(a.props)
    p = Proposer(1)
    print(p.props)
