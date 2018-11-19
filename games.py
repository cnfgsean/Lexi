"""
BOT COG: Commands which relate to games, miscellaneous behavior
"""
import discord
from discord.ext import commands
import functions_en as en
import random

class Games:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def opinion(self, *item):
        item = list(item)
        print(item)
        verdict = en.will_like(item)
        await self.client.say("\n".join(verdict))

    @commands.command(pass_context=True)
    async def yomamma(self, ctx, victim=None):
        author = "<@{}>".format(ctx.message.author.id)
        print(author, victim)
        x = (random.randint(0, 49)) * 2  # from 0 to 98
        line1 = en.random_from_txt("texts/yo_mamma.txt", x + 1)  # from 1 to 99
        line2 = en.random_from_txt("texts/yo_mamma.txt", x + 2)  # from 2 to 100
        if not victim:
            await self.client.say("\n".join([line1, line2]))
        else:
            await self.client.say("{} :arrow_right: {}".format(author, victim))
            await self.client.say("\n".join([line1, line2]))


def setup(client):
    client.add_cog(Games(client))
