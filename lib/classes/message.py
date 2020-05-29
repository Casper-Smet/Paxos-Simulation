class Message(object):
    """Message class for Paxos simulation."""

    types = ["PROPOSE",
             "PREPARE",
             "PROMISE",
             "ACCEPT",
             "ACCEPTED",
             "REJECTED",
             ]

    def __init__(self, src, dst, type_, value):
        """Init for Message class.

        :param src: [description]
        :type src: [type]
        :param dst: [description]
        :type dst: [type]
        :param type_: [description]
        :type type_: [type]
        :param value: [description]
        :type  value: [type]
        """
        assert type_ in self.types, f"{type_} is not a valid message type"
        self.src = src
        self.dst = dst
        self.type = type_
        self.value = value

    def __repr__(self):
        """__repr__ implementation for Message object.

        :return: Text representation of Message object
        :rtype: string
        """
        return f"{self.src}-{self.dst}-{self.type}"

    def __str__(self):
        """__str__ implementation for Message object.
        
        :return: Text representation of Message object
        :rtype: string
        """
        return f"{self.src}-{self.dst}-{self.type}"