from telethon import events
import io
from PIL import Image
import math
import requests
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto


@borg.on(events.NewMessage(pattern=r"\.kangsticker", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    userid = event.from_id
    packname = f"UniBorgPack_{userid}"
    sticker_pack_url = f"http://t.me/addstickers/{packname}"
    response = requests.get(sticker_pack_url).text.split("\n")
    reply_message = await event.get_reply_message()
    photo = None
    emoji = "🔥"
    if reply_message and reply_message.media:
        if isinstance(reply_message.media, MessageMediaPhoto):
            photo = io.BytesIO()
            photo = await borg.download_media(
                message=reply_message.media.photo,
                file=photo
            )
        elif "image" in reply_message.media.document.mime_type.split('/'):
            photo = io.BytesIO()
            await borg.download_file(
                reply_message.media.document,
                photo
            )
            if DocumentAttributeFilename(file_name="sticker.webp") in reply_message.media.document.attributes and len(reply_message.media.document.attributes) > 1:
                emoji = reply_message.media.document.attributes[1].alt
        else:
            await event.edit("Reply to a photo to add to my personal sticker pack.")
            return False
    else:
        await event.edit("Reply to a photo to add to my personal sticker pack.")
        return False

    if photo:
        im = Image.open(photo)
        maxsize = (512, 512)
        if (im.width and im.height) < 512:
            size1 = im.width
            size2 = im.height
            if im.width > im.height:
                scale = 512 / size1
                size1new = 512
                size2new = size2 * scale
            else:
                scale = 512 / size2
                size1new = size1 * scale
                size2new = 512
            size1new = math.floor(size1new)
            size2new = math.floor(size2new)
            sizenew = (size1new, size2new)
            im = im.resize(sizenew)
        else:
            im.thumbnail(maxsize)

        file = io.BytesIO()
        file.name = "sticker.png"
        im.save(file, "PNG")

        if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in response:
            async with borg.conversation("@Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                await conv.send_message(packname)
                await conv.get_response()
                file.seek(0)
                await conv.send_file(file, force_document=True)
                await conv.get_response()
                await conv.send_message(emoji)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
        else:
            await event.edit("userbot sticker pack doesn't exist! Making a new one!")
            async with borg.conversation("@Stickers") as conv:
                await conv.send_message("/newpack")
                await conv.get_response()
                await conv.send_message(f"@UniBorg Sticker Pack for {userid}")
                await conv.get_response()
                file.seek(0)
                await conv.send_file(file, force_document=True)
                await conv.get_response()
                await conv.send_message(emoji)
                await conv.get_response()
                await conv.send_message("/publish")
                await conv.get_response()
                await conv.send_message(packname)
                await conv.get_response()
        await event.edit(f"sticker added! Your pack can be found [here](t.me/addstickers/{packname})")
