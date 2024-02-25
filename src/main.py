import discord
import discord.app_commands as app_commands
import discord.ext.commands as cmd
from discord.app_commands import Choice
import asyncio
import time
import traceback
import package_loader
import views
import os
import database as db

BALANCE = db.Bucket(db.FileType.balance)
ACCOUNTS = db.Bucket(db.FileType.roblox_accounts)

colors = package_loader.import_("utilities").libs.colors
bot = cmd.Bot(command_prefix="!", intents=discord.Intents.all())
tree = bot.tree

def log_command_interaction(interaction: discord.Interaction):
    username = colors.magenta(interaction.user.name)
    print(colors.green(f"User ")+username+colors.green(" ran ")+colors.yellow(f"/{interaction.command.name}"))

def log_command_context(ctx: cmd.Context):
    sub_command_name = ctx.interaction.command.parent.name
    
    username = colors.magenta(ctx.author.name)
    print(colors.green(f"User ")+username+colors.green(" ran ")+colors.yellow(f"/{sub_command_name} {ctx.command.name}"))

"""
Normal Commands
"""

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await tree.sync()
    await tree.sync(guild=discord.Object(id="1206737795901689896"))
    print("Synced") 
    
@tree.command(name="reset", description="Used to reset the user in case of any issues. ADMIN ONLY COMMAND.")
@app_commands.describe(user='The user factory reset.')
async def reset(ctx: cmd.Context, user: discord.User):
    log_command_interaction(ctx)
    
    channel: discord.TextChannel = ctx.channel
    user_id = user.id
    
    user_data = {"roblox_username": "", "balance": 0, "discord_username": user.name}
    BALANCE.set_value(user_id, user_data)
    
    main_embed = discord.Embed(
                title='Balance Reset',
                description=f"<@{user_id}>'s stats have been factory reset.",
                color=discord.Color.from_str("#FF0000")
    )
        
    main_message: discord.Message = await ctx.response.send_message(embed=main_embed)

"""
Hybrid Commands (These use commands.Context instead of discord.Interaction)
"""

@bot.hybrid_group(fallback=None)
async def set(interaction: discord.Interaction):
    pass

@bot.hybrid_group(fallback=None)
async def see(interaction: discord.Interaction):
    pass

@bot.hybrid_group(fallback=None)
async def add(interaction: discord.Interaction):
    pass

@bot.hybrid_group(fallback=None)
async def sub(interaction: discord.Interaction):
    pass

@bot.hybrid_group(fallback=None)
async def panel(interaction: discord.Interaction):
    pass

@panel.command(name="balance", description="Used to send the balance panel to the current channel. ADMIN ONLY COMMAND.")
async def panel_balance(ctx: cmd.Context):
    log_command_context(ctx)
    
    channel = ctx.channel
    
    main_embed = discord.Embed(
            title='Raffle Balance',
            description='Funding roles are automatically updated based on your balance! Use raffle balance to deposit gems into your raffle account to enter into raffles! All deposits should be processed within 1-24 hours 💎',
            color=discord.Color.from_str("#69BDE4")
    )
    
    main_embed.set_footer(text='Contact support or management if you have any issues!')
    
    main_message = await channel.send(embed=main_embed, view=views.BalancePanel())
    try:
        await ctx.interaction.response.send_message(" ")
    except:
        pass

@panel.command(name="username", description="Used to send the balance panel to the current channel. ADMIN ONLY COMMAND.")
async def panel_balance(ctx: cmd.Context):
    log_command_context(ctx)
    
    channel = ctx.channel
    
    main_embed = discord.Embed(
            title='Set Username',
            description='You can use this reaction to set your username for raffle balances!',
            color=discord.Color.from_str("#90EE90")
    )

    main_embed.set_footer(text='Contact support or management if you have any issues!')
    
    main_message = await channel.send(embed=main_embed, view=views.SetUsername())
    try:
        await ctx.interaction.response.send_message(" ")
    except:
        pass
    
@set.command(name="balance", description="Used to send the balance panel to the current channel. ADMIN ONLY COMMAND.")
@app_commands.describe(user='The user to set the gems to.')
@app_commands.describe(value='The value that the balance will be set to after updating.')
async def set_balance(ctx: cmd.Context, user: discord.User, value: int):
    log_command_context(ctx)
    
    channel: discord.TextChannel = ctx.channel
    user_id = user.id
    
    BALANCE.manage_value(user_id, "balance", value)
    
    main_embed = discord.Embed(
            title='Balance Update',
            description=f"Updated <@{user_id}>'s balance to {value:,} 💎",
            color=discord.Color.from_str("#90EE90")
    )

    main_message: discord.Message = await ctx.reply(embed=main_embed)

@add.command(name="balance", description="Used to send the balance panel to the current channel. ADMIN ONLY COMMAND.")
@app_commands.describe(user='The user to add gems to.')
@app_commands.describe(value='The value that will be added to the old balance.')
async def add_balance(ctx: cmd.Context, user: discord.User, value: int):
    log_command_context(ctx)
    
    channel: discord.TextChannel = ctx.channel
    user_id = user.id
    
    old_value, success = BALANCE.get_value(user_id)
    
    if success:
        old_value = int(old_value["balance"])
        new_balance = old_value + value
    
        BALANCE.manage_value(user_id, "balance", new_balance)
        
        main_embed = discord.Embed(
                title='Balance Update',
                description=f"Added {value:,} 💎 to <@{user_id}>'s balance.",
                color=discord.Color.from_str("#90EE90")
        )
        
        main_message: discord.Message = await ctx.reply(embed=main_embed)
    else:
        BALANCE.set_value(user_id, value)
        
        main_embed = discord.Embed(
                title='Balance Update',
                description=f"Added {value:,} 💎 to <@{user_id}>'s balance.",
                color=discord.Color.from_str("#90EE90")
        )
        
        main_message: discord.Message = await ctx.reply(embed=main_embed)

@sub.command(name="balance", description="Used to send the balance panel to the current channel. ADMIN ONLY COMMAND.")
@app_commands.describe(user='The user to subtract gems from.')
@app_commands.describe(value='The value that will be subtracted from the old balance.')
async def sub_balance(ctx: cmd.Context, user: discord.User, value: int):
    log_command_context(ctx)
    
    channel: discord.TextChannel = ctx.channel
    user_id = user.id
    
    old_value, success = BALANCE.get_value(user_id)
    
    if success:
        old_value = int(old_value["balance"])
        new_balance = old_value - value
    
        BALANCE.manage_value(user_id, "balance", new_balance)
        
        main_embed = discord.Embed(
                title='Balance Update',
                description=f"Removed {value:,} 💎 from <@{user_id}>'s balance.",
                color=discord.Color.from_str("#90EE90")
        )
        
        main_message: discord.Message = await ctx.reply(embed=main_embed)
    else:
        BALANCE.set_value(user_id, value)
        
        main_embed = discord.Embed(
                title='Balance Update',
                description=f"Subtracted {value:,} 💎 from <@{user_id}>'s balance.",
                color=discord.Color.from_str("#90EE90")
        )
        
        main_message: discord.Message = await ctx.reply(embed=main_embed)

    
@see.command(name="balance", description="Used to send the balance panel to the current channel. ADMIN ONLY COMMAND.")
@app_commands.describe(user='The user to view the balance to.')
async def see_balance(ctx: cmd.Context, user: discord.User):
    log_command_context(ctx)
    
    channel: discord.TextChannel = ctx.channel
    user_id = user.id
    
    user_data = BALANCE.get_list(user_id)
   
    if user_data != None:
        roblox_username = user_data["roblox_username"] if user_data["roblox_username"] != "" else "None"
        
        main_embed = discord.Embed(
                title='Balance',
                description=f"**User:** <@{user_id}>\n**Roblox Username:** {roblox_username}\n**Balance:** {user_data["balance"]:,} 💎",
                color=discord.Color.from_str("#90EE90")
        )
        
        main_message: discord.Message = await ctx.reply(embed=main_embed)
    else: 
        user_data = {"roblox_username": "", "balance": 0, "discord_username": user.name}
        BALANCE.set_value(user_id, user_data)
            
        main_embed = discord.Embed(
                title='Balance',
                description=f"**User:** <@{user_id}>\n**Roblox Username:** {"None"}\n**Balance:** {user_data["balance"]:,} 💎",
                color=discord.Color.from_str("#90EE90")
        )
        
        main_message: discord.Message = await ctx.reply(embed=main_embed)
        
bot.run("")
