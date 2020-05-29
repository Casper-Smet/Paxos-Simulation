from classes.computer import Acceptor, Proposer, Network, Message

class Simulation:

    def __init__(self, n_p, n_a, tmax, E):
        """[summary]

        Arguments:
            n_p {[type]} -- [description]
            n_a {[type]} -- [description]
            tmax {[type]} -- [description]
            E {[type]} -- [description]
        """
        self.P = None
        self.A = None
        self.tmax = tmax
        self.E = E
    
    def run(self):
        """[summary]
        """

        for t in self.tmax:
            pass


if __name__ == "__main__":
    a = Acceptor(1)
    print(a.props, a.acs)
    p = Proposer(1)
    print(p.props, p.acs)

    q = Network()
    q.queue_message(Message(p, a, "PROPOSE", 0))
    q.queue_message(Message(a, p, "ACCEPTED", 0))
    print(q.extract_message())

