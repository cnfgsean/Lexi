"""
BOT COG: Commands which relate to grammar (i.e. parts of speech)
"""
import discord
from discord.ext import commands
import functions_en
import random


class Grammar:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def isword(self, word="can you specify an actual word?"):
        if functions_en.is_word(word):
            await self.client.say("'{}' is an English word.".format(word))
        else:
            await self.client.say("'{}' is not an English word.".format(word))

    @commands.command()
    async def adj(self, syllables=None):
        if not syllables:
            syllables = random.randint(1, 4)
        try:
            syllables = int(syllables)
            if not syllables:
                syllables = random.randint(1, 4)
            elif syllables > 4:
                await self.client.say("Sorry, I'm not that smart yet.")
                await self.client.say("I only know up to four syllables.")
            elif syllables < 0:
                await self.client.say("What do you mean?")
            if 0 < syllables <= 4:
                await self.client.say("Here's an adjective!")
                await self.client.say(" > {}".format(functions_en.new_adjective(syllables)))
        except ValueError as err:
            print(err)
            await self.client.say("That doesn't seem right.")
            await self.client.say("Correct usage: _adj syllables(1 to 4)")
            await self.client.say("Example: _adj 3")

    @commands.command()
    async def adv(self, syllables=None):
        if not syllables:
            syllables = random.randint(1, 4)
        try:
            syllables = int(syllables)
            if syllables == 0:
                syllables = random.randint(1, 4)
            elif syllables > 4:
                await self.client.say("Sorry, I'm not that smart yet.")
                await self.client.say("I only know up to four syllables.")
            elif syllables < 0:
                await self.client.say("What do you mean?")
            if 0 < syllables <= 4:
                await self.client.say("Here's an adverb!")
                await self.client.say(" > {}".format(functions_en.new_adverb(syllables)))
        except ValueError as err:
            print(err)
            await self.client.say("That doesn't seem right.")
            await self.client.say("Correct usage: _adv syllables(1 to 4)")
            await self.client.say("Example: _adv 2")


    @commands.command()
    async def noun(self, syllables=None):
        if not syllables:
            syllables = random.randint(1, 4)
        try:
            syllables = int(syllables)
            if syllables == 0:
                syllables = random.randint(1, 4)
            elif syllables > 4:
                await self.client.say("Sorry, I'm not that smart yet.")
                await self.client.say("I only know up to four syllables.")
            elif syllables < 0:
                await self.client.say("What do you mean?")
            if 0 < syllables <= 4:
                await self.client.say("Here's a noun!")
                await self.client.say(" > {}".format(functions_en.new_noun(syllables)))
        except ValueError as err:
            print(err)
            await self.client.say("That doesn't seem right.")
            await self.client.say("Correct usage: _noun syllables(1 to 4)")
            await self.client.say("Example: _noun 4")


    @commands.command()
    async def verb(self, syllables=None):
        if not syllables:
            syllables = random.randint(1, 4)
        try:
            syllables = int(syllables)
            if syllables == 0:
                syllables = random.randint(1, 4)
            elif syllables > 4:
                await self.client.say("Sorry, I'm not that smart yet.")
                await self.client.say("I only know up to four syllables.")
            elif syllables < 0:
                await self.client.say("What do you mean?")
            if 0 < syllables <= 4:
                await self.client.say("Here's a verb!")
                await self.client.say(" > {}".format(functions_en.new_verb(syllables)))
        except ValueError as err:
            print(err)
            await self.client.say("That doesn't seem right.")
            await self.client.say("Correct usage: _verb syllables(1 to 4)")
            await self.client.say("Example: _verb 1")



def setup(client):
    client.add_cog(Grammar(client))
