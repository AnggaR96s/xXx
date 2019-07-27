"""Take screenshot of any website
Syntax: .sc <Website URL>"""

import io
import traceback
from datetime import datetime
from selenium import webdriver
from telethon import events
from uniborg.util import admin_cmd


@borg.on(admin_cmd("sc (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if Config.GOOGLE_CHROME_BIN is None:
        await event.edit("need to install Google Chrome. Module Stopping.")
        return
    await event.edit("Processing ...")
    start = datetime.now()
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        options.binary_location = Config.GOOGLE_CHROME_BIN
        await event.edit("Starting Google Chrome BIN")
        driver = webdriver.Chrome(chrome_options=options)
        input_str = event.pattern_match.group(1)
        driver.get(input_str)
        await event.edit("Opening web-page")
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        driver.close()
        await event.edit("Stopping Google Chrome BIN")
        with io.BytesIO(im_png) as out_file:
            out_file.name = "@UniBorg.ScreenCapture.PNG"
            await borg.send_file(
                event.chat_id,
                out_file,
                caption=input_str,
                force_document=True,
                reply_to=event.message.reply_to_msg_id,
                allow_cache=False,
                silent=True
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(f"Completed screencapture Process in {ms} seconds")
    except Exception:
        await event.edit(traceback.format_exc())
