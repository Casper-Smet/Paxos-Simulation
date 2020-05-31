from classes.computer import Acceptor, Computer, Proposer, Network, Message


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

        self.network = Network()

    def parse_events(self):
        """Returns generator object for Messages

        :yield: (ticks, Message, Failed computer, Recovered computer) describing event
        :rtype: (t, Message, F, R)
        """
        # FIXME, skips 11 for some reason
        current_t = self.E[0].split(" ")[0]
        # Computers that fail this tick
        F = []
        # Computer that recover this tick
        R = []
        # Message that is sent during this tick
        message = None
        for t, msg_type, target, value in map(lambda row: row.split(" "), self.E):
            if current_t != t:
                # Yield message for generator
                yield int(current_t), message, F, R
                current_t = t
                # Computers that fail this tick
                F = []
                # Computer that recover this tick
                R = []
                # Message that is sent during this tick
                message = None
            # If the msg_type is PROPOSE, simply make a message
            if msg_type == "PROPOSE":
                message = Message(
                    src="  ", dst=Proposer.props[int(target) - 1], type_="PROPOSE", value=value)

            # If the msg_type is FAIL or RECOVER, check target for Proposer or Acceptor
            elif msg_type in ["FAIL", "RECOVER"]:
                # If target is Proposer, grab the Proposer at index value-1
                if target == "PROPOSER":
                    c = Proposer.props[int(value) - 1]
                # If the target is Acceptor, grab the Acceptor at index value-1
                elif target == "ACCEPTOR":
                    c = Acceptor.acs[int(value) - 1]
                else:
                    print("Invalid target")
                    pass

                if msg_type == "FAIL":
                    F.append(c)
                elif msg_type == "RECOVER":
                    R.append(c)
            else:
                print("Invalid message type")
                pass
            
        yield int(current_t), message, F, R

    def run(self):
        """[summary]
        """
        events = self.parse_events()
        events_empty = False
        tick, m, F, R = next(events)

        
        print(list(self.parse_events()))
        for t in range(self.tmax):
            if events_empty and self.network.is_empty():
                # If events_empty is true, and the queue is empty, exit simulation
                # TODO add necessary prints here
                return

            if t != tick:
                m = self.network.extract_message()
                if m:
                    print(f"{t:03}: {m}")
                    Computer.deliver_message(m.dst, m)
                else:
                    # print(f"{t:03}:")
                    pass
            else:
                # Fail all computers that failed during this tick
                for c in F:
                    c.failed = True
                    print(f"{t:03}: ** {c} kapot **")
                # Repair all computers that recovered during this tick
                for c in R:
                    c.failed = False
                    print(f"{t:03}: ** {c} gerepareerd **")
                
                if m:
                    print(f"{t:03}: {m}")
                    Computer.deliver_message(m.dst, m)
                else:
                    m = self.network.extract_message()
                    if m:
                        print(f"{t:03}: {m}")
                        Computer.deliver_message(m.dst, m)

                try:
                    tick, m, F, R = next(events)
                except StopIteration:
                    # If the end of events is reached, set events_empty to True
                    events_empty = True


if __name__ == "__main__":
    input_ = ["0 PROPOSE 1 42",
              "8 FAIL PROPOSER 1",
              "11 PROPOSE 2 37",
              "26 RECOVER PROPOSER 1"]
    sim = Simulation(2, 3, 50, input_)
    sim.run()
