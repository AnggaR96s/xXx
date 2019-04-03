"""Default Permission in Telegram 5.0.1
Available Commands: .lock <option>, .unlock <option>, .dblocks
API Options: msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo
DB Options: url, bots, forward"""
import asyncio
from telethon import events, functions, types
from sql_helpers.locks_sql import update_lock, is_locked, get_locks
from uniborg.util import admin_cmd


@borg.on(admin_cmd(r"\.lock ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("url", "bots", "forward")):
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
        banned_rights=types.ChatBannedRights(
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


@borg.on(admin_cmd(r"\.unlock ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("url", "bots", "forward")):
        update_lock(peer_id, input_str, False)
        await event.edit(
            "UnLocked {}".format(input_str)
        )
    else:
        await event.edit(
            "Use `.lock` without any parameters to unlock API locks"
        )


@borg.on(admin_cmd(r"\.dblocks"))
async def _(event):
    if event.fwd_from:
        return
    res = ""
    current_locks = get_locks(event.chat_id)
    if not current_locks:
        res = "There are no DataBase locks in this chat"
    else:
        res = "Following are the DataBase locks in this chat: \n"
        res += "👉 `url`: `{}`\n".format(current_locks.url)
        res += "👉 `forward`: `{}`\n".format(current_locks.forward)
        res += "👉 `bots`: `{}`\n".format(current_locks.bots)
    await event.edit(res)


@borg.on(events.MessageEdited())  # pylint:disable=E0602
@borg.on(events.NewMessage())  # pylint:disable=E0602
async def check_incoming_messages(event):
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
                if isinstance(entity, types.MessageEntityTextUrl) or isinstance(entity, types.MessageEntityUrl):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "url", False)
