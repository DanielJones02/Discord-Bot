# auto install modules
try:
    from discord.ext import commands
    from colorama import Fore
    import discord
except ModuleNotFoundError:
    import os
    os.system('pip install discord')
    os.system('pip install colorama')

    # if program fails to auto install requirements
    # run this in your terminal
    # pip install -r requirements.txt

from discord.ext import commands
from discord import app_commands
from colorama import Fore
import time
import discord

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(Fore.LIGHTGREEN_EX, f"Ready and online - {bot.user.display_name}\n", Fore.RESET)

    # Lists every guild the bot is in

    try:
        guild_count = 0

        for guild in bot.guilds:
            print(Fore.RED, f"- {guild.id} (name: {guild.name})\n", Fore.RESET)

            guild_count = guild_count + 1

        print(Fore.GREEN, f"{bot.user.display_name} is in " + str(guild_count) + " guilds.\n", Fore.RESET)

        synced = await bot.tree.sync() # Loads/syncs commands
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(e)


# Simple Test command
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong! {0}'.format(round(bot.latency, 1)), ephemeral=True)
    print(Fore.CYAN, f"/ping | {interaction.channel} | Executed By {interaction.user}", Fore.RESET)


# Repeats what you say 
@bot.tree.command(name="say")
@app_commands.describe(thing_2_say="What should I say??")
async def say(interaciton: discord.Interaction, thing_2_say: str):
    await interaciton.response.send_message(f"{thing_2_say}")
    print(Fore.CYAN, f"/say {thing_2_say} | {interaciton.channel} | Executed By {interaciton.user}", Fore.RESET)


# Nukes/purges the channel you run the command in
@bot.tree.command(name="nuke")
@app_commands.checks.has_permissions(manage_channels=True, manage_messages=True)
async def nuke(interaction: discord.Interaction):
    await interaction.channel.delete()
    new_channel = await interaction.channel.clone(reason="Channel was purged")
    await new_channel.edit(position=interaction.channel.position)
    await new_channel.send(f"This Channel was purged.")

    print(Fore.RED, f'Purged {interaction.channel} | Executed By {interaction.user}', Fore.RESET)

@nuke.error
async def nuke_error(interaction: discord.Interaction):
    await interaction.response.send_message("Insufficient Permissions", ephemeral=True)
    print(Fore.RED, f'/nuke {interaction.channel} | Insufficient Perms | Executed By {interaction.user}', Fore.RESET)


# Nukes/Purges every single channel in the guild
@bot.tree.command(name="nuke_everything")
@app_commands.checks.has_permissions(administrator=True) # administrator Needed
async def nuke_everything(interaction: discord.Interaction):
    # Get the guild from the interaction
    guild = interaction.guild

    # Iterate through channels in the guild
    for channel in guild.channels:
        try:
            # Check if the channel is a category
            if isinstance(channel, discord.CategoryChannel):
                continue  # Skip categories

            # Get the category ID of the channel
            category_id = channel.category_id

            # Delete the channel
            await channel.delete(reason="Channel was purged")

            # Clone the channel
            new_channel = await channel.clone(reason="Channel was purged")

            # Set the new channel's position to match the original channel
            await new_channel.edit(position=channel.position)

            # If the original channel was in a category, assign the new channel to the same category
            if category_id:
                category = guild.get_channel(category_id)
                if category:
                    await new_channel.edit(category=category)

            await new_channel.send(f"This Channel was purged.")

            print(Fore.RED, f'Purged {channel} | Executed By {interaction.user}', Fore.RESET)
        except Exception as e:
            print(Fore.RED, f"Failed to purge {channel}! | Error: {e}", Fore.RESET)

    print(Fore.MAGENTA,
          f"/nuke_everything | {interaction.channel} | Purges Everything | Executed By {interaction.user}",
          Fore.RESET)
    

@nuke_everything.error
async def nuke_all_error(interaction: discord.Interaction):
    await interaction.response.send_message("Insufficient Permissions", ephemeral=True)
    print(Fore.RED, f'/nuke_everything | {interaction.channel} | Insufficient Perms | Executed By {interaction.user}', Fore.RESET)


# This command Deletes every single channel in the guild
@bot.tree.command(name="delete")
@app_commands.checks.has_permissions(administrator=True) # administrator Needed
async def delete(interaction: discord.Interaction):
    for channel in interaction.guild.channels:
        try:
            await channel.delete(reason="Nuked")
        except Exception as e:
            print(Fore.RED, f"Failed to delete channel | Error: {e}")

    print(Fore.MAGENTA, f"/delete | {interaction.channel} | Deleted all channels | Executed By {interaction.user}", Fore.RESET)
    

@delete.error
async def delete_error(interaction: discord.Interaction):
    await interaction.response.send_message("Insufficient Permissions", ephemeral=True)
    print(Fore.RED, f'/delete {interaction.channel} | Insufficient Perms | Executed By {interaction.user}', Fore.RESET)


token = ''
bot.run(token)
