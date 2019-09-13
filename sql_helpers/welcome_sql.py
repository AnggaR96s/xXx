from sqlalchemy import BigInteger, Boolean, Column, LargeBinary, Numeric, String, UnicodeText
from sql_helpers import SESSION, BASE


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    custom_welcome_message = Column(UnicodeText)
    message_type = Column(Numeric)
    media_id = Column(UnicodeText)
    media_access_hash = Column(UnicodeText)
    media_file_reference = Column(LargeBinary)
    should_clean_welcome = Column(Boolean, default=False)
    previous_welcome = Column(BigInteger)

    def __init__(
        self,
        chat_id,
        custom_welcome_message,
        should_clean_welcome,
        previous_welcome,
        message_type=0,
        media_id=None,
        media_access_hash=None,
        media_file_reference=None,
    ):
        self.chat_id = chat_id
        self.custom_welcome_message = custom_welcome_message
        self.message_type = message_type
        self.media_id = media_id
        self.media_access_hash = media_access_hash
        self.media_file_reference = media_file_reference
        self.should_clean_welcome = should_clean_welcome
        self.previous_welcome = previous_welcome


Welcome.__table__.create(checkfirst=True)


def get_current_welcome_settings(chat_id):
    try:
        return SESSION.query(Welcome).filter(Welcome.chat_id == str(chat_id)).one()
    except:
        return None
    finally:
        SESSION.close()


def add_welcome_setting(
    chat_id,
    custom_welcome_message,
    should_clean_welcome,
    previous_welcome,
    message_type=0,
    media_id=None,
    media_access_hash=None,
    media_file_reference=None
):
    # adder = SESSION.query(Welcome).get(chat_id)
    adder = Welcome(
        chat_id,
        custom_welcome_message,
        should_clean_welcome,
        previous_welcome,
        message_type,
        media_id,
        media_access_hash,
        media_file_reference
    )
    SESSION.add(adder)
    SESSION.commit()


def rm_welcome_setting(chat_id):
    rem = SESSION.query(Welcome).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def update_previous_welcome(chat_id, previous_welcome):
    row = SESSION.query(Welcome).get(str(chat_id))
    row.previous_welcome = previous_welcome
    # commit the changes to the DB
    SESSION.commit()
