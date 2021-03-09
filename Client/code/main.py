import socket, threading
login_server_address=('192.168.1.80', '8000')


if __name__ == "__main__":

    with socket.create_connection(login_server_address) as login_server:
        print('[main] connected to the login server')

