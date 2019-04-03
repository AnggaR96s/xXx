"""Greetings
Commands:
.clearwelcome
.savewelcome <Welcome Message>"""
from telethon import events
from telethon.tl import types, functions
from sql_helpers.locks_sql import update_lock, is_locked
from sql_helpers.welcome_sql import get_current_welcome_settings, \
    add_welcome_setting, rm_welcome_setting, update_previous_welcome
from uniborg.util import admin_cmd


@borg.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await borg.delete_messages(  # pylint:disable=E0602
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            try:
                user_ids = event.action_message.action.users
            except AttributeError:
                user_ids = [event.action_message.from_id]
            for user_id in user_ids:
                current_saved_welcome_message = cws.custom_welcome_message
                user_obj = await borg.get_entity(user_id)  # pylint:disable=E0602
                mention = "[{}](tg://user?id={})".format(user_obj.first_name, user_id)
                current_message = await event.reply(
                    current_saved_welcome_message.format(mention=mention)
                )
                update_previous_welcome(event.chat_id, current_message.id)
    # check for "lock" "bots"
    if is_locked(event.chat_id, "bots"):
        # bots are limited Telegram accounts,
        # and cannot join by themselves
        if event.user_added:
            users_added_by = event.action_message.from_id
            is_ban_able = False
            rights = types.ChatBannedRights(
                until_date=None,
                view_messages=True
            )
            added_users = event.action_message.action.users
            for user_id in added_users:
                user_obj = await borg.get_entity(user_id)
                if user_obj.bot:
                    is_ban_able = True
                    try:
                        await borg(functions.channels.EditBannedRequest(
                            event.chat_id,
                            user_obj,
                            rights
                        ))
                    except Exception as e:
                        await event.reply(
                            "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                        )
                        update_lock(event.chat_id, "bots", False)
                        break
            if is_ban_able:
                ban_reason_msg = await event.reply(
                    "!warn [user](tg://user?id={}) Please Do Not Add BOTs to this chat.".format(users_added_by)
                )



@borg.on(admin_cmd(r"\.savewelcome (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    add_welcome_setting(event.chat_id, input_str, True, 0)
    await event.edit("Welcome note saved. ")


@borg.on(admin_cmd(r"\.clearwelcome"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.edit(
        "Welcome note cleared. " + \
        "The previous welcome message was `{}`.".format(cws.custom_welcome_message)
    )
