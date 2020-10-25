import virtualbox, asyncio, winbot_common
from discord.ext import commands

#Ping pong!
@commands.command()
async def ping(ctx):
    """Ping Pong!
    
    If the bot is alive, it will reply with "Pong!\""""
    for key in ctx:
        print(f"debug: {key} is {getattr(ctx.key)}")
    await ctx.send('Pong!')

#Get image of VM
@commands.command()
async def screen(ctx):
    """Get a screenshot of the VM."""
    get_vm_screenshot(bot.session, 'temp.png')
    await ctx.send('Say cheese!', file=discord.File('temp.png'))

#Reset the VM
@commands.command()
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
@commands.command()
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
        
def setup(bot):
    bot.add_command(ping)
    bot.add_command(screen)
    bot.add_command(reset)
    bot.add_command(reload)
    
if __name__ == "__main__":
    print("This is a library or cog and should not be executed directly.")