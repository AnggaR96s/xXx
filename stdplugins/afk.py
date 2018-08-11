# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import os
import time


global ISAFK
ISAFK=False
global AFKREASON
AFKREASON="No Reason"
global USERS
USERS={}
global COUNT_MSG
COUNT_MSG=0
global PRIVATE_GROUP_BOT_API_ID
PRIVATE_GROUP_BOT_API_ID = os.environ.get("PRIVATE_GROUP_BOT_API_ID")


@borg.on(events.NewMessage(incoming=True))
async def _(event):
    global PRIVATE_GROUP_BOT_API_ID
    if not PRIVATE_GROUP_BOT_API_ID:
        await event.edit("This functionality will not work")
        return
    PRIVATE_GROUP_BOT_API_ID = int(PRIVATE_GROUP_BOT_API_ID)
    global COUNT_MSG
    global USERS
    global ISAFK
    global AFKREASON
    if event.message.mentioned or event.is_private:
        if ISAFK:
            if event.sender:
                if event.sender.username not in USERS:
                    USERS.update({event.sender.username:1})
                    COUNT_MSG=COUNT_MSG+1
                    await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soon😉.Meanwhile you can play around with his AI. **This message shall be self destructed in 5 seconds**")
                    time.sleep(5)
                    i=1
                    async for message in borg.iter_messages(event.chat_id,from_user='me'):
                        if i>1:
                            break
                        i=i+1
                        await message.delete()
            else:
                USERS.update({event.chat_id:1})
                COUNT_MSG=COUNT_MSG+1
                await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soon😉. Meanwhile you can play around with his AI. **This message shall be self destructed in 5 seconds**")
                time.sleep(5)
                i=1
                async for message in borg.iter_messages(event.chat_id,from_user='me'):
                    if i>1:
                        break
                    i=i+1
                    await message.delete()


@borg.on(events.NewMessage(outgoing=True, pattern=r'.iamafk (.*)'))
async def _(event):
    global PRIVATE_GROUP_BOT_API_ID
    if not PRIVATE_GROUP_BOT_API_ID:
        await event.edit("This functionality will not work")
        return
    PRIVATE_GROUP_BOT_API_ID = int(PRIVATE_GROUP_BOT_API_ID)
    if event.fwd_from:
        return
    string = event.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    ISAFK = True
    await event.edit("I am now AFK!")
    if string != "":
        AFKREASON = string


@borg.on(events.NewMessage(outgoing=True, pattern='.notafk'))
async def _(event):
    global PRIVATE_GROUP_BOT_API_ID
    if not PRIVATE_GROUP_BOT_API_ID:
        await event.edit("This functionality will not work")
        return
    PRIVATE_GROUP_BOT_API_ID = int(PRIVATE_GROUP_BOT_API_ID)
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    ISAFK=False
    await event.edit("I have returned from AFK mode.")
    await event.respond("```You had recieved "+str(COUNT_MSG)+" messages while you were away. Check log for more details. This auto-generated message shall be self destructed in 2 seconds.```")
    time.sleep(2)
    i=1
    async for message in borg.iter_messages(event.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
    await borg.send_message(PRIVATE_GROUP_BOT_API_ID, "You had recieved "+str(COUNT_MSG)+" messages from "+str(len(USERS))+" chats while you were away")
    for i in USERS:
        await borg.send_message(PRIVATE_GROUP_BOT_API_ID,str(i)+" sent you "+"```"+str(USERS[i])+" messages```")
    COUNT_MSG=0
    USERS={}
    AFKREASON="No reason"
