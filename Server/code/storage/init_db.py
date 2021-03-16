import os

def text_init_db(db_path='.'):
    db_path=db_path.rstrip('/')

    os.mkdir(db_path) 
    os.mkdir(db_path + '/chats')
    os.mkdir(db_path + '/users') 
    

   
