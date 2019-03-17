from telethon import events
import os
from PIL import Image, ImageColor


@borg.on(events.NewMessage(pattern=r"\.color (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if input_str.startswith("#"):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            await event.edit(str(e))
            return False
        else:
            im = Image.new(mode="RGB", size=(128, 128), color=usercolor)
            im.save("UniBorg.webp", "PNG")
            await borg.send_file(
                event.chat_id,
                "UniBorg.webp",
                caption=input_str,
                reply_to=message_id
            )
            os.remove("UniBorg.webp")
            await event.delete()
