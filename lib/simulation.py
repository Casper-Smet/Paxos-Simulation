from classes.computer import Acceptor, Proposer, Network, Message

if __name__ == "__main__":
    q = Network()
    q.queue_message(Message(1, 2, "PROPOSE", 0))
    q.queue_message(Message(2, 1, "ACCEPTED", 0))
    print(q.extract_message())

    a = Acceptor(1)
    print(a.props, a.acs)
    p = Proposer(1)
    print(p.props, p.acs)
