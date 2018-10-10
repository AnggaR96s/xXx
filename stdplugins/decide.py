from telethon import events
import requests


@borg.on(events.NewMessage(pattern=r"\.decide", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    r = requests.get("https://yesno.wtf/api").json()
    await event.edit("[{}]({})".format(r["answer"], r["image"]))

