""" Discord redbot cog which continuously wipes out any message it can older than 7 days. """

import asyncio
import datetime 
import discord
import os
import time
import json
from redbot.core import commands

DELETE_OLDER_THAN = datetime.timedelta(days=7)
ids = {}

class MemoryHole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open('memoryhole_ids.json') as f:
                ids = json.load(f)
        except FileNotFoundError:
            print("Could not load memoryhole ids")

    @commands.command(pass_context=True)
    async def memoryhole(self, ctx):
        """Toggles the user's inclusion in the memoryhole program"""
        author = ctx.message.author.id
        if author not in ids:
            ids[author] = "1"
            await ctx.send("You are now being memoryholed")
        else:
            del ids[author]
            await ctx.send("You are no longer being memoryholed")
        with open('memoryhole_ids.json', 'w+') as f:
            json.dump(ids, f)

    async def loop(self):
        while self is self.bot.get_cog("MemoryHole"):
            await asyncio.sleep(0.1)
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    print("Wiping {} #{}".format(guild.name, channel.name))
                    try:
                        async for message in channel.history(limit=None, before=datetime.datetime.utcnow() - DELETE_OLDER_THAN, after=None, oldest_first=True):
                            try:
                                if message.author.id in ids:
                                    await message.delete()
                                    print("Deleted {}".format(message.clean_content))
                            except discord.errors.NotFound:
                                pass
                            except discord.errors.Forbidden:
                                print("Can't delete messages")
                                break
                    except discord.errors.Forbidden:
                        print("Can't read message history")
                    except discord.errors.HTTPException:
                        print("HTTP error")


def setup(bot):
    b = MemoryHole(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(b.loop())
    bot.add_cog(b)
