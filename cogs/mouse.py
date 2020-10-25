import virtualbox, asyncio, winbot_common, discord
from discord.ext import commands

#Send a mouse command
@commands.group()
async def mouse(ctx):     
    """Perform a mouse-related function."""
    if ctx.invoked_subcommand is None:
        await ctx.send(f"Unknown mouse command, do {prefix}help mouse for valid commands!")

#Click the mouse
@mouse.command()
async def click(ctx, *args):
    ctx.bot.mouse_state = 0x01
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, ctx.bot.mouse_state)
    ctx.bot.mouse_state = 0x00
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Click and hold the mouse
@mouse.command()
async def clickhold(ctx, *args):
    ctx.bot.mouse_state = 0x01
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Right click the mouse.
@mouse.command()    
async def rclick(ctx, *args):
    ctx.bot.mouse_state = 0x02
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, ctx.bot.mouse_state)
    ctx.bot.mouse_state = 0x00
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Right click and hold the mouse.
@mouse.command()
async def rclickhold(ctx, *args):
    ctx.bot.mouse_state = 0x02
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Stop holding any mouse buttons (reset state to 0).
@mouse.command()
async def release(ctx, *args):
    ctx.bot.mouse_state = 0x00
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse right (+X).
@mouse.command()
async def right(ctx, pixels):
    ctx.bot.session.console.mouse.put_mouse_event(int(pixels), 0, 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse left (-X).
@mouse.command()
async def left(ctx, pixels):
    ctx.bot.session.console.mouse.put_mouse_event(0-int(pixels), 0, 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse down (+Y).
@mouse.command()
async def down(ctx, pixels):
    ctx.bot.session.console.mouse.put_mouse_event(0, int(pixels), 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Move the mouse up (-Y).
@mouse.command()
async def up(ctx, pixels):
    ctx.bot.session.console.mouse.put_mouse_event(0, 0-int(pixels), 0, 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Scroll the mouse wheel.
@mouse.command()
async def scroll(ctx, pixels):
    ctx.bot.session.console.mouse.put_mouse_event(0, 0, int(pixels), 0, ctx.bot.mouse_state)
    await asyncio.sleep(0.5)
    winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
    await ctx.send('Done!', file=discord.File('temp.png'))

#Send a raw put_mouse_event command. (Semi-secret)    
@mouse.command()
async def rawcommand(ctx, *args):
        if len(args) == 5:
            ctx.bot.session.console.mouse.put_mouse_event(int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))
            await asyncio.sleep(0.5)
            winbot_common.get_vm_screenshot(ctx.bot.session, 'temp.png')
            await ctx.send('Done!', file=discord.File('temp.png'))
        else:
            await ctx.send("uh uh uh, you didn't say the magic words!")

def setup(bot):
    bot.add_command(mouse)

if __name__ == "__main__":
    print("This is a library or cog and should not be executed directly.")