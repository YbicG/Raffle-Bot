import discord
import discord.app_commands as app_commands
import discord.ext.commands as cmd
from discord.app_commands import Choice
import asyncio
import time
import traceback
import package_loader
import views

colors = package_loader.import_("utilities").libs.colors
bot = cmd.Bot(command_prefix="!", intents=discord.Intents.all())
tree = bot.tree

def log_command(ctx):
    username = colors.magenta(ctx.user.name)
    print(colors.green(f"User ")+username+colors.green(" ran ")+colors.yellow(f"/{ctx.command.name}"))
    
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await tree.sync()
    await tree.sync(guild=discord.Object(id="1206737795901689896"))
    print("Synced")

@tree.command(name="panel_balance", description="Used to send the balance panel to the current channel. ADMIN ONLY COMMAND.")
async def panel_balance(ctx):
    log_command(ctx)
    
    channel = ctx.channel
    
    secondary_embed = discord.Embed(
            title='Set Username',
            description='You can use this reaction to set your username for raffle balances!',
            color=discord.Color.from_str("#90EE90")
    )
    
    main_embed = discord.Embed(
            title='Raffle Balance',
            description='Funding roles are automatically updated based on your balance! You can withdraw or deposit gems at any time. Withdraws and deposits are handled manually by a select team of admins, and should be processed within 1-24 hours 💎',
            color=discord.Color.from_str("#69BDE4")
    )
    
    main_embed.set_footer(text='Contact support or management if you have any issues!')
    
    secondary_message = await channel.send(embed=secondary_embed, view=views.SetUsername())
    main_message = await channel.send(embed=main_embed, view=views.BalancePanel())
    try:
        await ctx.response.send_message(" ")
    except:
        pass

@tree.command(name="test", description="Testing")
@app_commands.describe(msg='Testing')
async def test(ctx, msg: str):
    await ctx.response.send_message(f"Testing to see if I come on! {msg}")

bot.run("MTIxMDM4NTY3NDg1NTkwNzQwOA.GrhXPX.yhjllKmlHY1DMjE5qUW8C6LWYMFTlEsSPxWODs")