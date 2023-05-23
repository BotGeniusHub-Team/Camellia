import threading

from sqlalchemy import Column, String

from camillia.modules.sql import BASE, SESSION


class camilliaChats(BASE):
    __tablename__ = "camillia_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


camilliaChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_camillia(chat_id):
    try:
        chat = SESSION.query(camilliaChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_camillia(chat_id):
    with INSERTION_LOCK:
        camilliachat = SESSION.query(camilliaChats).get(str(chat_id))
        if not camilliachat:
            camilliachat = camilliaChats(str(chat_id))
        SESSION.add(camilliachat)
        SESSION.commit()


def rem_camillia(chat_id):
    with INSERTION_LOCK:
        camilliachat = SESSION.query(camilliaChats).get(str(chat_id))
        if camilliachat:
            SESSION.delete(camilliachat)
        SESSION.commit()
