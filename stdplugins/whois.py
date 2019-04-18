"""Get Telegram Profile Picture and other information
Syntax: .whois @username"""
import html
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from uniborg.util import admin_cmd


@borg.on(admin_cmd("whois ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    replied_user = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await borg(GetFullUserRequest(previous_message.forward.from_id or previous_message.forward.channel_id))
        else:
            replied_user = await borg(GetFullUserRequest(previous_message.from_id))
    else:
        input_str = event.pattern_match.group(1)
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await borg(GetFullUserRequest(user_id))
            else:
                try:
                    user_object = await borg.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await borg(GetFullUserRequest(user_id))
                except Exception as e:
                    await event.edit(str(e))
                    return None
        else:
            try:
                user_object = await borg.get_entity(input_str)
                user_id = user_object.id
                replied_user = await borg(GetFullUserRequest(user_id))
            except Exception as e:
                await event.edit(str(e))
                return None
    logger.info(replied_user)
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Need a Profile Picture to check **this**"
        location = str(e)
    caption = """ID: <code>{}</code>
Name: <a href='tg://user?id={}'>{}</a>
Bio: {}
DC ID: {}
Restricted: {}
Verified: {}
Bot: {}
Groups in Common: {}
""".format(
        user_id,
        user_id,
        first_name,
        user_bio,
        dc_id,
        replied_user.user.restricted,
        replied_user.user.verified,
        replied_user.user.bot,
        common_chats
    )
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await borg.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True
    )
    await event.delete()
