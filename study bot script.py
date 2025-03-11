import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass

CHANNEL_ID = 1331032469905866816

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0
    
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()
MAX_SESSION_TIME_MINUTES = 1

@bot.event
async def on_ready():
    print("Hello! Study boy is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")

# tasks run immediately on startup
@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():

    # Ignore first time this runs i.e on startup
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break.** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes")



@bot.command() 
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)

    await ctx.send(f'The result of the sum is {result}')

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    readableTime = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start() 
    await ctx.send(f'New session started at {readableTime}')

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    readableDuration = str(datetime.timedelta(seconds = duration))
    break_reminder.stop()
    await ctx.send(f'Session ended after {readableDuration} seconds')


bot.run(BOT_TOKEN)