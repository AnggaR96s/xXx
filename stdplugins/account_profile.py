"""Profile Updation Commands
.pbio <Bio>
.pname <Name>
.ppic"""
import asyncio
import io
import os
from telethon import events
from telethon.tl import functions, types


@borg.on(events.NewMessage(pattern=r"\.pbio (.*)", outgoing=True))
async def change_bio(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await borg(functions.account.UpdateProfileRequest(about=bio))
        await event.edit("Succesfully changed my profile bio")
    except Exception as e:
        await event.edit(str(e))


@borg.on(events.NewMessage(pattern=r"\.pname ((.|\n)*)", outgoing=True))
async def change_name(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    firstName = names
    lastName = ""
    if  "\\n" in names:
        firstName, lastName = name.split("\\n", 1)
    try:
        await borg(functions.account.UpdateProfileRequest(first_name=firstName, last_name=lastName))
        await event.edit("My name was changed successfully")
    except Exception as e:
        await event.edit(str(e))


@borg.on(events.NewMessage(pattern=r"\.ppic", outgoing=True))
async def set_profile_picture(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("Downloading Profile Picture to my local ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await borg.download_media(reply_message, Config.TMP_DOWNLOAD_DIRECTORY)
    except Exception as e:
        await event.edit(str(e))
    else:
        if photo:
            await event.edit("now, Uploading to @Telegram ...")
            file = await borg.upload_file(photo)
            try:
                await borg(functions.photos.UploadProfilePhotoRequest(file))
            except Exception as e:
                await event.edit(str(e))
            else:
                await event.edit("My profile picture was succesfully changed")
    try:
        os.remove(photo)
    except Exception as e:
        logger.warn(str(e))
