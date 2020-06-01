class Message(object):
    """Message class for Paxos simulation."""

    types = ["PROPOSE",
             "PREPARE",
             "PROMISE",
             "ACCEPT",
             "ACCEPTED",
             "REJECTED",
             ]

    def __init__(self, src, dst, type_, n, value=None):
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
        self.n = n
        self.value = value

    #TODO add n to print statement
    def __repr__(self):
        """__repr__ implementation for Message object.

        :return: Text representation of Message object
        :rtype: string
        """

        return_str = f"{self.src} -> {self.dst} {self.type}"
        if self.type in "PROPOSE":
            return_str += f" v={self.value}"
        else:
            return_str += f" n={self.n}"
            if self.type in ["ACCEPT", "ACCEPTED"]:
                return_str += f" v={self.value}"
            elif self.type == "PROMISE":
                #TODO add prior to print statement
                return_str += f" (Prior: n={14}, v={14})"
        return return_str

    #TODO add n to print statement
    def __str__(self):
        """__str__ implementation for Message object.
        
        :return: Text representation of Message object
        :rtype: string
        """
        return_str = f"{self.src} -> {self.dst} {self.type}"
        if self.type in "PROPOSE":
            return_str += f" v={self.value}"
        else:
            return_str += f" n={self.n}"
            if self.type in ["ACCEPT", "ACCEPTED"]:
                return_str += f" v={self.value}"
            elif self.type == "PROMISE":
                #TODO add prior to print statement
                return_str += f" (Prior: n={14}, v={14})"
        return return_str