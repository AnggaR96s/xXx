from telethon import events
import os
from datetime import datetime
import requests
import json

SECRET_NSFW_CHECKER_KEY = os.environ.get("NSFW_CHECKER_KEY", None)


@borg.on(events.NewMessage(pattern=r".nsfw check (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if SECRET_NSFW_CHECKER_KEY is None:
        await event.edit("You need to set the required keys in the app.json! This module will not work. Quitting.")
        return
    permanent_url = event.pattern_match.group(1)
    check_nsfw_url = "https://spechide.shrimadhavuk.me/functions/nsfw.php?q={}&Q={}".format(SECRET_NSFW_CHECKER_KEY, permanent_url)
    r = requests.get(check_nsfw_url).text
    s = json.loads(r)
    if s["R"]["status"] == "success":
        safe_probability = s["R"]["nudity"]["safe"]
        await event.edit("The image is considered to be safe with probability: {}".format(safe_probability))
    else:
        await event.delete()



