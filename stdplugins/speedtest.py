# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import subprocess
from datetime import datetime
import requests


@borg.on(events.NewMessage(pattern=r".speedtest", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Downloading speedtest-cli binary to my local ... Thus might take some time")
    url = "https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py"
    required_file_name = "./../DOWNLOADS/speedtest.cli"
    r = requests.get(url, stream=True)
    with open(required_file_name, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    await event.edit("Now executing python speedtest.py Please wait")
    command_to_run = "python3 {}".format(required_file_name)
    input_command = command_to_run.split(" ")
    output_str = None
    try:
        t_response = subprocess.check_output(input_command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        output_str = "process returned {}\n output: {}".format(exc.returncode, exc.output)
    else:
        x_reponse = t_response.decode("UTF-8")
        output_str = x_reponse
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("**SpeedTest** completed in {} seconds \n\n {}".format(ms, output_str))

