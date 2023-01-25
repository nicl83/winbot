# import discord, sys, asyncio, traceback
import discord
import sys
import asyncio
import traceback
from qemu.qmp import QMPClient
import pathlib
import PIL.Image as Image

from discord.ext import commands
from configparser import ConfigParser as configparser

def load_config(config_file_name):
    config = configparser()
    try:
        with open(config_file_name, 'r') as w: #sanity check because configparser is stupid
            config.read(config_file_name)
        print("Config loaded succesfully!")

    except:
        print("Please add your token and other information to winbot.ini, then run the script again.")
        config['winbot'] = {}
        config['winbot']['token'] = 'SetMeUp'
        config['winbot']['prefix'] = 'vm!'
        config['winbot']['vm_name'] = 'Example'
        config['winbot']['owner_id'] = '12345'
        config['winbot']['channel_id'] = '67890'
        with open(config_file_name, 'w') as f:
            config.write(f)
        sys.exit(1)
        
    if config['winbot']['token'] == 'SetMeUp' or len(config['winbot']['token']) < 8:
        print("winbot.ini contains invalid data. Winbot will now terminate.")
        sys.exit(1)
    else:
        return_config = []
        return_config.append(config['winbot']['token'])
        return_config.append(config['winbot']['prefix'])
        return_config.append(config['winbot']['vm_name'])
        return_config.append(int(config['winbot']['owner_id']))
        return_config.append(int(config['winbot']['channel_id']))
        return return_config

config_file = "winbot.ini"
token, prefix, vm_name, owner_id, channel_id = load_config(config_file)

print(f"Prefix: {prefix}")
print(f"VM name: {vm_name}")
print(f"Owner ID: {owner_id}")
print(f"Channel ID: {channel_id}")

bgrfix = (
 0, 0, 1, 0,
 0, 1, 0, 0,
 1, 0, 0, 0
)
def fiximage(filename="temp.png"):
    with Image.open(filename) as image:
        im_converted = image.convert("RGB").convert(mode="RGB",matrix=bgrfix)
    im_converted.convert(mode="RGBA").save(filename)

qemu_keys = ['unmapped', 'pause', 'ro', 'kp_comma', 'kp_equals', 'power', 'hiragana', 'henkan', 'yen', 'sleep', 'wake', 'audionext', 'audioprev', 'audiostop', 'audioplay', 'audiomute', 'volumeup', 'volumedown', 'mediaselect', 'mail', 'calculator', 'computer', 'ac_home', 'ac_back', 'ac_forward', 'ac_refresh', 'ac_bookmarks', 'muhenkan', 'katakanahiragana', 'lang1', 'lang2', 'shift', 'shift_r', 'alt', 'alt_r', 'ctrl', 'ctrl_r', 'menu', 'esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'minus', 'equal', 'backspace', 'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'bracket_left', 'bracket_right', 'ret', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'semicolon', 'apostrophe', 'grave_accent', 'backslash', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma', 'dot', 'slash', 'asterisk', 'spc', 'caps_lock', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'num_lock', 'scroll_lock', 'kp_divide', 'kp_multiply', 'kp_subtract', 'kp_add', 'kp_enter', 'kp_decimal', 'sysrq', 'kp_0', 'kp_1', 'kp_2', 'kp_3', 'kp_4', 'kp_5', 'kp_6', 'kp_7', 'kp_8', 'kp_9', 'less', 'f11', 'f12', 'print', 'home', 'pgup', 'pgdn', 'end', 'left', 'up', 'down', 'right', 'insert', 'delete', 'stop', 'again', 'props', 'undo', 'front', 'copy', 'open', 'paste', 'find', 'cut', 'lf', 'help', 'meta_l', 'meta_r', 'compose']

qemu_aliases = { # Designed for en-GB, YMMV
    ' ': 'spc',
    'win': 'meta_l',
    'cmd': 'meta_l',
    'opt': 'alt',
    'space': 'spc',
    'enter': 'ret',
    '.': 'dot',
    'failtest': 451,
    '?': ['shift', 'slash'],
    '/': 'slash',
    ':': ['shift', 'semicolon'],
    '!': ['shift', '1'],
    '"': ['shift', '2'],
    '$': ['shift', '4'],
    '%': ['shift', '5'],
    '&': ['shift', '7'],
    "'": 'apostrophe',
    '(': ['shift', '9'],
    ')': ['shift', '0'],
    '*': 'asterisk',
    '+': ['shift', 'equal'],
    ',': 'comma',
    '-': 'minus',
    '.': 'dot',
    '/': 'slash',
    ':': ['shift', 'semicolon'],
    ';': 'semicolon',
    '<': ['shift', 'comma'],
    '=': 'equal',
    '>': ['shift', 'dot'],
    '?': ['shift', 'slash'],
    '@': ['shift', 'apostrophe'],
    '[': 'bracket_left',
    '\\': 'backslash',
    ']': 'bracket_right',
    '^': ['shift', '6'],
    '_': ['shift', 'minus'],
    '`': 'grave_accent',
    '{': ['shift', 'bracket_left'],
    '|': ['shift', 'backslash'],
    '}': ['shift', 'bracket_right'],
    '£': ['shift', '3'],
    '¬': ['shift', 'grave_accent']
}

intents = discord.Intents(messages=True, guilds=True, message_content=True)
bot = commands.Bot(command_prefix = prefix, intents = intents, owner_id=owner_id)
mouse_state = dict()

vm_session = QMPClient(vm_name)

async def send_key(key_names: list[str], session=vm_session):
    """Send keys to the VM. Wrapper around QMP 'send-key' command.
    Assumes you know what you're doing already, will not error handle."""
    await session.execute(
        cmd="send-key",
        arguments={"keys": [
            {"type": "qcode", "data": key} for key in key_names
        ]}
    )


@bot.event
async def on_ready():
    global vm_session
    await vm_session.connect(('127.0.0.1', 4444))
    await get_vm_screenshot(vm_session, 'temp.png')
    channel = bot.get_channel(channel_id)
    await channel.send('Winbot has started! Current VM state:', file=discord.File('temp.png')) # type: ignore

@bot.event
async def on_command_error(ctx, exception):
    tb_data = ''.join(traceback.format_tb(exception.__traceback__))
    await ctx.send(f"Sorry, an error occurred.\n```\n{repr(exception)}\n{tb_data}\n```")

#Ping pong!
@bot.command()
async def ping(ctx):
    """Ping Pong!
    
    If the bot is alive, it will reply with "Pong!\""""
    await ctx.send('Pong!')

#Get image of VM
async def get_vm_screenshot(vm_sesh: QMPClient, file_name: str):
    screenshot_path = (pathlib.Path(__file__).parent/file_name).resolve()
    await vm_sesh.execute(
        cmd="screendump",
        arguments={
            "filename": str(screenshot_path),
            "format": "png"
        }
    )
    fiximage(str(screenshot_path))


@bot.command()
async def screen(ctx):
    """Get a screenshot of the VM."""
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Say cheese!', file=discord.File('temp.png'))

#Send long string or normal chars to VM
@bot.command(name='type')
async def bot_type(ctx, *, arg: str):
    """Sends a long string of text to the VM, followed by a newline."""
    global vm_session
    for key in arg:
        if key.lower() not in qemu_keys:
            if key in qemu_aliases.keys():
                if type(qemu_aliases[key]) == str:
                    await send_key([qemu_aliases[key]])
                elif type(qemu_aliases[key]) == list:
                    await send_key(qemu_aliases[key])
                else:
                    await ctx.send(f"secret third thing error: {qemu_aliases[key]}")
            else:    
                await ctx.send(f"Unkown key: {key}")
                await asyncio.sleep(0.1)
        elif key.isupper():
            await send_key(["shift", key.lower()])
        else:
            await send_key([key])
    await send_key(["ret"])
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Send special buttons to the VM
def release_special_keys(key_session):
    release_codes = [0x9d, 0xaa, 0xb8, 0xb6]
    key_session.console.keyboard.put_scancodes(release_codes)

@bot.command()
async def press(ctx, *args):
    """Send special keys to the VM.
    
    Get a list of valid keys with vb!keys. Also accepts a sequence of keys."""
    global vm_session
    key_name_list = []
    for key in args:
        key = key.lower() # discard case sensitivity
        if key not in qemu_keys:
            if key in qemu_aliases.keys():
                if type(qemu_aliases[key]) == str:
                    key_name_list.append(qemu_aliases[key])
                elif type(qemu_aliases[key]) == list:
                    key_name_list.extend(qemu_aliases[key])
                else:
                    await ctx.send(f"secret third thing error: {qemu_aliases[key]}")
            else:    
                await ctx.send(f"Unkown key: {key}")
                await asyncio.sleep(0.1)
        else:
            key_name_list.append(key)
    await send_key(key_name_list)
    # release_special_keys(vm_session)
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

@bot.command()
async def backspace(ctx, count):
    "Really fuckin delete something"
    global vm_session
    try:
        count = int(count)
    except:
        await ctx.send("gotta be a number")
        return
    for x in range(0,count):
        await send_key(["backspace"])
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Send a mouse command
@bot.group()
async def mouse(ctx):       
    if ctx.invoked_subcommand is None:
        await ctx.send(f"Unknown mouse command, do {prefix}help mouse for valid commands!")

#Click the mouse
@mouse.command()
async def click(ctx, *args):
    global vm_session
    await vm_session.execute(
        cmd="input-send-event",
        arguments={

            "events": [
                {"type": "btn", "data": { "down": True, "button": "left" } }
            ]
        }
    )
    await vm_session.execute(
        cmd="input-send-event",
        arguments={
            "events": [
                {"type": "btn", "data": { "down": False, "button": "left" } }
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Click and hold the mouse
@mouse.command()
async def clickhold(ctx, *args):
    global vm_session
    await vm_session.execute(
        cmd="input-send-event",
        arguments={

            "events": [
                {"type": "btn", "data": { "down": True, "button": "left" } }
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Right click the mouse.
@mouse.command()    
async def rclick(ctx, *args):
    global vm_session
    await vm_session.execute(
        cmd="input-send-event",
        arguments={

            "events": [
                {"type": "btn", "data": { "down": True, "button": "right" } }
            ]
        }
    )
    await vm_session.execute(
        cmd="input-send-event",
        arguments={

            "events": [
                {"type": "btn", "data": { "down": False, "button": "right" } }
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Right click and hold the mouse.
@mouse.command()
async def rclickhold(ctx, *args):
    global vm_session
    await vm_session.execute(
        cmd="input-send-event",
        arguments={

            "events": [
                {"type": "btn", "data": { "down": True, "button": "right" } }
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Stop holding any mouse buttons (reset state to 0).
@mouse.command()
async def release(ctx, *args):
    global vm_session
    await vm_session.execute(
        cmd="input-send-event",
        arguments={

            "events": [
                {"type": "btn", "data": { "down": False, "button": "left" } },
                {"type": "btn", "data": { "down": False, "button": "right" } }
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse right (+X).
@mouse.command()
async def right(ctx, pixels):
    global vm_session
    pixels = int(pixels)
    await vm_session.execute(
        cmd="input-send-event",
        arguments={
            "events": [
                {"type": "rel", "data": {"axis": "x", "value": pixels}}
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse left (-X).
@mouse.command()
async def left(ctx, pixels):    
    global vm_session
    pixels = int(pixels)
    await vm_session.execute(
        cmd="input-send-event",
        arguments={
            "events": [
                {"type": "rel", "data": {"axis": "x", "value": 0-pixels}}
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse down (+Y).
@mouse.command()
async def down(ctx, pixels):
    global vm_session
    pixels = int(pixels)
    await vm_session.execute(
        cmd="input-send-event",
        arguments={
            "events": [
                {"type": "rel", "data": {"axis": "y", "value": pixels}}
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse up (-Y).
@mouse.command()
async def up(ctx, pixels):
    pixels = int(pixels)
    global vm_session
    await vm_session.execute(
        cmd="input-send-event",
        arguments={
            "events": [
                {"type": "rel", "data": {"axis": "y", "value": 0-pixels}}
            ]
        }
    )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Scroll the mouse wheel.
@mouse.command()
async def scroll(ctx, pixels, direction):
    pixels = int(pixels)
    global vm_session
    if direction == "up":
        button = "wheel-up" # must explicitly go up
    else:
        button = "wheel-down"
    global vm_session
    for x in range(0,pixels):
        await vm_session.execute(
            cmd="input-send-event",
            arguments={
    
                "events": [
                    {"type": "btn", "data": { "down": True, "button": button } }
                ]
            }
        )
        await vm_session.execute(
            cmd="input-send-event",
            arguments={
    
                "events": [
                    {"type": "btn", "data": { "down": False, "button": button } }
                ]
            }
        )
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))


#List available keys
@bot.command()
async def keys(ctx):
    """Get a list of keys you can use with vb!press"""
    temp_keys = qemu_keys
    temp_keys.sort()
    await ctx.send(f"`{temp_keys}`")

#Reset the VM
@bot.command()
async def reset(ctx):
    """Reset the VM. Owner only."""
    global vm_session
    if ctx.author.id == owner_id:
        await vm_session.execute(cmd="system_reset")
        await asyncio.sleep(0.5)
        await get_vm_screenshot(vm_session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
    else:
        await ctx.send("You are not the owner.")

#Reload some bot config paramaters, but not all of them
@bot.command()
@commands.has_any_role('vm bot user')
async def reload(ctx):
    global vm_session
    """Reload the bot config files.
    
    Will also reload other config files, when added."""
    if ctx.author.id == bot.owner_id:
        _, _, vm_name, bot.owner_id, channel_id = load_config(config_file)
        print(f"VM name: {vm_name}")
        print(f"Owner ID: {owner_id}")
        print(f"Channel ID: {channel_id}")
        vm_session = QMPClient(name=vm_name)
        await vm_session.connect(('127.0.0.1', 4444))
        await ctx.send("Config reloaded!")
    else:
        await ctx.send("You are not the owner.")

@bot.command()
@commands.is_owner()
async def raw_command(ctx, command: str, args: str):
    global vm_session
    """
    Send a raw command to the QMP server.
    Admin only for obvious reasons.
    """
    if args is not None:
        cmd_args = eval(args)
    else:
        cmd_args = None
    await ctx.send(f"Command: {command}, args: {cmd_args}")
    resp = await vm_session.execute(cmd=command, arguments=cmd_args)
    await ctx.send("Server replies:")
    await ctx.send(f"```\n{resp}\n```")

@bot.command(hidden=True)
@commands.is_owner()
async def generate_key_map(ctx):
    await ctx.send("Please wait, this will take a very long time.")
    for key in qemu_keys:
        if key == "power":
            # this obviously interrupts the VM, don't do this one
            continue
        await send_key(["shift", "apostrophe"])
        await send_key([key])
        await send_key([
            "shift", "apostrophe"
        ])
        await send_key([
            "equal"
        ])
        await send_key([
            "shift", "apostrophe",
        ])
        for letter in key:
            if letter in qemu_keys:
                await send_key([letter])
            else:
                pass    
        await send_key([
            "shift", "apostrophe"
        ])
        await send_key([
            "comma"
        ])
        await send_key([
            "ret"
        ])
        # "="[key]",\n
        await asyncio.sleep(5)
    await asyncio.sleep(0.5)
    await get_vm_screenshot(vm_session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

bot.run(token)