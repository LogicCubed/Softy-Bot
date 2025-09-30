from discord.ext import commands
import discord
import os

MY_USER_ID = int(os.getenv("MY_USER_ID"))

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="dmuser", description="DM a user by ID (OWNER ONLY)")
    async def dmuser(self, interaction: discord.Interaction, user_id: str, message: str):
        if interaction.user.id != MY_USER_ID:
            return await interaction.response.send_message("❌ You are not allowed to use this command.")
        try:
            user = await self.bot.fetch_user(int(user_id))
            await user.send(message)
            await interaction.response.send_message(f"✅ Sent a DM to {user.name}!")
        except discord.NotFound:
            await interaction.response.send_message("❌ Could not find that user.")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I cannot DM this user. They might have DMs disabled.")
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}")

    @discord.app_commands.command(name="sendchannel", description="Send a message to a channel by ID (OWNER ONLY)")
    async def sendchannel(self, interaction: discord.Interaction, channel_id: str, message: str):
        if interaction.user.id != MY_USER_ID:
            return await interaction.response.send_message("❌ You are not allowed to use this command.")
        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            return await interaction.response.send_message("❌ Could not find that channel.")
        try:
            await channel.send(message)
            await interaction.response.send_message(f"✅ Sent your message to {channel.name}!")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I cannot send messages to that channel.")
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}")

    @discord.app_commands.command(name="setstatus", description="Set the bot's status (OWNER ONLY)")
    async def setstatus(self, interaction: discord.Interaction, status_text: str):
        if interaction.user.id != MY_USER_ID:
            return await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
        activity = discord.Game(name=status_text)
        await self.bot.change_presence(activity=activity)
        await interaction.response.send_message(f"✅ Bot status updated to: {status_text}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))