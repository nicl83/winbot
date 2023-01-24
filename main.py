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

#i hate this next section of code.
#i never want to touch keycodes again.
keycodes = {
    'esc': (0x01, 0x81),
    '1': (0x02, 0x82),
    '2': (0x03, 0x83),
    '3': (0x04, 0x84),
    '4': (0x05, 0x85),
    '5': (0x06, 0x86),
    '6': (0x07, 0x87),
    '7': (0x08, 0x88),
    '8': (0x09, 0x89),
    '9': (0x0A, 0x8A),
    '0': (0x0B, 0x8B),
    '-': (0x0C, 0X8C),
    '+': (0x0D, 0X8D),
    'backspace': (0x0e, 0x8e),
    'tab': (0x0f, 0x8f),
    'q': (0x10, 0x90),
    'w': (0x11, 0x91),
    'e': (0x12, 0x92),
    'r': (0x13, 0x93),
    't': (0x14, 0x94),
    'y': (0x15, 0x95),
    'u': (0x16, 0x96),
    'i': (0x17, 0x97),
    'o': (0x18, 0x98),
    'p': (0x19, 0x99),
    '[': (0x1a, 0x9a),
    ']': (0x1b, 0x9b),
    'enter': (0x1c, 0x9c),
    'ctrl': (0x1d),
    'a': (0x1e, 0x9e),
    's': (0x1f, 0x9f),
    'd': (0x20, 0xa0),
    'f': (0x21, 0xa1),
    'g': (0x22, 0xa2),
    'h': (0x23, 0xa3),
    'j': (0x24, 0xa4),
    'k': (0x25, 0xa5),
    'l': (0x26, 0xa6),
    ';': (0x27, 0xa7),
    "'": (0x28, 0xa8),
    '~': (0x29, 0xa9),
    'shift': (0x2a),
    '\\': (0x2b, 0xab),
    'z': (0x2c, 0xac),
    'x': (0x2d, 0xad),
    'c': (0x2e, 0xae),
    'v': (0x2f, 0xaf),
    'b': (0x30, 0xb0),
    'n': (0x31, 0xb1),
    'm': (0x32, 0xb2),
    ',': (0x33, 0xb3),
    '.': (0x34, 0xb4),
    '/': (0x35, 0xb5),
    'rshift': (0x36),
    'numpad*': (0x37, 0xb7),
    'alt': (0x38),
    'space': (0x39, 0xb9),
    'caps': (0x3a, 0xba),
    'f1': (0x3b, 0xbb),
    'f2': (0x3c, 0xbc),
    'f3': (0x3d, 0xbd),
    'f4': (0x3e, 0xbe),
    'f5': (0x3f, 0xbf),
    'f6': (0x40, 0xc0),
    'f7': (0x41, 0xc1),
    'f8': (0x42, 0xc2),
    'f9': (0x43, 0xc3),
    'f10': (0x44, 0xc4),
    'numlock': (0x45),
    'scrolllock': (0x46),
    'numpad7': (0x47, 0xc7),
    'numpad8': (0x48, 0xc8),
    'numpad9': (0x49, 0xc9),
    'keypad-': (0x4a, 0xca),
    'numpad4': (0x4b, 0xcb),
    'numpad5': (0x4c, 0xcc),
    'numpad6': (0x4d, 0xcd),
    'numpad+': (0x4e, 0xce),
    'numpad1': (0x4f, 0xcf),
    'numpad2': (0x50, 0x50),
    'numpad3': (0x51, 0x51),
    'numpad0': (0x52, 0x52),
    'numpad.': (0x53, 0x53),
    'up': (0xe0, 0x48, 0xe0, 0xc8),
    'left': (0xe0, 0x4b, 0xe0, 0xcb),
    'right': (0xe0, 0x4d, 0xe0, 0xcd),
    'down': (0xe0, 0x50, 0xe0, 0xd0),
    'pgup': (0xe0, 0x49, 0xe0, 0xc9),
    'pgdown': (0xe0, 0x51, 0xe0, 0xd1),
    'win': (0xe0, 0x5b, 0xe0, 0xdb)
}

keycodes_no_up = {
    'esc': (0x01),
    '1': (0x02),
    '2': (0x03),
    '3': (0x04),
    '4': (0x05),
    '5': (0x06),
    '6': (0x07),
    '7': (0x08),
    '8': (0x09),
    '9': (0x0A),
    '0': (0x0B),
    '-': (0x0C),
    '+': (0x0D),
    'backspace': (0x0e),
    'tab': (0x0f),
    'q': (0x10),
    'w': (0x11),
    'e': (0x12),
    'r': (0x13),
    't': (0x14),
    'y': (0x15),
    'u': (0x16),
    'i': (0x17),
    'o': (0x18),
    'p': (0x19),
    '[': (0x1a),
    ']': (0x1b),
    'enter': (0x1c),
    'ctrl': (0x1d),
    'a': (0x1e),
    's': (0x1f),
    'd': (0x20),
    'f': (0x21),
    'g': (0x22),
    'h': (0x23),
    'j': (0x24),
    'k': (0x25),
    'l': (0x26),
    ';': (0x27),
    "'": (0x28),
    '~': (0x29),
    'shift': (0x2a),
    '\\': (0x2b),
    'z': (0x2c),
    'x': (0x2d),
    'c': (0x2e),
    'v': (0x2f),
    'b': (0x30),
    'n': (0x31),
    'm': (0x32),
    ',': (0x33),
    '.': (0x34),
    '/': (0x35),
    'rshift': (0x36),
    'numpad*': (0x37),
    'alt': (0x38),
    'space': (0x39),
    ' ': (0x39),
    'caps': (0x3a),
    'f1': (0x3b),
    'f2': (0x3c),
    'f3': (0x3d),
    'f4': (0x3e),
    'f5': (0x3f),
    'f6': (0x40),
    'f7': (0x41),
    'f8': (0x42),
    'f9': (0x43),
    'f10': (0x44),
    'numlock': (0x45),
    'scrolllock': (0x46),
    'numpad7': (0x47),
    'numpad8': (0x48),
    'numpad9': (0x49),
    'keypad-': (0x4a),
    'numpad4': (0x4b),
    'numpad5': (0x4c),
    'numpad6': (0x4d),
    'numpad+': (0x4e),
    'numpad1': (0x4f),
    'numpad2': (0x50),
    'numpad3': (0x51),
    'numpad0': (0x52),
    'numpad.': (0x53),
    'up': (0xe0, 0x48),
    'left': (0xe0, 0x4b),
    'right': (0xe0, 0x4d),
    'down': (0xe0, 0x50),
    'pgup': (0xe0, 0x49),
    'pgdown': (0xe0, 0x51),
    'win': (0xe0, 0x5b)
}

qemu_keys = ['unmapped', 'pause', 'ro', 'kp_comma', 'kp_equals', 'power', 'hiragana', 'henkan', 'yen', 'sleep', 'wake', 'audionext', 'audioprev', 'audiostop', 'audioplay', 'audiomute', 'volumeup', 'volumedown', 'mediaselect', 'mail', 'calculator', 'computer', 'ac_home', 'ac_back', 'ac_forward', 'ac_refresh', 'ac_bookmarks', 'muhenkan', 'katakanahiragana', 'lang1', 'lang2', 'shift', 'shift_r', 'alt', 'alt_r', 'ctrl', 'ctrl_r', 'menu', 'esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'minus', 'equal', 'backspace', 'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'bracket_left', 'bracket_right', 'ret', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'semicolon', 'apostrophe', 'grave_accent', 'backslash', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma', 'dot', 'slash', 'asterisk', 'spc', 'caps_lock', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'num_lock', 'scroll_lock', 'kp_divide', 'kp_multiply', 'kp_subtract', 'kp_add', 'kp_enter', 'kp_decimal', 'sysrq', 'kp_0', 'kp_1', 'kp_2', 'kp_3', 'kp_4', 'kp_5', 'kp_6', 'kp_7', 'kp_8', 'kp_9', 'less', 'f11', 'f12', 'print', 'home', 'pgup', 'pgdn', 'end', 'left', 'up', 'down', 'right', 'insert', 'delete', 'stop', 'again', 'props', 'undo', 'front', 'copy', 'open', 'paste', 'find', 'cut', 'lf', 'help', 'meta_l', 'meta_r', 'compose']

qemu_aliases = {
    ' ': 'spc',
    'win': 'meta_l',
    'cmd': 'meta_l',
    'opt': 'alt',
    'space': 'spc',
    'enter': 'ret'
}

intents = discord.Intents(messages=True, guilds=True, message_content=True)
bot = commands.Bot(command_prefix = prefix, intents = intents, owner_id=owner_id)
mouse_state = dict()

vm_session = QMPClient(vm_name)

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
@bot.command()
async def type(ctx, *, arg: str):
    """Sends a long string of text to the VM, followed by a newline."""
    global vm_session
    for key in arg:
        if key.lower() not in qemu_keys:
            if key in qemu_aliases.keys():
                await vm_session.execute(
                    cmd="send-key",
                    arguments={"keys": [
                        {"type": "qcode", "data": qemu_aliases[key]}
                    ]}
                )
            else:    
                await ctx.send(f"Unkown key: {key}")
                await asyncio.sleep(0.1)
        elif key.isupper():
            await vm_session.execute(
                cmd="send-key",
                arguments={"keys": [
                    {"type": "qcode", "data": "shift"},
                    {"type": "qcode", "data": key.lower()}
                ]}
            )
        else:
            await vm_session.execute(
                cmd="send-key",
                arguments={"keys": [
                    {"type": "qcode", "data": key}
                ]}
            )
    await vm_session.execute(
        cmd="send-key",
        arguments={"keys": [
            {"type": "qcode", "data": "ret"}
        ]}
    )
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
    key_event_list = []
    for key in args:
        key = key.lower() # discard case sensitivity
        if key not in qemu_keys:
            if key in qemu_aliases.keys():
                await vm_session.execute(
                    cmd="send-key",
                    arguments={"keys": [
                        {"type": "qcode", "data": qemu_aliases[key]}
                    ]}
                )
            else:    
                await ctx.send(f"Unkown key: {key}")
                await asyncio.sleep(0.1)
        else:
            key_event_list.append({
                "type": "qcode",
                "data": key
            })
    await vm_session.execute(
        cmd="send-key",
        arguments={"keys": key_event_list}
    )
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
        await vm_session.execute(
                cmd="send-key",
                arguments={"keys": [
                    {"type": "qcode", "data": 'backspace'}
                ]}
            )
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

bot.run(token)