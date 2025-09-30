from discord.ext import commands
import discord
import random

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("quotes.txt", "r", encoding="utf-8") as f:
            self.quotes = [line.strip() for line in f if line.strip()]

    @discord.app_commands.command(name="ping", description="Check if the bot is responsive")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong!")

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
    await bot.add_cog(UserCommands(bot))