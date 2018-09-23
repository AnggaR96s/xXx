from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins, ChatParticipantCreator
from telethon.errors import ChatAdminRequiredError, InputUserDeactivatedError


@borg.on(events.NewMessage(pattern=".get_admin ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this Channel**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "Admins in {} channel: \n".format(input_str)
        try:
            chat = await borg.get_entity(input_str)
        except ValueError as e:
            await event.edit(str(e))
            return None
    try:
        async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not x.deleted:
                mentions += f"\n[{x.first_name}](tg://user?id={x.id}) `{x.id}`"
            else:
                mentions += f"\n InputUserDeactivatedError `{x.id}`"
    except ChatAdminRequiredError as e:
        mentions += " " + str(e) + "\n"
    await borg.send_message(
        to_write_chat,
        mentions,
        reply_to=event.message.reply_to_msg_id
    )
    await event.delete()
