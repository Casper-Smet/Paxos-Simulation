from collections import defaultdict
from classes.computer import Acceptor, Computer, Proposer, Network, Message


def from_text(fp: str):
    """Function for processing .txt files with Paxos instructions

    :param fp: Filepath
    :type fp: str
    :return: n_p, n_a, tmax, E
    :rtype: (int, int, int, list)
    """
    with open(fp, "r") as file:
        lines = [line.strip() for line in file]

    n_p, n_a, tmax = lines.pop(0).split(" ")
    return int(n_p), int(n_a), int(tmax), lines[:-1]


class Simulation:

    def __init__(self, n_p: int, n_a: int, tmax: int, E: list):
        """[summary]

        Arguments:
            n_p {[type]} -- [description]
            n_a {[type]} -- [description]
            tmax {[type]} -- [description]
            E {[type]} -- [description]
        """
        self.network = Network()

        # Make n_p Proposers
        self.P = [Proposer(i + 1, self.network) for i in range(n_p)]
        # Make n_a Acceptors
        self.A = [Acceptor(i + 1, self.network) for i in range(n_a)]
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
                    src="  ", dst=Proposer.props[int(target) - 1], type_="PROPOSE", value=value)
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

        # Loop through range(self.tmax) until events is empty and network is empty
        for t in range(self.tmax):
            if events_empty and self.network.is_empty():
                # If events_empty is true, and the queue is empty, exit simulation
                # TODO add necessary prints here
                return

            if t != tick:
                # Attempt to extract and deliver message from queue
                extracted_m = self.network.extract_message()
                if extracted_m:
                    print(f"{t:03}: {extracted_m}")
                    Computer.deliver_message(extracted_m.dst, extracted_m)
                else:
                    print(f"{t:03}:")
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

                # If event has message, deliver message
                if m:
                    print(f"{t:03}: {m}")
                    Computer.deliver_message(m.dst, m)
                # Else, attempt to extract message from queue and deliver
                else:
                    extracted_m = self.network.extract_message()
                    if extracted_m:
                        print(f"{t:03}: {extracted_m}")
                        Computer.deliver_message(extracted_m.dst, extracted_m)

                try:
                    # Get next scripted event
                    tick, m, F, R = next(events)
                except StopIteration:
                    # If the end of events is reached, set events_empty to True
                    events_empty = True


if __name__ == "__main__":
    n_a1, n_p1, tmax1, E1 = from_text(r"test_input\01.txt")
    sim1 = Simulation(n_a1, n_p1, tmax1, E1)
    sim1.run()

    # n_a2, n_p2, tmax2, E2 = from_text(r"test_input\02.txt")
    # sim2 = Simulation(n_a2, n_p2, tmax2, E2)
    # sim2.run()
