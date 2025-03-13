import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.members = True  # Enable member-related events

# Define the bot and its command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# List of role IDs allowed to use moderation commands
ALLOWED_ROLES = [
    1347339503379153057,
    1347339566696366151,
    1347339659398611041,
    1347339699986890814
]

# Variable to store the welcome channel ID
welcome_channel_id = None


# Helper function to check permissions
def has_permission(interaction: discord.Interaction) -> bool:
    user_roles = [role.id for role in interaction.user.roles]
    return any(role_id in ALLOWED_ROLES for role_id in user_roles)


# Slash Commands
@bot.tree.command(name="kick", description="Kick a member from the server")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not has_permission(interaction):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member} has been kicked. Reason: {reason}")


@bot.tree.command(name="ban", description="Ban a member from the server")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not has_permission(interaction):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member} has been banned. Reason: {reason}")


@bot.tree.command(name="timeout", description="Timeout a member")
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int):
    if not has_permission(interaction):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    # Apply timeout using datetime.utcnow()
    await member.edit(timeout=datetime.utcnow() + timedelta(minutes=duration))
    await interaction.response.send_message(f"{member} has been timed out for {duration} minutes.")


@bot.tree.command(name="untimeout", description="Remove timeout from a member")
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    if not has_permission(interaction):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    await member.edit(timeout=None)
    await interaction.response.send_message(f"{member} has been untimed out.")


# Command to set the welcome channel
@bot.tree.command(name="setwelcomechannel", description="Set the welcome message channel")
async def set_welcome_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global welcome_channel_id
    if not has_permission(interaction):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    welcome_channel_id = channel.id
    await interaction.response.send_message(f"Welcome messages will now be sent to {channel.mention}.")


# Event: On Member Join
@bot.event
async def on_member_join(member):
    global welcome_channel_id
    if welcome_channel_id:
        channel = member.guild.get_channel(welcome_channel_id)
    else:
        channel = member.guild.system_channel  # Fallback to system channel if not set

    if channel:
        welcome_message = f"Welcome to Sawaahh's Beaming, {member.mention}! Go to the sites to get started."
        await channel.send(welcome_message)


# Run the bot
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync the slash commands
    print(f"We have logged in as {bot.user}")

# Replace with your actual bot token
bot.run("MTM0OTczNjY1OTEwMDQ5OTk2OA.GS8I6a.5jKXOCphyYfBoWLHpSnGcmUH5R58GbfQ65kY3g")
