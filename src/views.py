import discord
import discord.app_commands as app_commands
import discord.ext.commands as cmd
from discord.app_commands import Choice
import database
import messages as msgs
from database import FileType

class BalancePanel(discord.ui.View):
    balance = database.Bucket(FileType.balance)
    spreadsheet = database.Bucket(FileType.roblox_accounts)
    
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="💎", custom_id="raffle_bot:diamond")
    async def diamond(self, interaction, button):  
        user_data, success = self.balance.get_value(interaction.user.id)

        if success != True:
            user_data = {"roblox_username": "", "balance": 0, "discord_username": interaction.user.name}
            self.balance.set_value(interaction.user.id, user_data)
        
        await interaction.response.send_message(f"""**Balance:** {user_data["balance"]} 💎""", ephemeral=True)
    
    @discord.ui.button(label="Deposit", style=discord.ButtonStyle.success, custom_id="raffle_bot:deposit")
    async def deposit(self, interaction, button):
        username = database.get_roblox_username(interaction.user.id)
        
        if username != None:
            await interaction.response.send_message(msgs.deposit_message.replace('^username^', username), ephemeral=True)
        else:
            await interaction.response.send_message(msgs.no_username_deposit_message, ephemeral=True)
    
    @discord.ui.button(label="See Raffles", style=discord.ButtonStyle.danger, custom_id="raffle_bot:raffles")
    async def enter_raffle(self, interaction, button):
        await interaction.response.send_message(msgs.see_raffles_message, ephemeral=True)

class SetUsername(discord.ui.View):
    class UsernameModal(discord.ui.Modal):
        spreadsheet = database.Bucket(FileType.roblox_accounts)
        
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.roblox_username = discord.ui.TextInput(label="Roblox Username (Not display name)")
            self.add_item(self.roblox_username)

        async def on_submit(self, interaction: discord.Interaction):
            success, claimed_by = database.set_roblox_username(interaction.user.id, self.roblox_username.value)
            
            if success:
                await interaction.response.send_message(content="✅ Username successfully connected to this account!", ephemeral=True)
            else:
                await interaction.response.send_message(content=f"❌ Username already claimed by <@{claimed_by}>! Make a ticket and give your username and proof of account ownership if you would like to claim it.", ephemeral=True)
            
    @discord.ui.button(label="Set Username", style=discord.ButtonStyle.secondary, custom_id="raffle_bot:diamond")
    async def diamond(self, interaction, button):
        await interaction.response.send_modal(self.UsernameModal(title="Submit Username"))