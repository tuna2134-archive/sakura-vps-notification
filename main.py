import requests
import yaml

import time
from datetime import datetime

from core import Webhook


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
webhook = Webhook(**config["webhook"])

while True:
    data = requests.get(
        "https://help.sakura.ad.jp/maint/api/v1/feeds/?service=vps&type=trouble&ordering=-event_start&limit=1000"
    ).json()
    last = data["results"][0]
    if last["url"] != config["last"]:
        when = datetime.fromtimestamp(int(last["event_start"]))
        embed = {
            "title": last["title"],
            "description": last["desc"],
            "url": last["url"],
            "timestamp": when.isoformat(),
        }
        if last["type"] == "trouble":
            embed["color"] = 0xff0000
        webhook.send_message(embeds=[embed], username=last["type"])
        config["last"] = last["url"]
        with open("config.yml", "w") as f:
            yaml.dump(config, f)
    time.sleep(60)