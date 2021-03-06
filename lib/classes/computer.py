from classes.network import Message, Network

from sklearn.tree import DecisionTreeRegressor
import pandas as pd


def load_data():
    """loads_data"""
    df = pd.read_pickle("test_input/train.pkl")
    df["yesterday"] = df["count"].shift(1, fill_value=0)
    df = df.drop(0)
    return df


def load_predictor(df=load_data()):
    """Loads predictor"""
    X_train = df.drop(["date", "count"], axis=1)
    y_train = df["count"]

    tree = DecisionTreeRegressor()
    tree.fit(X_train, y_train)

    def predict(day):
        row = X_train.iloc[[day]]
        return tree.predict(row)[0]

    return predict


class Computer(object):
    """Computer class for Paxos simulation."""

    acs = []
    props = []
    lears = []

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


class Client(Computer):
    """Client class for Paxos simulation. Represents outside world. Inherits Computer Class"""
    def __init__(self, *args, **kwargs):
        super().__init__(number=0, network=None, *args, **kwargs)
    
    def deliver_message(self, m: Message):
        """When a new value has been predicted reset all the acceptors for the next round.

        Args:
            m (Message): [description]
        """
        if m.type == "PREDICTED":
            self.reset_round()
    
    def reset_round(self):
        """Resets acceptors and learners for a new round."""
        for acceptor in self.acs:
            acceptor.prior = (0, None)

        for learners in self.lears:
            learners.has_predicted = False

    def __str__(self):
        """__str__ implementation for Proposer object.

        :return: Text representation of Proposer object
        :rtype: string
        """
        return "  "

    def __repr__(self):
        """__repr__ implementation for Proposer object.

        :return: Text representation of Proposer object
        :rtype: string
        """
        return "  "


class Proposer(Computer):
    """Proposer class for Paxos simulation. Inherits Computer class."""

    proposal_count = 1
    acceptor_count = 0
    learner_count = 0
    next_n = 1

    def __init__(self, *args, **kwargs):
        """Initialiser for Proposer class."""
        super().__init__(*args, **kwargs)
        self.props.append(self)
        self.proposed_value = None
        self.value = None
        self.n = None
        self.accepted_count = 0
        self.rejected_count = 0
        self.has_consensus = False

    def get_next_n(self):
        self.n = Proposer.next_n
        Proposer.next_n += 1
        return self.n

    def deliver_message(self, m: Message):
        """Takes a message and acts accordingly based on the type of the message.

        :param m: Message
        :type m: Message
        """
        if m.type == "PROPOSE":
            # The proposer gets a propose message
            self.value = m.value
            self.proposed_value = self.value
            n = self.get_next_n()
            for accept_dest in self.acs:
                self.network.queue_message(Message(self, accept_dest, "PREPARE", n=n))

        elif m.type == "PROMISE":
            # The proposer gets a promise message
            if m.prior:
                self.value = m.prior[1]
            self.network.queue_message(Message(self, m.src, "ACCEPT", m.n, value=self.value))
        elif m.type == "ACCEPTED" and not self.has_consensus:
            # Adds 1 to accepted_count
            self.accepted_count += 1
            # Checks if Proposer has reached consensus
            self.has_consensus = self.accepted_count > Proposer.acceptor_count // 2
            if self.has_consensus:
                # Send a SUCCES message to all learners
                for l in Computer.lears:
                    self.network.queue_message(Message(self, l, "SUCCES", m.n, m.value))
                self.accepted_count = 0
                self.has_consensus = False

        elif m.type == "REJECTED":
            # Adds 1 to rejected_count
            self.rejected_count += 1
            # Checks if Proposer has been rejected
            if self.rejected_count > Proposer.acceptor_count // 2:
                # If Proposer has been rejected, queue new PREPARE messages
                n = self.get_next_n()
                for accept_dest in self.acs:
                    self.network.queue_message(Message(self, accept_dest, "PREPARE", n=n))
                self.accepted_count = 0
                self.rejected_count = 0

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
        self.prior = (0, None)

    def deliver_message(self, m: Message):
        """Takes a message and acts accordingly based on the type of the message.

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
                # Send an ACCEPTED message to proposer
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


class Learner(Computer):
    """Learner class for Paxos simulation. Inherits Computer class."""

    def __init__(self, number, network, predict_function=load_predictor(), *args, **kwargs):
        """Initialiser for Learner class."""
        super().__init__(network=network, number=number, *args, **kwargs)
        self.lears.append(self)
        Proposer.learner_count += 1
        self.has_predicted = False
        self.learned_value = None
        self.predicted_value = None
        self.predict_function = predict_function

    def deliver_message(self, m: Message):
        """Takes a message and acts accordingly based on the type of the message.

        :param m: Message
        :type m: Message
        """
        if m.type == "SUCCES" and not self.has_predicted:
            # The learner gets a SUCCES message
            self.learned_value = m.value
            self.predicted_value = self.predict_function(self.learned_value)
            self.network.queue_message(Message(self, dst=Client(), type_="PREDICTED", value=self.predicted_value))
            self.has_predicted = True

    def __str__(self):
        """__repr__ implementation for Acceptor object.

        :return: Text representation of Acceptor object
        :rtype: string
        """
        return "L" + super().__str__()

    def __repr__(self):
        """__repr__ implementation for Acceptor object.

        :return: Text representation of Acceptor object
        :rtype: string
        """
        return "L" + super().__str__()
