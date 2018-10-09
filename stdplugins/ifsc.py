from telethon import events
import asyncio
import requests


@borg.on(events.NewMessage(pattern=r"\.ifsc rp (.*)"))
@borg.on(events.MessageEdited(pattern=r"\.ifsc rp (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://ifsc.razorpay.com/{}".format(input_str)
    r = requests.get(url).content
    await event.edit(r)
