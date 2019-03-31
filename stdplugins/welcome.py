"""Greetings
Commands:
.clearwelcome
.savewelcome <Welcome Message>"""
from telethon import events
from sql_helpers.welcome_sql import get_current_welcome_settings, \
    add_welcome_setting, rm_welcome_setting, update_previous_welcome


@borg.on(events.ChatAction())
async def welcome(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """
        user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,
        """
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await borg.delete_messages(
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:
                    logger.warn(str(e))
            try:
                user_ids = event.action_message.action.users
            except AttributeError as e:
                user_ids = [event.action_message.from_id]
            for user_id in user_ids:
                current_saved_welcome_message = cws.custom_welcome_message
                user_obj = await borg.get_entity(user_id)
                mention = "[{}](tg://user?id={})".format(user_obj.first_name, user_id)
                current_message = await event.reply(
                    current_saved_welcome_message.format(mention=mention)
                )
                update_previous_welcome(event.chat_id, current_message.id)


@borg.on(events.MessageEdited(pattern=r"\.savewelcome (.*)", outgoing=True))
@borg.on(events.NewMessage(pattern=r"\.savewelcome (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    add_welcome_setting(event.chat_id, input_str, True, 0)
    await event.edit("Welcome note saved. ")


@borg.on(events.MessageEdited(pattern=r"\.clearwelcome", outgoing=True))
@borg.on(events.NewMessage(pattern=r"\.clearwelcome", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.edit("Welcome note cleared. The previous welcome message was `{}`.".format(cws.custom_welcome_message))
