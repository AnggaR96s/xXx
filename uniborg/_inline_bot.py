#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
import re
from telethon import events, custom


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


if Config.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        if event.query.user_id == borg.uid:
            logger.info(event.stringify())
            query = event.text
            rev_text = query[::-1]
            if query.startswith("ping"):
                ping_place_rs = query.split(" ")[1]
                result = builder.article(
                    "© @UniBorg",
                    text="Pong\n{}".format(ping_place_rs),
                    buttons=[
                        [custom.Button.url("Join the Channel", "https://telegram.dog/UniBorg"), custom.Button.url("Join the Group", "https://telegram.dog/ShrimadhaVahdamirhS")],
                        [custom.Button.url("Source Code", "https://GitLab.com/SpEcHiDe/UniBorg")]
                    ],
                    link_preview=False
                )
            elif "@UniBorg" in query:
                buttons = []
                same_row_buttons = []
                i = 1
                for plugin in borg._plugins:
                    helpable_plugin = not plugin.startswith("_")
                    if helpable_plugin:
                        same_row_buttons.append(
                            custom.Button.inline(
                                "{} {}".format("✅", plugin),
                                data="ub_plugin_{}".format(plugin)
                            )
                        )
                    if (i % 3) == 0:
                        buttons.append(same_row_buttons)
                        same_row_buttons = []
                    if helpable_plugin:
                        i = i + 1
                result = builder.article(
                    "© @UniBorg",
                    text="{}\nCurrently Loaded Plugins: {}".format(query, len(borg._plugins)),
                    buttons=buttons,
                    link_preview=False
                )
            else:
                result = builder.article(
                    "© @UniBorg",
                    text=query,
                    buttons=[
                        [custom.Button.url("Join the Channel", "https://telegram.dog/UniBorg"), custom.Button.url("Join the Group", "https://telegram.dog/ShrimadhaVahdamirhS")],
                        [custom.Button.url("Source Code", "https://GitLab.com/SpEcHiDe/UniBorg")]
                    ],
                    link_preview=False
                )
        else:
            result = builder.article(
                "© @UniBorg",
                text="""Try @UniBorg
You can log-in as Bot or User and do many cool things with your Telegram account.

All instaructions to run @UniBorg in your PC has been explained in https://t.me/UniBorg/4""",
                buttons=[
                    [custom.Button.url("Join the Channel", "https://telegram.dog/UniBorg"), custom.Button.url("Join the Group", "https://telegram.dog/ShrimadhaVahdamirhS")],
                    [custom.Button.url("Source Code", "https://GitLab.com/SpEcHiDe/UniBorg")]
                ],
                link_preview=False
            )
        await event.answer([result] if result else None)


    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ub_plugin_(.*)")))
    async def on_plug_in_callback_query_handler(event):
        plugin_name = event.data_match.group(1).decode("UTF-8")
        help_string = borg._plugins[plugin_name].__doc__
        reply_pop_up_alert = help_string if help_string is not None else "No DOCSTRING has been setup for {} plugin".format(plugin_name)
        reply_pop_up_alert += "\n\n Use .unload {} to remove this plugin from the loaded plugins\n© @UniBorg".format(plugin_name)
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
