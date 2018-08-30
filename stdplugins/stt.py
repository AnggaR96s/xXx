from telethon import events
import requests
import os
from datetime import datetime


current_date_time = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./../DOWNLOADS/")
IBM_WATSON_CRED_USERNAME = os.environ.get("IBM_WATSON_CRED_USERNAME", None)
IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)


@borg.on(events.NewMessage(pattern=r"\.stt (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("Downloading to my local, for analysis 🙇")
    start = datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await borg.download_media(
            previous_message,
            current_date_time
        )
        lan = input_str
        if IBM_WATSON_CRED_USERNAME is None or IBM_WATSON_CRED_PASSWORD is None:
            await event.edit("You need to set the required ENV variables for this module. \nModule stopping")
        else:
            await event.edit("Starting analysis, using IBM WatSon Speech To Text")
            headers = {
                "Content-Type": "audio/ogg",
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize",
                headers=headers,
                data=data,
                auth=(IBM_WATSON_CRED_USERNAME, IBM_WATSON_CRED_PASSWORD)
            )
            r = response.json()
            # process the json to appropriate string format
            results = r["results"]
            alternatives = results[0]["alternatives"][0]
            # take the 0th element, because it is assumed to have maximum confidence
            transcript_response = alternatives["transcript"]
            transcript_confidence = alternatives["confidence"]
            end = datetime.now()
            ms = (end - start).seconds
            string_to_show = "Language: `{}`\nTRANSCRIPT: `{}`\nTime Taken: {} seconds\nConfidence: `{}`".format(lan, transcript_response, ms, transcript_confidence)
            await event.edit(string_to_show)
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await event.edit("I do not know what to do with this message.")
