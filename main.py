import discord
import json
from enum import Enum
from discord.ext import commands

with open("setting.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open("token") as f:
    token = f.read()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

allowed_users = config["setup_allowed_users"]

rule =  config["rule"]
print(f"Added {rule}")
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def setup(ctx):

    if ctx.author.id not in allowed_users:
        await ctx.send("このコマンドは使用できません。")
        return
    
    message = await ctx.send(f"{rule}")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    channel = payload.channel_id
    rule_channel = config["channel"]["rule"]
    if channel != rule_channel:
        print(f"The Channel({channel}) is not Rule Channel({rule_channel})")
        return

    if not member or member.bot:
        return

    role_dict = {
        "✅": "メンバー",
        "❌": "同意しねえぜ"
    }

    role_name = role_dict.get(payload.emoji.name)

    if role_name == None:
        print(f"WARN: The emoji({payload.emoji.name}) is missing in role_dict.")
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        print(f"Added {role_name} to {member.name}")
    
    channel = bot.get_channel(config["channel"]["log"])
    if channel:
        await channel.send(f"Added {role_name} to {member.name}")

bot.run(token)
