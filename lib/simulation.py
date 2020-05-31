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
        self.P = [Proposer(i + 1) for i in range(n_p)]
        self.A = [Acceptor(i + 1) for i in range(n_a)]
        self.tmax = tmax
        self.E = E

    def parse_events(self):
        """Returns generator object for Messages

        :yield: (ticks, Message, Failed computer, Recovered computer) describing event
        :rtype: (t, Message, F, R)
        """
        for t, msg_type, target, value in map(lambda row: row.split(" "), self.E):
            # Computers that fail this event
            F = None
            # Computer that recover this event
            R = None
            # If the msg_type is PROPOSE, simply make a message
            if msg_type == "PROPOSE":
                message = Message(
                    src="  ", dst=Proposer.props[int(target) - 1], type_="PROPOSE", value=value)

            # If the msg_type is FAIL or RECOVER, check target for Proposer or Acceptor
            elif msg_type in ["FAIL", "RECOVER"]:
                # If target is Proposer, grab the Proposer at index value-1
                if target == "PROPOSER":
                    F = Proposer.props[int(value) - 1]
                # If the target is Acceptor, grab the Acceptor at index value-1
                elif target == "ACCEPTOR":
                    R = Acceptor.acs[int(value) - 1]
                else:
                    print("Invalid target")
                    pass
            else:
                print("Invalid message type")
                pass
            # Yield message for generator
            yield int(t), message, F, R

    def run(self):
        """[summary]
        """
        events = self.parse_events()
        tick, m, F, R = next(events)

        for t in range(self.tmax):
            if t != tick:
                print(f"{t}:")
                pass
            # print(tick, m, F, R)
            print(f"{t}: {m}")
            try:
                event = next(events)
            except StopIteration:
                pass
             


if __name__ == "__main__":

    input_ = ["0 PROPOSE 1 42",
              "8 FAIL PROPOSER 1",
              "11 PROPOSE 2 37",
              "26 RECOVER PROPOSER 1"]
    sim = Simulation(2, 3, 50, input_)
    sim.run()
    # Acceptor(1)
    # Acceptor(2)
    # Acceptor(3)
    # # print(a.props, a.acs)
    # Proposer(1)
    # # print(p.props, p.acs)

    # q = Network()
    # # q.queue_message(Message(p, a, "PROPOSE", 0))
    # # q.queue_message(Message(a, p, "ACCEPTED", 0))
    # print(q.extract_message())
    # print(q)
