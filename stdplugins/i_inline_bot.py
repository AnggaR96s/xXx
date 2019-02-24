from telethon import events


@borg.on(events.NewMessage(pattern=r"\.ib (.[^ ]*) (.*)", outgoing=True))
async def _(event):
    # https://stackoverflow.com/a/35524254/4723940
    if event.fwd_from:
        return
    bot_username = event.pattern_match.group(1)
    search_query = event.pattern_match.group(2)
    try:
        output_message = ""
        bot_results = await borg.inline_query(bot_username, search_query)
        i = 0
        for result in bot_results:
            output_message += "{} {} `{}`\n\n".format(result.title, result.description, ".icb " + bot_username + " " + str(i + 1) + " " + search_query)
            i = i + 1
        await event.edit(output_message)
    except Exception as e:
        await event.edit("{} did not respond correctly, for **{}**!\n `{}`".format(bot_username, search_query, str(e)))


@borg.on(events.NewMessage(pattern=r"\.icb (.[^ ]*) (.[^ ]*) (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    bot_username = event.pattern_match.group(1)
    i_plus_oneth_result = event.pattern_match.group(2)
    search_query = event.pattern_match.group(3)
    try:
        bot_results = await borg.inline_query(bot_username, search_query)
        message = await bot_results[int(i_plus_oneth_result) - 1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
    except Exception as e:
        await event.edit(str(e))
