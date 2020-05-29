from classes.network import Message, Network


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

        :param m: Message
        :type m: Message
        """
        pass

    def __str__(self):
        """__repr__ implementation for Message object.

        :return: Text representation of Computer object
        :rtype: string
        """
        return f"{self.number}"

    def __repr__(self):
        """__repr__ implementation for Message object.

        :return: Text representation of Computer object
        :rtype: string
        """
        return f"{self.number}"


class Proposer(Computer):
    """Proposer class for Paxos simulation. Inherits Computer class."""

    proposal_count = 1
    acceptor_count = 0

    def __init__(self, *args, **kwargs):
        """Initialiser for Proposer class."""
        super().__init__(*args, **kwargs)
        self.props.append(self)

    def __str__(self):
        """__repr__ implementation for Proposer object.

        :return: Text representation of Proposer object
        :rtype: string
        """
        return "P" + super().__str__()

    def __repr__(self):
        """__repr__ implementation for Proposer object.

        :return: Text representation of Proposer object
        :rtype: string
        """
        return "P" + super().__str__()


class Acceptor(Computer):
    """Acceptor class for Paxos simulation. Inherits Computer class."""

    def __init__(self, *args, **kwargs):
        """Initialiser for Acceptor class."""
        super().__init__(*args, **kwargs)
        self.acs.append(self)
        Proposer.acceptor_count += 1

    def __str__(self):
        """__repr__ implementation for Acceptor object.

        :return: Text representation of Acceptor object
        :rtype: string
        """
        return "A" + super().__str__()

    def __repr__(self):
        """__repr__ implementation for Acceptor object.

        :return: Text representation of Acceptor object
        :rtype: string
        """
        return "A" + super().__str__()
