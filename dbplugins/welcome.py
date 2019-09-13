"""Greetings
Commands:
.clearwelcome
.savewelcome <Welcome Message>"""

from telethon import events, utils
from telethon.tl import types
from sql_helpers.welcome_sql import get_current_welcome_settings, \
    add_welcome_setting, rm_welcome_setting, update_previous_welcome
from uniborg.util import admin_cmd

TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


@borg.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined or event.user_added:
            if cws.should_clean_welcome:
                try:
                    await borg.delete_messages(  # pylint:disable=E0602
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            a_user = await event.get_user()
            current_saved_welcome_message = cws.custom_welcome_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            file_media = None
            if cws.message_type == TYPE_PHOTO:
                file_media = types.InputPhoto(
                    int(cws.media_id),
                    int(cws.media_access_hash),
                    cws.media_file_reference
                )
            elif cws.message_type == TYPE_DOCUMENT:
                file_media = types.InputDocument(
                    int(cws.media_id),
                    int(cws.media_access_hash),
                    cws.media_file_reference
                )
            else:
                file_media = None
            #
            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention),
                file=file_media
            )
            update_previous_welcome(event.chat_id, current_message.id)


@borg.on(admin_cmd(pattern="savewelcome"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        media = None
        message_type = TYPE_TEXT
        if isinstance(msg.media, types.MessageMediaPhoto):
            media = utils.get_input_photo(msg.media.photo)
            message_type = TYPE_PHOTO
        elif isinstance(msg.media, types.MessageMediaDocument):
            media = utils.get_input_document(msg.media.document)
            message_type = TYPE_DOCUMENT
        #
        add_welcome_setting(event.chat_id, msg.message, True, 0, message_type, media.id, media.access_hash, media.file_reference)
        await event.edit("Welcome note saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], True, 0)
        await event.edit("Welcome note saved. ")


@borg.on(admin_cmd(pattern="clearwelcome"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.edit(
        "Welcome note cleared. " + \
        "The previous welcome message was `{}`.".format(cws.custom_welcome_message)
    )
