class Message(object):
    """Message class for Paxos simulation."""

    types = ["PROPOSE",
             "PREPARE",
             "PROMISE",
             "ACCEPT",
             "ACCEPTED",
             "REJECTED",
             ]

    def __init__(self, src, dst, type_):
        """Init for Message class.

        :param src: [description]
        :type src: [type]
        :param dst: [description]
        :type dst: [type]
        :param type_: [description]
        :type type_: [type]
        """
        assert type_ in self.types, f"{type_} is not a valid message type"
        self.src = src
        self.dst = dst
        self.type = type_
