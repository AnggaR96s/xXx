# uniborg

Pluggable [``asyncio``](https://docs.python.org/3/library/asyncio.html)
[Telegram](https://telegram.org) userbot based on
[Telethon](https://github.com/LonamiWebs/Telethon).

## installing

#### The Easy Way

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### The Legacy Way

Simply clone the repository and run the main file:
```sh
git clone https://github.com/uniborg/uniborg.git
cd uniborg
pip install -r requirements.txt
pip install -r requirements-stdborg.txt
python3 -m stdborg stdborg
```

## internals

The core features offered by the custom `TelegramClient` live under the
[`uniborg/`](https://github.com/uniborg/uniborg/tree/master/uniborg)
directory, with some utilities, enhancements and the core plugin.
