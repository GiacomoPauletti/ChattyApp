import threading, socket
from custom_socket.custom_socket import SocketDecorator

class ChatHandlerListener:
    def __init__(self, chat_handler):
        self.__address=('', 11000)
        self.__is_listening=False
        self.__chat_handler=chat_handler

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        with socket.create_server(self.__address) as real_server:
            print('[ChatHandlerServer] server is now listening')
            server=SocketDecorator(real_server)

            self.__is_listening=True
            while self.__is_listening:
                print('[ChatHandlerServer] new connection')
                real_client, address=server.accept()
                client=SocketDecorator(real_client)

                self.__chat_handler.handle(client, address)
    

    def stop(self):
        self.__is_listening=False

class ChatHandler:
    def __init__(self, user_message_class, answer_message_class, chat_creator, user_chat_storage, active_chat_register):
        self.__UserMessage=user_message_class
        self.__AnswerMessageClass=answer_message_class
        self.__chat_creator=chat_creator
        self.__active_chat_register=active_chat_register
        self.__user_chat_storage=user_chat_storage

        self.__client_action_map={'create_chat':self.new_chat, 'leave_chat':self.leave_chat, 'join_chat':self.join_chat, 'add_users_to_chat':self.add_users_to_chat}

    def handle(self, client, client_address):
        handle_thread=threading.Thread(target=self._handle, args=(client, client_address))
        handler_thread.start()

    def _handle(self, client, client_address):
        while True:
            try:
                msg=client.recv_with_header()
                msg=self.__UserMessage.from_string(msg)

                self.__client_action_map[msg.get_action()](client=client, client_address=client_address, msg=msg)
            except:
                pass

    def new_chat(self, client, client_address, msg):
        #generazione di un nuovo chatid (forse) al posto di questo commento

        chatid=msg.get_chat()
        if self.__chat_creator(chatid):
            print('[ChatHandler] new chat created')
            #essendo stata appena creata, la chat non può essere nel registro, così chiamare il metodo .get() mi crea l'oggetto e me lo aggiunge al registro
            chat_obj=self.__active_chat_register.get(chatid)

            self.join_chat(client, client_address, msg)
            self.add_users_to_chat(client, client_address, msg)

            #bisogna notificare gli utenti di essere stati aggiunti

            client.send_with_header(self.__AnswerMessageClass(answer='success'))
        else:
            client.send_with_header(self.__AnswerMessageClass(answer='failed'))     #aggiungere "error=..."
        
            

    def leave_chat(self, client, client_address, msg):
        chatid=msg.get_chat()
        
        if self.__user_chat_storage.remove_user(chatid, msg.get_sender()):
            client.send_with_header(self.__AnswerMessageClass(answer='success'))
        else:
            client.send_with_header(self.__AnswerMessageClass(answer='success'))

    def join_chat(self, client, client_address, msg):
        chatid=msg.get_chat()

        self.__user_chat_storage.add_user(chatid, msg.get_sender())

    def add_users_to_chat(self, client, client_address, msg):
        chatid=msg.get_chat()

        for user in msg.get_users():
           self.__user_chat_storage.add_user(chatid, user)
        


