from telethon import events
import asyncio
from telethon.tl.functions.channels import EditBannedRequest


borg.storage.CHAT_FLOOD = {}


@borg.on(events.NewMessage(chats=Config.CHATS_TO_MONITOR_FOR_ANTI_FLOOD))
async def _(event):
    chat = await event.get_chat()
    if not event.chat_id in borg.storage.CHAT_FLOOD:
        borg.storage.CHAT_FLOOD[event.chat_id] = {}
    if event.chat_id in borg.storage.CHAT_FLOOD:
        if event.message.from_id in borg.storage.CHAT_FLOOD[event.chat_id]:
            current_count = int(borg.storage.CHAT_FLOOD[event.chat_id][1])
            current_count += 1
            if current_count > Config.MAX_ANTI_FLOOD_MESSAGES:
                borg.storage.CHAT_FLOOD[event.chat_id] = (event.message.from_id, 0)
                try:
                    await borg(EditBannedRequest(event.chat_id, event.message.from_id, Config.ANTI_FLOOD_WARN_MODE))
                except (Exception) as exc:
                    m1 = await borg.send_message(
                        entity=event.chat_id,
                        message="**Automatic AntiFlooder**\n @admin [User](tg://user?id={}) is flooding this chat. \n`{}`".format(event.message.from_id, str(exc)),
                        reply_to=event.message.id
                    )
                    await asyncio.sleep(10)
                    await m1.edit("https://t.me/keralagram/724970")
                else:
                    await borg.send_message(
                        entity=event.chat_id,
                        message="**Automatic AntiFlooder**\n[User](tg://user?id={}) has been automatically restricted because he reached the defined flood limit.".format(event.message.from_id),
                        reply_to=event.message.id
                    )
            else:
                borg.storage.CHAT_FLOOD[event.chat_id] = (event.message.from_id, current_count)
        else:
            borg.storage.CHAT_FLOOD[event.chat_id] = (event.message.from_id, 1)

