## [@SpEcHlDe](https://telegram.dog/ShrimadhaVahdamirhS)

- Only two of the environment variables are mandatory.
- This is because of `telethon.errors.rpc_error_list.ApiIdPublishedFloodError`
    - `APP_ID`:   You can get this value from https://my.telegram.org
    - `API_HASH`:   You can get this value from https://my.telegram.org
- The userbot will work without setting the non-mandatory environment variables.
- Please report any issues to the support group: [@SpEcHlDe](https://telegram.dog/ShrimadhaVahdamirhS)


## design

The modular design of the project enhances your Telegram experience
through [plugins](https://github.com/uniborg/uniborg/tree/master/stdplugins)
which you can enable or disable on demand.

Each plugin gets the `borg`, `logger` and `storage` magical
[variables](https://gitlab.com/SpEcHiDe/UniBorg/blob/4805f2f6de7d734c341bb978318f44323ad525f1/uniborg/uniborg.py#L66-L68)
to ease their use. Thus creating a plugin as easy as adding
a new file under the plugin directory to do the job:

```python
# stdplugins/myplugin.py
from telethon import events

@borg.on(events.NewMessage(pattern='hi'))
async def handler(event):
    await event.reply('hey')
```


## learning

Check out the already-mentioned
[plugins](https://gitlab.com/SpEcHiDe/UniBorg/tree/master/stdplugins)
directory to learn how to write your own, and consider reading
[Telethon's documentation](http://telethon.readthedocs.io/).
