# winbot
A Discord bot for interfacing with a QEMU VM.
> Fair warning, this branch is *very* buggy as it's pretty much a quick dirty port of the VirtualBox version to QEMU.

## Pre-Setup
1. Install [Python 3](https://www.python.org/downloads/).
2. Install [QEMU](https://www.qemu.org/download/).
3. Install [`discord.py`](https://pypi.org/project/discord.py/) and [`qemu.qmp`](https://pypi.org/project/qemu.qmp/).

## Setup
1. Run `main.py` once. It should generate a new file, `winbot.ini`.
2. Fill out `winbot.ini` with values of your choice. `token` is your Discord bot token, `prefix` is the bot's prefix, `channel_id` is the Text Channel ID of where the bot's startup message will be sent and `owner_id` is the User ID of the bot's owner.
3. Start a QEMU VM with `-qmp tcp:localhost:4444,server,nowait` appended to the end of its launch options.
5. Start the bot by running `main.py`.
6. Go nuts!
> Note: You can ignore `vm_name` safely as it is no longer needed, unless you are running multiple QMP enabled QEMU instances at once.

## Commands
```
  backspace   Really fuckin delete something.
  help        Shows this message.
  keys        Get a list of keys you can use with the 'press' command.
  mouse       Control the mouse.
  ping        Ping Pong!
  press       Send special keys to the VM.
  raw_command Send raw QEMU inputs.
  reload      Reload winbot's config file.
  reset       Reset the VM. Owner only.
  screen      Get a screenshot of the VM.
  type        Sends a long string of text to the VM, followed by a newline.
```

Run `help [command name]` for more info on each command.
