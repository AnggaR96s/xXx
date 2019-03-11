from telethon import events, functions, __version__
import sys


@borg.on(events.NewMessage(pattern=r"\.helpme", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("""@UniBorg
Python {}
Telethon {}

UserBot Forked from https://github.com/expectocode/uniborg""".format(
        sys.version,
        __version__
    ))


@borg.on(events.NewMessage(pattern=r"\.dc", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())
    await event.edit(result.stringify())


@borg.on(events.NewMessage(pattern=r"\.config", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetConfigRequest())
    result = result.stringify()
    logger.info(result)
    await event.edit("""Telethon UserBot powered by @UniBorg""")
