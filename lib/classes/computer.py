from classes.network import Message, Network


class Computer(object):
    """Computer class for Paxos simulation."""

    acs = []
    props = []

    def __init__(self, number, network, failed=False):
        """Initialiser for Computer class."""
        self.number = number
        self.failed = failed
        self.network = network

    def deliver_message(self, m: Message):
        """Abstract method

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
    next_n = 1

    def __init__(self, *args, **kwargs):
        """Initialiser for Proposer class."""
        super().__init__(*args, **kwargs)
        self.props.append(self)
        self.value = None
        self.n = None
        self.accepted_count = 0
        self.rejected_count = 0

    def get_next_n(self):
        self.n = Proposer.next_n
        Proposer.next_n += 1
        return self.n

    def deliver_message(self, m: Message):
        """[summary]

        :param m: Message
        :type m: Message
        """
        if m.type == "PROPOSE":
            # The proposer gets a propose message
            self.value = m.value
            n = self.get_next_n()
            for accept_dest in self.acs:
                self.network.queue_message(Message(self, accept_dest, "PREPARE", n=n))

        elif m.type == "PROMISE":
            # The proposer gets a promise message
            # TODO check for prior
            self.network.queue_message(Message(self, m.src, "ACCEPT", m.n, value=self.value))
        elif m.type == "ACCEPTED":
            # The proposer gets an accepted message
            pass
        elif m.type == "REJECTED":
            self.rejected_count += 1
            if self.rejected_count > Proposer.acceptor_count // 2:
                n = self.get_next_n()
                for accept_dest in self.acs:
                    self.network.queue_message(Message(self, accept_dest, "PREPARE", n=n))
            # TODO reset accepted_count and rejected_count
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
        # TODO We should change this from a tuple to two seperate values
        self.prior = (0, None)

    def deliver_message(self, m: Message):
        """[summary]

        :param m: Message
        :type m: Message
        """
        if m.type == "PREPARE":
            # The acceptor gets a PREPARE message
            # If the n saved in prior is smaller than that of the message, send a PROMISE
            if self.prior[0] < m.n:
                if self.prior[1]:
                    self.network.queue_message(Message(src=self, dst=m.src, type_="PROMISE", n=m.n, prior=self.prior))
                else:
                    self.network.queue_message(Message(self, m.src, "PROMISE", m.n))
                
        elif m.type == "ACCEPT":
            # The acceptor gets an ACCEPT message
            # If the n saved in prior is smaller than that of the message, send a PROMISE
            if self.prior[0] < m.n:
                self.network.queue_message(Message(self, m.src, "ACCEPTED", m.n, value=m.value))
                # update prior value
                self.prior = (m.n, m.value)
            else:
                self.network.queue_message(Message(self, m.src, "REJECTED", m.n))

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
