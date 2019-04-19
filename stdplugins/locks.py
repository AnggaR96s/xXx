"""Default Permission in Telegram 5.0.1
Available Commands: .lock <option>, .unlock <option>, .locks
API Options: msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo
DB Options: url, bots, forward, commands"""

from telethon import events, functions, types
from sql_helpers.locks_sql import update_lock, is_locked, get_locks
from uniborg.util import admin_cmd


@borg.on(admin_cmd("lock( (?P<target>\S+)|$)"))
async def _(event):
     # Space weirdness in regex required because argument is optional and other
     # commands start with ".lock"
    if event.fwd_from:
        return
    input_str = event.pattern_match.group("target")
    peer_id = event.chat_id
    if input_str in (("url", "bots", "forward", "commands")):
        update_lock(peer_id, input_str, True)
        await event.edit(
            "Locked {}".format(input_str)
        )
    else:
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str:
            if "msg" in input_str:
                msg = True
            if "media" in input_str:
                media = True
            if "sticker" in input_str:
                sticker = True
            if "gif" in input_str:
                gif = True
            if "gamee" in input_str:
                gamee = True
            if "ainline" in input_str:
                ainline = True
            if "gpoll" in input_str:
                gpoll = True
            if "adduser" in input_str:
                adduser = True
            if "cpin" in input_str:
                cpin = True
            if "changeinfo" in input_str:
                changeinfo = True
        banned_rights = types.ChatBannedRights(
            until_date=None,
            # view_messages=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            result = await borg(  # pylint:disable=E0602
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=peer_id,
                    banned_rights=banned_rights
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "Current Chat Default Permissions Changed Successfully, in API"
            )


@borg.on(admin_cmd("unlock ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("url", "bots", "forward", "commands")):
        update_lock(peer_id, input_str, False)
        await event.edit(
            "UnLocked {}".format(input_str)
        )
    else:
        await event.edit(
            "Use `.lock` without any parameters to unlock API locks"
        )


@borg.on(admin_cmd("lks"))
async def _(event):
    if event.fwd_from:
        return
    res = ""
    current_db_locks = get_locks(event.chat_id)
    if not current_db_locks:
        res = "There are no DataBase locks in this chat"
    else:
        res = "Following are the DataBase locks in this chat: \n"
        res += "👉 `url`: `{}`\n".format(current_db_locks.url)
        res += "👉 `forward`: `{}`\n".format(current_db_locks.forward)
        res += "👉 `bots`: `{}`\n".format(current_db_locks.bots)
        res += "👉 `commands`: `{}`\n".format(current_db_locks.commands)
    current_chat = await event.get_chat()
    try:
        current_api_locks = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        res += "\nFollowing are the API locks in this chat: \n"
        res += "👉 `msg`: `{}`\n".format(current_api_locks.send_messages)
        res += "👉 `media`: `{}`\n".format(current_api_locks.send_media)
        res += "👉 `sticker`: `{}`\n".format(current_api_locks.send_stickers)
        res += "👉 `gif`: `{}`\n".format(current_api_locks.send_gifs)
        res += "👉 `gamee`: `{}`\n".format(current_api_locks.send_games)
        res += "👉 `ainline`: `{}`\n".format(current_api_locks.send_inline)
        res += "👉 `gpoll`: `{}`\n".format(current_api_locks.send_polls)
        res += "👉 `adduser`: `{}`\n".format(current_api_locks.invite_users)
        res += "👉 `cpin`: `{}`\n".format(current_api_locks.pin_messages)
        res += "👉 `changeinfo`: `{}`\n".format(current_api_locks.change_info)
    await event.edit(res)


@borg.on(events.MessageEdited())  # pylint:disable=E0602
@borg.on(events.NewMessage())  # pylint:disable=E0602
async def check_incoming_messages(event):
    # result = await borg(functions.channels.GetParticipantRequest(
    #     channel=event.chat_id,
    #     user_id=event.message.from_id
    # ))
    # if not event.is_private and isinstance(result.participant, (types.ChannelParticipantCreator, types.ChannelParticipantAdmin)):
    #     # locks should not be affected for admins of the group
    #     return False
    peer_id = event.chat_id
    if is_locked(peer_id, "forward"):
        if event.fwd_from:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "forward", False)
    if is_locked(peer_id, "url"):
        entities = event.message.entities
        is_url = False
        if entities:
            for entity in entities:
                if isinstance(entity, (types.MessageEntityTextUrl, types.MessageEntityUrl)):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "url", False)
    if is_locked(peer_id, "commands"):
        entities = event.message.entities
        is_command = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityBotCommand):
                    is_command = True
        if is_command:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "commands", False)


@borg.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    # result = await borg(functions.channels.GetParticipantRequest(
    #     channel=event.chat_id,
    #     user_id=event.action_message.from_id
    # ))
    # if not event.is_private and not isinstance(result.participant, (types.ChannelParticipantCreator, types.ChannelParticipantAdmin)):
    #     # locks should not be affected for admins of the group
    #     return False
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
            if Config.G_BAN_LOGGER_GROUP != -100123456789 and is_ban_able:
                ban_reason_msg = await event.reply(
                    "!warn [user](tg://user?id={}) Please Do Not Add BOTs to this chat.".format(users_added_by)
                )
