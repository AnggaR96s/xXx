import sys 
import psutil 
import cpuinfo
from telethon import events, functions, __version__ 
from telethon.utils import get_input_location
from datetime import datetime, timedelta
from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="helpme", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    help_string = """@UniBorg
Python {}
Telethon {}

UserBot Forked from https://github.com/expectocode/uniborg""".format(
        sys.version,
        __version__
    )
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER  # pylint:disable=E0602
    if tgbotusername is not None:
        results = await borg.inline_query(  # pylint:disable=E0602
            tgbotusername,
            help_string
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.reply(help_string)
        await event.delete()


@borg.on(admin_cmd(pattern="dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())  # pylint:disable=E0602
    await event.edit(result.stringify())


@borg.on(admin_cmd(pattern="config"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetConfigRequest())  # pylint:disable=E0602
    result = result.stringify()
    logger.info(result)  # pylint:disable=E0602
    await event.edit("""Telethon UserBot powered by @UniBorg""")

@borg.on(admin_cmd("start")) 
async def _(event):
    if event.fwd_from:
        return 
    start = datetime.now()
    await event.edit("```collecting info!```")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    with open('/proc/uptime', 'r') as f: 
        uptime_seconds = float(f.readline().split()[0]) 
        uptime_string = str(timedelta(seconds = uptime_seconds))
        cpu = cpuinfo.get_cpu_info()['brand'] #psutil.cpu_freq(percpu=False)
        d = psutil.disk_usage('/')
    start_string = """
    ```Status :``` Online
PING:  ```{}```ms
```Dc : 5 IE``` 
```Python : {}
Telethon : {}``` 
```Plugins :``` {}
```Uptime :``` {} 
```Cpuinfo :``` {}
```Disk_usage :``` {}/100
[Shiva, Shiva, Shiva Shambho!!!](https://telegra.ph//file/f39b50eb06577ca400274.mp4)""".format(ms,
        sys.version,
        __version__,len(borg._plugins),uptime_string,cpu,d.percent)
    await event.edit(start_string,link_preview=True)
