import virtualbox, discord, sys, asyncio, random
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

bot = commands.Bot(command_prefix = prefix)
bot.owner_id = owner_id
bot.channel_id = channel_id
bot.mouse_state = 0

bot.vbox = virtualbox.VirtualBox()
bot.vm = bot.vbox.find_machine(vm_name)
bot.session = bot.vm.create_session()

@bot.event
async def on_ready():
    get_vm_screenshot(bot.session, 'temp.png')
    channel = bot.get_channel(bot.channel_id)
    await channel.send('Winbot has started! Current VM state:', file=discord.File('temp.png'))

#Ping pong!
@bot.command()
async def ping(ctx):
    """Ping Pong!
    
    If the bot is alive, it will reply with "Pong!\""""
    await ctx.send('Pong!')

#Get image of VM
def get_vm_screenshot(vm_sesh, file_name):
    h, w, _, _, _, _ = vm_sesh.console.display.get_screen_resolution(0)
    png = vm_sesh.console.display.take_screen_shot_to_array(0, h, w, virtualbox.library.BitmapFormat.png)
    with open(file_name, 'wb') as file:
        file.write(png)

@bot.command()
async def screen(ctx):
    """Get a screenshot of the VM."""
    get_vm_screenshot(bot.session, 'temp.png')
    await ctx.send('Say cheese!', file=discord.File('temp.png'))

#Send long string or normal chars to VM
@bot.command()
async def type(ctx, *, arg):
    """Sends a long string of text to the VM, followed by a newline."""
    bot.session.console.keyboard.put_keys(arg + '\n')
    await asyncio.sleep(0.5)
    get_vm_screenshot(bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Send special buttons to the VM
def release_special_keys(key_session):
    release_codes = [0x9d, 0xaa, 0xb8, 0xb6]
    key_session.console.keyboard.put_scancodes(release_codes)

@bot.command()
async def press(ctx, *args):
    """Send special keys to the VM.
    
    Get a list of valid keys with vb!keys. Also accepts a sequence of keys."""
    try:
        temp_scancodes = []
        for key in args:
            print(keycodes[key])
            if isinstance(keycodes[key], int):
                temp_scancodes.append(keycodes[key])
            else:
                temp_scancodes = [*temp_scancodes, *keycodes[key]]
        print(temp_scancodes)
        bot.session.console.keyboard.put_scancodes(temp_scancodes)
        release_special_keys(bot.session)
        await asyncio.sleep(0.5)
        get_vm_screenshot(bot.session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
        bot.session.console.keyboard.release_keys()
    except Exception as e:
        print(repr(e))
        await ctx.send("Something went wrong whilst doing that, try again or check the log!")

#Send a mouse command
@bot.command()
async def mouse(ctx, *args):
    """Do mouse shit.
    Move the mouse around. Valid commands: up, down, left, right, click, rclick, clickhold, rclickhold, release, scroll"""
    if args[0] == "random":
        fuck = random.randint(1,12)
        if fuck=1: # click
            bot.mouse_state = 0x01
            bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
            bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, 0x00)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=2: # clickhold
            bot.mouse_state = 0x01
            bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=3: # rclick
            bot.mouse_state = 0x02
            bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
            bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, 0x00)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=4: # rclickhold
            bot.mouse_state = 0x02
            bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=5: # release
            bot.mouse_state = 0x00
            bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=6: # right
            bot.session.console.mouse.put_mouse_event(random.randint(0,800), 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=7: # left
            bot.session.console.mouse.put_mouse_event(0-(random.randint(0,800), 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=8: # up
            bot.session.console.mouse.put_mouse_event(0, 0-(random.randint(0,600), 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=9: # down
            bot.session.console.mouse.put_mouse_event(0, random.randint(0,600), 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=10: # absx
            bot.session.console.mouse.put_mouse_event_absolute(random.randint(0,800), 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=11: # absy
            bot.session.console.mouse.put_mouse_event_absolute(0, random,randint(0,600), 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        elif fuck=12: # scroll
            bot.session.console.mouse.put_mouse_event(0, 0, int(args[1]), 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        
    if args[0] == "click":
        bot.mouse_state = 0x01
        bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
        bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, 0x00)
        await asyncio.sleep(0.5)
        get_vm_screenshot(bot.session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
        
    elif args[0] == "clickhold":
        bot.mouse_state = 0x01
        bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
        await asyncio.sleep(0.5)
        get_vm_screenshot(bot.session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
        
    elif args[0] == "rclick":
        bot.mouse_state = 0x02
        bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
        bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, 0x00)
        await asyncio.sleep(0.5)
        get_vm_screenshot(bot.session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
        
    elif args[0] == "rclickhold":
        bot.mouse_state = 0x02
        bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
        await asyncio.sleep(0.5)
        get_vm_screenshot(bot.session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
        
    elif args[0] == "release":
        bot.mouse_state = 0x00
        bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, bot.mouse_state)
        await asyncio.sleep(0.5)
        get_vm_screenshot(bot.session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
        
    elif args[0] == "right":
        if len(args) == 2:
            bot.session.console.mouse.put_mouse_event(int(args[1]), 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')
            
    elif args[0] == "left":
        if len(args) == 2:
            bot.session.console.mouse.put_mouse_event(0-int(args[1]), 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')
            
    elif args[0] == "up":
        if len(args) == 2:
            bot.session.console.mouse.put_mouse_event(0, 0-int(args[1]), 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')        
    
    elif args[0] == "down":
        if len(args) == 2:
            bot.session.console.mouse.put_mouse_event(0, int(args[1]), 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')
            
    elif args[0] == "absx":
        if len(args) == 2:
            bot.session.console.mouse.put_mouse_event_absolute(int(args[1]), 0, 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')
    
    elif args[0] == "absy":
        if len(args) == 2:
            bot.session.console.mouse.put_mouse_event_absolute(0, int(args[1]), 0, 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')
            
    elif args[0] == "scroll":
        if len(args) == 2:
            bot.session.console.mouse.put_mouse_event(0, 0, int(args[1]), 0, bot.mouse_state)
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')
            
    elif args[0] == "rawcommand":
        if len(args) == 6:
            bot.session.console.mouse.put_mouse_event(int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))
            await asyncio.sleep(0.5)
            get_vm_screenshot(bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send('I need more arguments!')
            
    else:
        await ctx.send("Invalid mouse command! Valid commands: `click, clickhold, rclick, rclickhold, release, x, y, absx, absy, scroll, rawcommand`")

#List available keys
@bot.command()
async def keys(ctx):
    """Get a list of keys you can use with vb!press"""
    keys = list(keycodes.keys())
    keys.sort()
    await ctx.send(f"`{keys}`")

#Reset the VM
@bot.command()
async def reset(ctx):
    """Reset the VM. Owner only."""
    if ctx.author.id == owner_id:
        bot.session.console.reset()
        await asyncio.sleep(0.5)
        get_vm_screenshot(bot.session, 'temp.png')
        await ctx.send('Done!', file=discord.File('temp.png'))
    else:
        await ctx.send("You are not the owner.")

#Reload some bot config paramaters, but not all of them
@bot.command()
async def reload(ctx):
    """Reload the bot config files.
    
    Will also reload other config files, when added."""
    if ctx.author.id == bot.owner_id:
        _, _, vm_name, bot.owner_id, bot.channel_id = load_config(config_file)
        print(f"VM name: {vm_name}")
        print(f"Owner ID: {owner_id}")
        print(f"Channel ID: {channel_id}")
        try:
            bot.session.unlock_machine()
        except:
            print("Warning: session not unlocked. You probably don't need to worry about this.")
        bot.vm = bot.vbox.find_machine(vm_name)
        bot.session = bot.vm.create_session()
        await ctx.send("Config reloaded!")
    else:
        await ctx.send("You are not the owner.")

bot.run(token)
