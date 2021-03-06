from collections import defaultdict
from classes.computer import Acceptor, Client, Computer, Proposer, Learner, Network, Message


def from_text(fp: str):
    """Function for processing .txt files with Paxos instructions

    :param fp: Filepath
    :type fp: str
    :return: n_p, n_a, n_l, tmax, E
    :rtype: (int, int, int, int, list)
    """
    with open(fp, "r") as file:
        lines = [line.strip() for line in file if not line.startswith("#")]

    last_line = lines.pop()
    assert last_line == "0 END", f"ERROR: test file {fp} should end with '0 END'"

    n_p, n_a, n_l, tmax = lines.pop(0).split(" ")

    return int(n_p), int(n_a), int(n_l), int(tmax), lines


class Simulation:

    def __init__(self, n_p: int, n_a: int, n_l: int, tmax: int, E: list):
        """[summary]

        Arguments:
            n_p {[type]} -- [description]
            n_a {[type]} -- [description]
            n_l {[type]} -- [description]
            tmax {[type]} -- [description]
            E {[type]} -- [description]
        """
        self.network = Network()

        # Make n_p Proposers
        self.P = [Proposer(i + 1, self.network) for i in range(n_p)]
        # Make n_a Acceptors
        self.A = [Acceptor(i + 1, self.network) for i in range(n_a)]
        # Make n_a Acceptors
        self.L = [Learner(i + 1, self.network) for i in range(n_l)]
        # Simulation time limit
        self.tmax = tmax
        # IO stream or list of strings with events
        self.E = E

    def parse_events(self):
        """Parses events in self.E.

        :yield: (Tick, Message, Failed computers, Recovered computers)
        :rtype: (int, Message, [Computer], [Computer])
        """
        # Default dict with dict with keys m, RECOVER and FAIL
        tick_dict = defaultdict(lambda: {"m": None, "RECOVER": [], "FAIL": []})
        # Loop through each row of input split with by spaces
        for t, msg_type, target, value in map(lambda row: row.split(" "), self.E):
            # Convert t from str to int
            t = int(t)
            # If the second argument equals "PROPOSE", it is a message
            if msg_type == "PROPOSE":
                message = Message(
                    src=Client(), dst=Proposer.props[int(target) - 1], type_="PROPOSE", value=value)
                # There can only be one Message per event, set m for that tick
                tick_dict[t]["m"] = message
            # If the msg_type is FAIL or RECOVER, a Computer either fails or recovers
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
                # Multiple Computers can FAIL or RECOVER each event. Append c to list based on msg_type (FAIL or RECOVER)
                tick_dict[t][msg_type].append(c)
            else:
                print("Invalid message type")
                pass
        
        tick_iterator = sorted(tick_dict.items(), key=lambda x: x[0])
        for tick, values in tick_iterator:
            yield int(tick), values["m"], values["FAIL"], values["RECOVER"]

    def run(self):
        """Runs Paxos simulation."""
        # Make parse_events generator object
        events = self.parse_events()
        # Set exit condition to False
        events_empty = False
        # Get first scripted event
        tick, m, F, R = next(events)

        # Padding
        p = len(str(self.tmax))

        # Loop through range(self.tmax) until events is empty and network is empty
        for t in range(self.tmax):
            if events_empty and self.network.is_empty():
                # If events_empty is true, and the queue is empty, exit simulation
                print("\n")
                for P in Computer.props:
                    if P.has_consensus:
                        print(f"{P} heeft wel consensus (voorgesteld: {P.proposed_value}, geaccepteerd: {P.value})")
                    else:
                        print(f"{P} heeft geen consensus.")
                return

            if t != tick:
                # Attempt to extract and deliver message from queue
                extracted_m = self.network.extract_message()
                if extracted_m:
                    print(f"{t:0{p}}: {extracted_m}")
                    extracted_m.dst.deliver_message(extracted_m)
                else:
                    print(f"{t:0{p}}:")
                    pass
            else:
                # Fail all computers that failed during this tick
                for c in F:
                    c.failed = True
                    print(f"{t:0{p}}: ** {c} kapot **")
                # Recover all computers that recovered during this tick
                for c in R:
                    c.failed = False
                    print(f"{t:0{p}}: ** {c} gerepareerd **")

                # If event has message, deliver message
                if m:
                    print(f"{t:0{p}}: {m}")
                    m.dst.deliver_message(m)
                # Else, attempt to extract message from queue and deliver
                else:
                    extracted_m = self.network.extract_message()
                    if extracted_m:
                        print(f"{t:0{p}}: {extracted_m}")
                        extracted_m.dst.deliver_message(extracted_m)

                try:
                    # Get next scripted event
                    tick, m, F, R = next(events)
                except StopIteration:
                    # If the end of events is reached, set events_empty to True
                    events_empty = True


if __name__ == "__main__":
    # n_a1, n_p1, tmax1, E1 = from_text(r"test_input\01.txt")
    # sim1 = Simulation(n_a1, n_p1, tmax1, E1)
    # sim1.run()

    # n_a2, n_p2, tmax2, E2 = from_text(r"test_input\02.txt")
    # sim2 = Simulation(n_a2, n_p2, tmax2, E2)
    # sim2.run()

    # n_a3, n_p3, n_l3, tmax3, E3 = from_text(r"test_input\03.txt")
    # sim3 = Simulation(n_a3, n_p3, n_l3, tmax3, E3)
    # sim3.run()

    n_a4, n_p4, n_l4, tmax4, E4 = from_text(r"test_input\learn.txt")
    sim_learn = Simulation(n_a4, n_p4, n_l4, tmax4, E4)
    sim_learn.run()

    