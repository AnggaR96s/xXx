# https://t.me/SnowballFight/257378
from telethon import events
from telethon.events import StopPropagation
@borg.on(events.NewMessage(chats=['@PublicTestGroup', '@SnowballFight', '@BotTalk']))
async def _(event):
  raise StopPropagation
