# matrix bot

I created this bot to send messages via matrix when long running tasks are finished. It is written in python but uses the REST API directly using requests.

## Installation

This package provides a `setup.py` file. You can install it via `pip install .` or `python setup.py install`.
Doing this without a virtual environment will install the package globally.

If you use `pipx` you can install it via `pipx install .`.
It should create terminal commands for you to use.

## Configuration

- homeserver: "https://YOUR_MATRIX_INSTANCE",
    This is the URL of your matrix instance.
- room_id: "YOUR_INTERNAL_ROOM_ID",
    This is the internal room id of the room you want to send messages to.
    In element, you can find this in the room settings under advanced.
- token_path: "~/.matrix_token",
    This is the path to the file where the your authentication token is stored.
    In element, you can find it under your user settings under help & about, all the way at the bottom.

You can store these values in a configuration json file and pass it to the bot via the `--config-path` flag.