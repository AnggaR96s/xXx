"""Take screenshot of any website
Syntax: .screencapture <Website URL>"""

import io
import os
import requests
from selenium import webdriver
from telethon import events
from uniborg.util import admin_cmd


@borg.on(admin_cmd(r"\.screencapture (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if Config.SCREEN_SHOT_LAYER_ACCESS_KEY is None:
        await event.edit("Need to get an API key from https://screenshotlayer.com/product \nModule stopping!")
        return
    await event.edit("Processing ...")
    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"
    input_str = event.pattern_match.group(1)
    response_api = requests.get(sample_url.format(
        Config.SCREEN_SHOT_LAYER_ACCESS_KEY,
        input_str,
        "1",
        "2560x1440",
        "PNG",
        "1"
    ))
    # https://stackoverflow.com/a/23718458/4723940
    contentType = response_api.headers['content-type']
    if "image" in contentType:
        with io.BytesIO(response_api.content) as screenshot_image:
            screenshot_image.name = "screencapture.png"
            try:
                await borg.send_file(
                    event.chat_id,
                    screenshot_image,
                    caption=input_str,
                    force_document=True,
                    reply_to=event.message.reply_to_msg_id
                )
                await event.delete()
            except Exception as e:
                await event.edit(str(e))
    else:
        await event.edit(response_api.text)


@borg.on(admin_cmd(r"\.screen (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    save_name = Config.TMP_DOWNLOAD_DIRECTORY + "/screen.png"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--test-type")
        chrome_bin = os.environ.get("GOOGLE_CHROME_SHIM", None)
        options.binary_location = chrome_bin
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(input_str)
        driver.save_screenshot(save_name)
        driver.close()
    except Exception as e:
        await event.edit(str(e))
    else:
        if os.path.exists(save_name):
            await borg.send_file(
                event.chat_id,
                save_name,
                caption=input_str,
                force_document=True,
                reply_to=event.message.reply_to_msg_id
            )
            os.remove(save_name)
