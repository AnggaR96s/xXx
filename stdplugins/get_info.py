# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
import os
from telethon.tl.types import MessageEntityMentionName


current_date_time = "./../DOWNLOADS/"


@borg.on(events.NewMessage(pattern=".get_info (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(current_date_time):
        os.makedirs(current_date_time)
    replied_user = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await borg(GetFullUserRequest(previous_message.from_id))
    else:
        input_str = event.pattern_match.group(1)
        mention_entity = event.message.entities
        if len(mention_entity) > 0:
            probable_user_mention_entity = mention_entity[0]
            if type(probable_user_mention_entity) == MessageEntityMentionName:
                user_id = probable_user_mention_entity.user_id
                replied_user = await borg(GetFullUserRequest(user_id))
            else:
                # the disgusting CRAP way, of doing the thing
                user_object = await borg.get_entity(input_str)
                user_id = user_object.id
                replied_user = await borg(GetFullUserRequest(user_id))
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    user_bio = replied_user.about
    photo = await borg.download_profile_photo(
        user_id,
        current_date_time,
        download_big=True
    )
    caption = "ID: {} \nName: [{}](tg://user?id={}) \nBio: {}".format(user_id, first_name, user_id, user_bio)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await borg.send_file(
        event.chat_id,
        photo,
        caption=caption,
        force_document=False,
        reply_to=message_id_to_reply
    )
    os.remove(photo)
    await event.delete()
