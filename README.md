# winbot
A Discord bot for interfacing with a VirtualBox VM.

## Pre-Setup
1. Install Python 3.8. (If you're able to use `discord.py` with your version of Python 3.9, feel free to use 3.9.)
2. Install VirtualBox.
3. Install `discord.py` and `pywin32` (or your COM library of choice for your platform)
4. Install `virtualbox` by following the instructions at [pypi](https://pypi.org/project/virtualbox/).

## Setup
1. Run `main.py` once. It should generate a new file, `winbot.ini`.
2. Fill out `winbot.ini` with values of your choice. `token` is your Discord bot token, `prefix` is the bot's prefix, `vm_name` is the name of the VM that will be used for the bot, `channel_id` is where the startup message will be sent, and `owner_id` is the ID of the bot owner.
3. Open VirtualBox and create a VM with the same name you used for `vm_name` (if it doesn't already exist.
4. Start the VM through VirtualBox.
5. Start the bot by running `main.py`.
6. Go nuts!

## Commands
```
  help   Shows this message
  keys   Get a list of keys you can use with press
  mouse  Do mouse shit.
  ping   Ping Pong!
  press  Send special keys to the VM.
  reload Reload the bot config files.
  reset  Reset the VM. Owner only.
  screen Get a screenshot of the VM.
  type   Sends a long string of text to the VM, followed by a newline.
```

Run `help [command name]` for more info on each command.
