"""
BOT COG: Commands which generate or alter text
"""
import discord
from discord.ext import commands
import functions_en
import poem
import random
import asyncio

on_remote_output = False
with open("misc/private_channel.txt") as inFile:
    private_channel = inFile.readline().strip()
to_send = ""


class CustomTexts:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reverseall(self, *args):
        s = ""
        for i in args:
            s += " "
            for j in i:
                s += j
        if s == "":
            await self.client.say("Can you give me something to reverse?"[::-1])
        else:
            s = s[::-1]
            print("reverseall {}".format(s))
            await self.client.say(s)

    @commands.command()
    async def reverse(self, *args):
        arr = []
        for i in args:
            arr.append(i)
        if len(arr) == 0:
            msg = "Can you give me something to reverse?".split()
            msg.reverse()
            await self.client.say(" ".join(msg))
        else:
            arr.reverse()
            arr = " ".join(arr)
            print("reverse {}".format(arr))
            await self.client.say(arr)

    @commands.command()
    async def shufflechaos(self, *args):
        """
        shuffle every word in a sentence and shuffling the sentence order
        :param args:
        :return:
        """
        arr = []
        output = []
        for i in args:
            arr.append(i)
        if len(arr) == 0:
            await self.client.say("Can you give me something to shuffle?")
        else:
            random.shuffle(arr)
            for i in arr:
                new_word = list(i)
                random.shuffle(new_word)
                output.append("".join(new_word))
            await self.client.say(" ".join(output))

    @commands.command()
    async def shuffleall(self, *args):
        """
        shuffle every word in a sentence, retaining the sentence order
        :param args:
        :return:
        """
        arr = []
        output = []
        for i in args:
            arr.append(i)
        if len(arr) == 0:
            await self.client.say("Can you give me something to shuffle?")
        else:
            for i in arr:
                new_word = list(i)
                random.shuffle(new_word)
                output.append("".join(new_word))
            await self.client.say(" ".join(output))

    @commands.command()
    async def shuffle(self, *args):
        """
        shuffles the sentence structure of the input
        :param args:
        :return:
        """
        arr = []
        for i in args:
            arr.append(i)
        if len(arr) == 0:
            await self.client.say("Can you give me something to shuffle?")
        else:
            random.shuffle(arr)
            await self.client.say(" ".join(arr))

    @commands.command()
    async def rant(self, subject="?", lines=None, tts=None):
        if not lines:
            lines = 4
        try:
            lines = int(lines)
            subject = str(subject)
            if lines < 3:
                await self.client.say("I need more lines to rant on {}.".format(lines))
                await self.client.say("Try using more than 2 lines.")
            else:
                poem_instance = poem.Poem(lines, subject)
                poem_instance.rant()
                s = poem_instance.content
                print("Rant created about {}".format(poem_instance.subject))
                # poem_instance.recite()
                if tts == "tts":
                    if lines < 15:
                        await self.client.say('"About the {}" (ALOUD)'.format(poem_instance.subject))
                        await self.client.say("\n".join(s), tts=True)
                    else:
                        await self.client.say("Well, wouldn't that be annoying?")
                else:
                    if lines < 30:
                        await self.client.say('"About the {}"'.format(poem_instance.subject))
                        await self.client.say("\n".join(s))
                    else:
                        await self.client.say("Well, wouldn't that be annoying?")
        except ValueError as err:
            await self.client.say("That doesn't make sense.")
            await self.client.say("Correct usage: _rant subject lines")
            await self.client.say("Example: _rant debugging 8")

    async def on_message(self, message):
        channel = str(message.channel)
        global private_channel
        global on_remote_output
        global to_send
        if private_channel == channel and on_remote_output == True and message.content != "_remoteoutput":
            print("'{}' sent!".format(message.content))
            to_send = message.content

    @commands.command(pass_context=True)
    async def remoteoutput(self, ctx):
        author_id = ctx.message.author.id
        channel = ctx.message.channel
        print("Throwing messages over to {}".format(channel))
        global on_remote_output
        global to_send
        if str(author_id) == "282031512713560064":  # only Fongii
            on_remote_output = not on_remote_output
            if on_remote_output:
                print("Now Lexi will take input from the private channel.")
            else:
                print("Lexi's remote input is turned off.")
            while on_remote_output:
                await asyncio.sleep(0.1)
                if to_send != "":
                    await self.client.say(to_send)
                    to_send = ""


def setup(client):
    client.add_cog(CustomTexts(client))
