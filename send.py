import os
import requests
import click
import json


@click.group()
def main():
    pass


DEFAULT_CONFIG = {
    "homeserver": "https://YOUR_MATRIX_INSTANCE",
    "room_id": "YOUR_INTERNAL_ROOM_ID",
    "token_path": "~/.matrix_token",
}


@main.command()
@click.argument("message")
@click.option(
    "--room-id",
    help="Room ID to send message to",
    default=None,
)
@click.option("--config-path", help="Path to config file", default=None)
@click.option("--token-path", help="Path to token file", default=None)
def send(message, room_id, config_path, token_path):
    if config_path is None:
        config = DEFAULT_CONFIG
    else:
        with open(config_path, "r") as f:
            config = json.load(f)

    if room_id is not None:
        config["room_id"] = room_id

    if token_path is not None:
        config["token_path"] = token_path

    with open(os.path.expanduser(config["token_path"]), "r") as f:
        access_token = f.read().strip()

    url = f"{config['homeserver']}/_matrix/client/r0/rooms/{config['room_id']}/send/m.room.message/m_psend{os.getpid()}"

    matrix_message = {"msgtype": "m.text", "body": message}

    proxies = {
        "http": os.getenv("http_proxy"),
        "https": os.getenv("https_proxy"),
    }

    headers = {
        "authorization": f"Bearer {access_token}",
    }

    response = requests.put(url, headers=headers, json=matrix_message, proxies=proxies)

    if not response.status_code == 200:
        print(
            f"Failed to send message. Status code: {response.status_code}\n{response.text}"
        )


# TODO: can I send files as m.image/m.file message types? what's the encoding?

if __name__ == "__main__":
    main()