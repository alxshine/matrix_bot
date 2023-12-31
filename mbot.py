# %%
import os
import requests
import click
import json
import sys


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


@main.command()
@click.option("--config-path", help="Path to config file", default=None)
def generate_config(config_path):
    if config_path is not None:
        f = open(config_path, "w")
    else:
        f = sys.stdout

    json.dump(DEFAULT_CONFIG, f, indent=4)



@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--room-id",
    help="Room ID to send message to",
    default=None,
)
@click.option("--config-path", help="Path to config file", default=None)
@click.option("--token-path", help="Path to token file", default=None)
def upload(file_path, room_id=None, config_path=None, token_path=None):
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

    # upload file
    filename = os.path.basename(file_path)
    url = f"{config['homeserver']}/_matrix/media/r0/upload?filename={filename}"
    response = requests.post(
        url,
        headers={"authorization": f"Bearer {access_token}"},
        files={"file": open(file_path, "rb")},
    )

    if not response.status_code == 200:
        print(
            f"Failed to upload file. Status code: {response.status_code}\n{response.text}"
        )

    json_response = response.json()
    content_uri = json_response["content_uri"]

    # send message
    message_dict = {"body": filename, "msgtype": "m.file", "url": content_uri}

    url = f"{config['homeserver']}/_matrix/client/r0/rooms/{config['room_id']}/send/m.room.message/m{os.getpid()}"
    message_response = requests.put(
        url, headers={"authorization": f"Bearer {access_token}"}, json=message_dict
    )

    if not message_response.status_code == 200:
        print(
            f"Failed to send message. Status code: {message_response.status_code}\n{message_response.text}"
        )


if __name__ == "__main__":
    main()
