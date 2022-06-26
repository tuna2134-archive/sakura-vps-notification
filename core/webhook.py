from requests import Session


class Webhook:
    def __init__(self, id: str, token: str):
        self.session = Session()
        self.url = "https://discord.com/api/v10/webhooks/{}/{}".format(id, token)

    def request(self, method: str, path: str, **kwargs):
        r = self.session.request(method, self.url + path, **kwargs)
        r.raise_for_status()
        return r

    def send_message(
        self, content: str = None, *, embeds: list = None,
        username: str = None, avatar_url: str = None
    ):
        payload = {}
        if content is not None:
            payload["content"] = content
        if embeds is not None:
            payload["embeds"] = embeds
        if username is not None:
            payload["username"] = username
        if avatar_url is not None:
            payload["avatar_url"] = avatar_url
        self.request("POST", "", json=payload)