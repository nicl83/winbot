import virtualbox, discord, sys, asyncio, traceback, winbot_common
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

bot = commands.Bot(command_prefix = prefix)
bot.owner_id = owner_id
bot.channel_id = channel_id
bot.mouse_state = 0

bot.vbox = virtualbox.VirtualBox()
bot.vm = bot.vbox.find_machine(vm_name)
bot.session = bot.vm.create_session()

cogs = ['cogs.keyboard',
        'cogs.mouse',
        'cogs.general'
        ]
        
for cog in cogs:
    try:
        bot.load_extension(cog)
        print(f"Loaded {cog} succesfully")
    except Exception as e:
        print(f"Failed to load {cog}: {e}")

#Send a screenshot of the current state of the VM when started.
@bot.event
async def on_ready():
    winbot_common.get_vm_screenshot(bot.session, 'temp.png')
    channel = bot.get_channel(bot.channel_id)
    await channel.send('Winbot has started! Current VM state:', file=discord.File('temp.png'))

#Reload a cog - i.e if changes were made:
@bot.command()
async def reloadcog(ctx, reload_cog):
    if ctx.author.id == owner_id:
        bot.reload_extension(reload_cog)
        print(f"Reloaded {reload_cog}!")
        await ctx.send(f"Reloaded {reload_cog}!")

        

#Handle exceptions.
@bot.event
async def on_command_error(ctx, exception):
    tb_data = ''.join(traceback.format_tb(exception.__traceback__))
    await ctx.send(f"Sorry, an error occurred.\n```\n{repr(exception)}\n{tb_data}\n```")

bot.run(token)