import socket, threading
import message.message as msg
import custom_socket.custom_socket as cs

login_server_address=('192.168.1.80', '8000')

class Receiver:
    def __init__(self, server):
        self.__server=server
        self.__is_online=True

    def receive(self):
        receive_thread=threading.Thread(target=self._receive)
        receive_thread.start()

    def _receive(self):
        while self.__is_online:
            print('[Receiver] user is now receiving from server') 
            message=self.__server.recv_with_header()
            print(message)

    def is_online(self):
        return self.__is_online

    def shutdown(self):
        self.__is_online=False

if __name__ == "__main__":

    with socket.create_connection(login_server_address) as real_login_server:
        print('[main] connected to the login server')
        
        login_server=cs.SocketDecorator(real_login_server)

        receiver=Receiver(login_server)
        receiver.receive()

        login_msg=msg.AccessMessage(private_name='john', password='akab', email='')
        login_server.send_with_header(str(login_msg))


