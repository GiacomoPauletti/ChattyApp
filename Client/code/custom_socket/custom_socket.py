import socket
HEADER=32
FORMAT='utf-8'

class SocketDecorator:
    def __init__(self, socket):
        self.__socket=socket

    def recv_with_header(self):
        """
        SocketDecorator.recv_with_header(self)
        The socket will first receive the header, which must be "HEADER"-byte
        long and it specifies the length of the actual message.
        Then the socket receives the actual message and it return back it
        decoded following the "FORMAT" protocol
        """

        msg_len = self.__socket.recv(HEADER).decode(FORMAT)
        msg_len = int(msg_len)
        msg= self.__socket.recv(msg_len).decode(FORMAT)
        return msg

    def send_with_header(self, msg : str):
        """
        SocketDecorator.send_with_header(self, message)

        The header is created containing the length of the message. The header
        and the message are then concatenated, encoded following the "FORMAT"
        protocol and sent to the socket
        """

        msg_len=f"{len(msg)}".encode(FORMAT)
        msg_len += (' ' * (HEADER - len(msg_len))).encode(FORMAT)

        msg = msg_len + msg.encode(FORMAT)

        self.__socket.send(msg)

    def __getattr__(self, name):
        """
        Called when an attribute is not found
        If it is not an attribute of the SocketDecorator, it is searched between
        the attributes of the decorated socket and if found is returned back
        """
        attr=getattr(self.__socket, name)

        return attr
