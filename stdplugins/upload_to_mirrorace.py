"""Upload local Files to Mirrors
Syntax:
."""

import aiohttp
import asyncio
import os
import time
from datetime import datetime
from uniborg.util import admin_cmd, progress


@borg.on(admin_cmd(pattern="mirrorace ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    required_file_name = None
    start = datetime.now()
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
            return False
        else:
            end = datetime.now()
            ms = (end - start).seconds
            required_file_name = downloaded_file_name
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        input_str = input_str.strip()
        if os.path.exists(input_str):
            end = datetime.now()
            ms = (end - start).seconds
            required_file_name = input_str
            await mone.edit("Found `{}` in {} seconds.".format(input_str, ms))
        else:
            await mone.edit("File Not found in local server. Give me a file path :((")
            return False
    logger.info(required_file_name)
    if required_file_name:
        # required_file_name will have the full path
        file_name = os.path.basename(required_file_name)
        file_size = os.stat(required_file_name).st_size
        # /* STEP 1: get upload_key */
        step_one_url = "https://mirrorace.com/api/v1/file/upload"
        step_one_auth_params = {
            "api_key": Config.MIRROR_ACE_API_KEY,
            "api_token": Config.MIRROR_ACE_API_TOKEN
        }
        async with aiohttp.ClientSession() as session:
            resp = await session.post(step_one_url, data=step_one_auth_params)
            print(resp.status)
            if resp.status == 200:
                step_one_response_json = await resp.json()
                print(step_one_response_json)
                if step_one_response_json["status"] == "success":
                    # /* STEP 2: Upload file */
                    # step one: response vars
                    step_two_upload_url = step_one_response_json["result"]["server_file"]
                    cTracker = step_one_response_json["result"]["cTracker"]
                    upload_key = step_one_response_json["result"]["upload_key"]
                    default_mirrors = step_one_response_json["result"]["default_mirrors"]
                    max_chunk_size = step_one_response_json["result"]["max_chunk_size"]
                    max_file_size = step_one_response_json["result"]["max_file_size"]
                    max_mirrors = step_one_response_json["result"]["max_mirrors"]

                    # check file size limit
                    if int(file_size) >= int(max_file_size):
                        await mone.edit(f"File exceeds maximum file size allowed: {max_file_size}")
                        return False

                    # step two: setup
                    mirrors = default_mirrors
                    chunk_size = int(max_chunk_size)
                    chunks = (file_size // chunk_size) + \
                        (file_size % chunk_size)

                    # //range vars //for multi chunk upload
                    last_range = False
                    response = False
                    i = 0
                    while_error = False

                    with open(required_file_name, "rb") as f_handle:
                        # start chunk upload
                        for chunk in iter((lambda: f_handle.read(chunk_size)), ""):
                            # for chunk in f_handle.read(chunk_size):
                            # print(chunk)
                            # while (i < chunks) and not while_error:
                            # chunk = f_handle.read(chunk_size)
                            if not chunk:
                                break
                            range_start = 0
                            range_end = min(chunk_size, file_size - 1)

                            if last_range:
                                range_start = last_range + 1
                                range_end = min(
                                    range_start + chunk_size, file_size - 1)
                            last_range = range_end

                            allowed_mirrors = {}
                            w = 0
                            for mirror in mirrors:
                                if w >= 25:
                                    break
                                allowed_mirrors["mirrors[]"] = mirror
                                w = w + 1
                            w = None

                            step_two_params = {
                                "api_key": Config.MIRROR_ACE_API_KEY,
                                "api_token": Config.MIRROR_ACE_API_TOKEN,
                                "cTracker": cTracker,
                                "upload_key": upload_key,
                                # "mirrors": allowed_mirrors,
                                # //these required vars will be added by buildMultiPartRequest function
                                # //'files' => $file,
                                # //'mirrors[1]' => 1,
                                # //'mirrors[2]' => 2,
                            }

                            range_value = range_start - range_end / file_size
                            ra_nge = f"bytes {range_value}"

                            my_boundary = "some-de-limited-boundary"

                            with aiohttp.MultipartWriter("mixed") as mpwriter:
                                with aiohttp.MultipartWriter("related") as subwriter:
                                    for k, v in step_two_params.items():
                                        part = subwriter.append(v)
                                        part.set_content_disposition("form-data", name=k)
                                    for k, v in allowed_mirrors.items():
                                        part = subwriter.append(v)
                                        part.set_content_disposition("form-data", name=k)
                                mpwriter.append(subwriter)
                                with aiohttp.MultipartWriter("related") as subwriter:
                                    subwriter.append(chunk, {
                                                     "name": "files",
                                                     "filename": file_name,
                                                     "Content-Type": "multipart/form-data"
                                                     })
                                mpwriter.append(subwriter)
                            logger.info(mpwriter)
                            response = await session.post(step_two_upload_url,  data=mpwriter)
                            logger.info(await response.json())

                    logger.info(await response.json())
