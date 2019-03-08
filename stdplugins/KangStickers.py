from telethon import events
from io import BytesIO
from PIL import Image
import datetime
import math
import requests
from telethon.errors.rpcerrorlist import StickersetInvalidError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (DocumentAttributeFilename,
                               DocumentAttributeSticker,
                               InputMediaUploadedDocument,
                               InputPeerNotifySettings, InputStickerSetID,
                               InputStickerSetShortName, MessageMediaPhoto)


@borg.on(events.NewMessage(pattern=r"\.kangsticker ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to a photo to add to my personal sticker pack.")
        return
    reply_message = await event.get_reply_message()
    sticker_emoji = "🔥"
    input_str = event.pattern_match.group(1)
    if input_str:
        sticker_emoji = input_str
    if not is_message_image(reply_message):
        await event.edit("Invalid message type")
        return
    me = borg.me
    userid = event.from_id
    packname = f"{userid}'s @UniBorg Pack"
    packshortname = f"Uni_Borg_{userid}" # format: Uni_Borg_userid

    await event.edit("Processing this sticker. Please Wait!")

    async with borg.conversation("@Stickers") as bot_conv:
        now = datetime.datetime.now()
        dt = now + datetime.timedelta(minutes=1)
        file = await borg.download_file(reply_message.media)
        with BytesIO(file) as mem_file, BytesIO() as sticker:
            resize_image(mem_file, sticker)
            sticker.seek(0)
            uploaded_sticker = await borg.upload_file(sticker, file_name="@UniBorg_Sticker.png")
            if not await stickerset_exists(bot_conv, packshortname):
                await silently_send_message(bot_conv, "/cancel")
                response = await silently_send_message(bot_conv, "/newpack")
                if response.text != "Yay! A new stickers pack. How are we going to call it? Please choose a name for your pack.":
                    await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
                    return
                response = await silently_send_message(bot_conv, packname)
                if not response.text.startswith("Alright!"):
                    await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
                    return
                await bot_conv.send_file(
                    InputMediaUploadedDocument(
                        file=uploaded_sticker,
                        mime_type='image/png',
                        attributes=[
                            DocumentAttributeFilename(
                                "@UniBorg_Sticker.png"
                            )
                        ]
                    ),
                    force_document=True
                )
                await bot_conv.get_response()
                await silently_send_message(bot_conv, sticker_emoji)
                await silently_send_message(bot_conv, "/publish")
                response = await silently_send_message(bot_conv, packshortname)
                if response.text == "Sorry, this short name is already taken.":
                    await event.edit(f"**FAILED**! @Stickers replied: {response.text}")
                    return
            else:
                await silently_send_message(bot_conv, "/cancel")
                await silently_send_message(bot_conv, "/addsticker")
                await silently_send_message(bot_conv, packshortname)
                await bot_conv.send_file(
                    InputMediaUploadedDocument(
                        file=uploaded_sticker,
                        mime_type='image/png',
                        attributes=[
                            DocumentAttributeFilename(
                                "@UniBorg_Sticker.png"
                            )
                        ]
                    ),
                    force_document=True
                )
                response = await bot_conv.get_response()
                await silently_send_message(bot_conv, response)
                await silently_send_message(bot_conv, sticker_emoji)
                await silently_send_message(bot_conv, "/done")

    await event.edit(f"sticker added! Your pack can be found [here](t.me/addstickers/{packshortname})")


@borg.on(events.NewMessage(pattern=r"\.packinfo", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to any sticker to get it's pack info.")
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await event.edit("Reply to any sticker to get it's pack info.")
        return
    stickerset_attr = rep_msg.document.attributes[1]
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await event.edit("sticker does not belong to a pack.")
        return
    get_stickerset = await borg(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    await event.edit(f"**Sticker Title:** `{get_stickerset.set.title}\n`" \
             f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n" \
             f"**Official:** `{get_stickerset.set.official}`\n" \
             f"**Archived:** `{get_stickerset.set.archived}`\n" \
             f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n" \
             f"**Emojis In Pack:** {' '.join(pack_emojis)}")


# Helpers

def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


async def stickerset_exists(conv, setname):
    try:
        await borg(GetStickerSetRequest(InputStickerSetShortName(setname)))
        response = await silently_send_message(conv, "/addsticker")
        if response.text == "Invalid pack selected.":
            await silently_send_message(conv, "/cancel")
            return False
        await silently_send_message(conv, "/cancel")
        return True
    except StickersetInvalidError:
        return False


def resize_image(image, save_locaton):
    """ Copyright Rhyse Simpson:
        https://github.com/skittles9823/SkittBot/blob/master/tg_bot/modules/stickers.py
    """
    im = Image.open(image)
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
    im.save(save_locaton, "PNG")
