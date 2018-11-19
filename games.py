"""
BOT COG: Commands which relate to games, miscellaneous behavior
"""
import discord
from discord.ext import commands
import functions_en as en
import random
import asyncio

mystery_box_queue = dict()


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

    @commands.command(pass_context=True)
    async def mysterybox(self, ctx):
        player = ctx.message.author
        player_id = player.id
        channel = ctx.message.channel
        if player_id not in mystery_box_queue:
            await self.client.say("<@{}> : Guess which box I am thinking of!".format(player_id))
            await self.client.say("[:one:] [:two:] [:three:] [:four:] [:five:]")
            correct = random.randint(1, 5)
            hint_chance = random.randint(1, 3)
            if hint_chance == 2:
                if correct % 2 == 0:
                    num_type = "even"
                else:
                    num_type = "odd"
                await self.client.say("I'm feeling pretty generous today!")
                await self.client.say("<@{}> : The box is an {} number".format(player_id, num_type))
            mystery_box_queue[player_id] = [False, correct, False]  # Hasn't guessed, correct box, is guilty
            print(mystery_box_queue)
            for i in range(700):
                await asyncio.sleep(0.01)
                if mystery_box_queue[player_id][0]:
                    await self.client.say("Wow! You're correct!")
                    await self.client.say("<@{}> : Give me some time to open it..".format(player_id))
                    await asyncio.sleep(0.1)
                    msg = await self.client.say(":package:")
                    await asyncio.sleep(1.5)
                    await self.client.edit_message(msg, ":hourglass_flowing_sand:")
                    await asyncio.sleep(2.3)
                    await self.client.edit_message(msg, ":hourglass:")
                    await asyncio.sleep(1.9)
                    await self.client.edit_message(msg, ":unlock:")
                    reward = en.random_from_txt("texts/materials.txt")
                    await self.client.say("<@{}> : O.O You just received a new {}!".format(player_id, reward))
                    adj = en.random_from_txt("texts/positive_adjectives.txt").lower()
                    await self.client.say("<@{}> : Your gift seems pretty {}. Pretty jealous tbh.".format(player_id, adj))
                    break
                elif mystery_box_queue[player_id][2]:
                    break
            else:
                await self.client.say("<@{}> : Time's up!".format(player_id))
                await self.client.say("I guess you won't find out what's in the mystery box.")
            mystery_box_queue.pop(player_id, None)
            print(mystery_box_queue)
        else:
            await self.client.say("You're already guessing, <@{}>!".format(player_id))

    async def on_message(self, message):
        author = message.author
        author_id = message.author.id
        content = str(message.content)
        channel = message.channel
        try:
            if author_id in mystery_box_queue.keys() and content != "_mysterybox":
                if int(content) == mystery_box_queue[author_id][1]:
                    mystery_box_queue[author_id][0] = True
                    # put something that is in the box
                else:
                    if mystery_box_queue[author_id][1] == 1:
                        ans = ":one:"
                    elif mystery_box_queue[author_id][1] == 2:
                        ans = ":two:"
                    elif mystery_box_queue[author_id][1] == 3:
                        ans = ":three:"
                    elif mystery_box_queue[author_id][1] == 4:
                        ans = ":four:"
                    else:
                        ans = ":five:"
                    await self.client.send_message(channel, "Sorry, the correct box was number [{}].".format(ans))
                    mystery_box_queue[author_id][2] = True
        except ValueError:
            if not mystery_box_queue[author_id][0]:
                mystery_box_queue[author_id][2] = True
                await self.client.send_message(channel, "That doesn't make sense.")
                await self.client.send_message(channel, "I guess you won't find out what's in the mystery box.")


def setup(client):
    client.add_cog(Games(client))
