""" Powered by @Google
Available Commands:
.gs <query>
.gi image <query>
.grs reverse search"""

import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from google_images_download import google_images_download
from gsearch.googlesearch import search
from uniborg.util import admin_cmd


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@borg.on(admin_cmd("gs (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1) # + " -inurl:(htm|html|php|pls|txt) intitle:index.of \"last modified\" (mkv|mp4|avi|epub|pdf|mp3)"
    search_results = search(input_str, num_results=Config.GOOGLE_SEARCH_COUNT_LIMIT)
    output_str = " "
    for text, url in search_results:
        output_str += " 👉🏻  [{}]({}) \n\n".format(text, url)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("searched Google for {} in {} seconds. \n{}".format(input_str, ms, output_str), link_preview=False)
    await asyncio.sleep(5)
    await event.edit("Google: {}\n{}".format(input_str, output_str), link_preview=False)

@borg.on(admin_cmd("img (.*)"))
async def _(event):
    """ For .img command, search and return images matching the query. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("Processing...")
        query = event.pattern_match.group(1)
        try:
            lim = lim[0]
            lim = lim.replace("lim=", "")
            query = query.replace("lim=" + lim[0], "")
        except IndexError:
            lim = 2
        response = google_images_download.googleimagesdownload()

        # creating list of arguments
        arguments = {
            "keywords": query,
            "limit": lim,
            "format": "jpg",
            "no_directory": "no_directory"
        }

        # passing the arguments to the function
        paths = response.download(arguments)
        lst = paths[0][query]
        await event.client.send_file(await event.client.get_input_entity(event.chat_id), lst)
        os.remove(lst[0])
        os.remove(lst[1])
        os.rmdir(os.path.dirname(os.path.abspath(lst[0])))
        await event.delete()

@borg.on(admin_cmd("gi (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    response = google_images_download.googleimagesdownload()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    arguments = {
        "keywords": input_str,
        "limit": Config.TG_GLOBAL_ALBUM_LIMIT,
        "format": "jpg",
        "delay": 1,
        "safe_search": True,
        "output_directory": Config.TMP_DOWNLOAD_DIRECTORY
    }
    paths = response.download(arguments)
    lst = paths[input_str]
    await borg.send_file(
        event.chat_id,
        lst,
        caption=input_str,
        reply_to=event.message.id,
        progress_callback=progress
    )
    for each_file in lst:
        os.remove(each_file)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("searched Google for {} in {} seconds.".format(input_str, ms), link_preview=False)
    await asyncio.sleep(5)
    await event.delete()


@borg.on(admin_cmd("grs"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    BASE_URL = "http://www.google.com"
    OUTPUT_STR = "Reply to an image to do Google Reverse Search"
    if event.reply_to_msg_id:
        await event.edit("Pre Processing Media")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (downloaded_file_name, open(downloaded_file_name, "rb")),
                "image_content": ""
            }
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = requests.post(SEARCH_URL, files=multipart, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await event.edit("Found Google Result. Pouring some soup on it!")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # document.getElementsByClassName("r5a77d"): PRS
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = BASE_URL + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        # document.getElementById("jHnbRc")
        img_size_div = soup.find(id="jHnbRc")
        img_size = img_size_div.find_all("div")
        end = datetime.now()
        ms = (end - start).seconds
        OUTPUT_STR = """{img_size}
**Possible Related Search**: <a href="{prs_url}">{prs_text}</a>

More Info: Open this <a href="{the_location}">Link</a> in {ms} seconds""".format(**locals())
    await event.edit(OUTPUT_STR, parse_mode="HTML", link_preview=False)
