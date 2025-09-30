from discord.ext import commands
import discord
import os
import random

MY_USER_ID = int(os.getenv("MY_USER_ID"))

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("quotes.txt", "r", encoding="utf-8") as f:
            self.quotes = [line.strip() for line in f if line.strip()]

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # Checks if bot is responsive
    @discord.app_commands.command(name="ping", description="Check if the bot is responsive")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong!")

    # Sends a message to a specific user (OWNER ONLY)
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

    # Sends a message to a specific channel (OWNER ONLY)
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

    # Sends a random quote
    @discord.app_commands.command(name="quote", description="Send a random quote")
    async def quote(self, interaction: discord.Interaction):
        if not self.quotes:
            await interaction.response.send_message("❌ No quotes available.")
            return
        random_quote = random.choice(self.quotes)
        if " - " in random_quote:
            quote_text, author = random_quote.rsplit(" - ", 1)
            embed_description = f"{quote_text}\n\n— {author}"
        else:
            embed_description = random_quote
        embed = discord.Embed(description=embed_description, color=0x38bdf8)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))