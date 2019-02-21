from telethon import events
import datetime
import asyncio


borg.storage.USER_AFK = {}
borg.storage.afk_time = None


intervals = (
    ("weeks", 604800),
    ("days", 86400),
    ("hours", 3600),
    ("minutes", 60),
    ("seconds", 1),
)


@borg.on(events.NewMessage(outgoing=True))
async def _(event):
    current_message = event.message.message
    if ".afk" not in current_message and "yes" in borg.storage.USER_AFK:
        await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, "Set AFK mode to False")
        borg.storage.USER_AFK = {}
        borg.storage.afk_time = None


@borg.on(events.NewMessage(pattern=r"\.afk ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if not borg.storage.USER_AFK:
        borg.storage.afk_time = datetime.datetime.now()
        borg.storage.USER_AFK.update({"yes": reason})
        if reason:
            await event.edit(f"Set AFK mode to True, and Reason is {reason}")
        else:
            await event.edit(f"Set AFK mode to True")
        await asyncio.sleep(5)
        await event.delete()
        await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, f"Set AFK mode to True, and Reason is {reason}")


@borg.on(events.NewMessage(
    incoming=True,
    func=lambda e: True if e.mentioned or e.is_private else False,
    blacklist_chats=Config.UB_BLACK_LIST_CHAT
))
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.mentioned or event.is_private and not (await event.get_sender()).bot:
        if borg.storage.USER_AFK:
            reason = borg.storage.USER_AFK["yes"]
            now = datetime.datetime.now()

            dt = now - borg.storage.afk_time
            time = float(dt.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time

            if days == 1:
                afk_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime('%A, %Y %B %m, %H:%I')
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                afk_since = f"`{int(seconds)}s` **ago**"

            msg = None
            if not reason:
                msg = await event.reply(f"I'm afk since {afk_since} and I will be back soon.")
            else:
                msg = await event.reply(f"I'm afk since {afk_since} and I will be back soon\n__Reason:__ {reason}")
            await asyncio.sleep(5)
            await msg.delete()
