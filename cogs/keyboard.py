import virtualbox, asyncio, winbot_common
from discord.ext import commands

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

#Send long string or normal chars to VM
@commands.command()
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

@commands.command()
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

#List available keys
@commands.command()
async def keys(ctx):
    """Get a list of keys you can use with vb!press"""
    keys = list(keycodes.keys())
    keys.sort()
    await ctx.send(f"`{keys}`")

def setup(bot):
    bot.add_command(type)
    bot.add_command(press)
    bot.add_command(keys)
    
if __name__ == "__main__":
    print("This is a library or cog and should not be executed directly.")