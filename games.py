"""
BOT COG: Commands which relate to games, miscellaneous behavior
"""
import discord
from discord.ext import commands
import functions_en as en
import random
import asyncio
import json

mystery_box_queue = dict()
madlibs_queue = dict()
ispy_ref = dict()
ispy_topics = [
    ["https://github.com/cnfgsean/Lexi/blob/master/ispy/pexels-photo-1643324.jpeg?raw=true",
     [[["sweet"], ["strawberry"]],
      [["circular"], ["lemon"]]]
     ]
]


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
    async def rps(self, ctx, choice=None):
        author = ctx.message.author
        author_id = author.id
        valid_choices = [
            ["rock", "r", "1"],
            ["paper", "p", "2"],
            ["scissors", "s", "3"]
        ]
        choice = str(choice).lower()
        # picking the user's choice
        if choice in valid_choices[0]:
            choice = 1
        elif choice in valid_choices[1]:
            choice = 2
        elif choice in valid_choices[2]:
            choice = 3
        else:
            await self.client.say("<@{}> : I'm not sure that's a valid choice.".format(author_id))
            await self.client.say("I'll just pick something for you, then!")
            item_chance = random.randint(1, 3)
            if item_chance == 1:
                choice = 1
            elif item_chance == 2:
                choice = 2
            else:
                choice = 3

        # picking the bot's choice
        lexi_choice = random.randint(1, 3)

        # picking the emojis
        if choice == 1:
            emoji = ":fist:"
            literal = "rock"
        elif choice == 2:
            emoji = ":hand_splayed:"
            literal = "paper"
        else:
            emoji = ":v:"
            literal = "scissors"

        # picking the emojis
        if lexi_choice == 1:
            lexi_emoji = ":fist:"
            lexi_literal = "rock"
        elif lexi_choice == 2:
            lexi_emoji = ":hand_splayed:"
            lexi_literal = "paper"
        else:
            lexi_emoji = ":v:"
            lexi_literal = "scissors"

        # comparing choices
        embed = discord.Embed(
            color=discord.Color.dark_teal()
        )
        if ctx.message.server:
            user = ctx.message.server.get_member(author_id)
            pfp = user.avatar_url
            embed.set_author(name="{}'s match".format(str(author).split("#")[0]), icon_url=pfp)
        if choice == lexi_choice:  # P L   1, 1   2, 2   3, 3
            embed.add_field(name="*Here are the results!*", value="<@{}>   **{}** {} :left_right_arrow: {} **{}**   <@512442583142760465>".format(author_id, literal, emoji, lexi_emoji, lexi_literal), inline=False)
            await self.client.say(embed=embed)
            await self.client.say("<@{}> : Looks like it's a tie!".format(author_id))
        elif (choice == 1 and lexi_choice == 2) or (choice == 2 and lexi_choice == 3) or(choice == 3 and lexi_choice == 1):  # P L   1, 2   2, 3   3, 1  Lexi wins
            embed.add_field(name="*Here are the results!*", value="<@{}>   **{}** {} :arrow_left::arrow_left: {} **{}**   <@512442583142760465>".format(author_id, literal, emoji, lexi_emoji, lexi_literal), inline=False)
            await self.client.say(embed=embed)
            await self.client.say("<@{}> : Looks like I win!".format(author_id))
        else:  # P L   1, 3   3,2   2,1
            embed.add_field(name="*Here are the results!*", value="<@{}>   **{}** {} :arrow_right::arrow_right: {} **{}**   <@512442583142760465>".format(author_id, literal, emoji, lexi_emoji, lexi_literal), inline=False)
            await self.client.say(embed=embed)
            await self.client.say("<@{}> : Looks like you win Congrats!!".format(author_id))

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
            if hint_chance != 2:
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

    # TODO: add a madlibs game!
    @commands.command(pass_context=True)
    async def madlibs(self, ctx):
        author = ctx.message.author
        author_id = author.id
        channel = ctx.message.channel
        if ctx.message.content != "_madlibs":
            await self.client.say("That doesn't make sense.")
            await self.client.say("Just say **_madlibs** without any other arguments after it.")
            return
        if author_id not in madlibs_queue.keys():
            print(madlibs_queue)
            script = en.random_from_txt("texts/mad_libs.txt").split("&")  # TODO for manual changing
            print(script)
            items = int(script[0])
            text = script[1].split()
            title = script[2]
            madlibs_queue[author_id] = [False, False, items, [], [], 0]  # finished, has asked, items left, prompts, answers, timer
            await self.client.say("Great choice, <@{}>! Let's begin.".format(author_id))
            await self.client.say("Say **lexi stop**, **_cancel**, or one of my commands (i.e. _ping) if you wish to cancel.")
            await self.client.say("Note: You can use **_ignore (message that I will ignore)** if you want to talk to other people while you are playing.")
            await self.client.say("Seems like my random choice picked **{}** for you madlibs!".format(title))
            # print(items)
            # print(text)
            # print(madlibs_queue)
            for i in text:
                word = i.split("~")
                if word[0][0] == "%":
                    """
                    noun, plural_noun, verb, verb_ing, body_part, adjective, name_female
                    """
                    if word[0] == "%noun":
                        madlibs_queue[author_id][3].append("noun")
                    elif word[0] == "%plural_noun":
                        madlibs_queue[author_id][3].append("plural noun")
                    elif word[0] == "%verb":
                        madlibs_queue[author_id][3].append("verb")
                    elif word[0] == "%verb_s":
                        madlibs_queue[author_id][3].append("verb ending with 's'")
                    elif word[0] == "%verb_ing":
                        madlibs_queue[author_id][3].append("verb ending with 'ing'")
                    elif word[0] == "%body_part":
                        madlibs_queue[author_id][3].append("body part")
                    elif word[0] == "%adjective":
                        madlibs_queue[author_id][3].append("adjective")
                    elif word[0] == "%adverb":
                        madlibs_queue[author_id][3].append("adverb")
                    elif word[0] == "%name_female":
                        madlibs_queue[author_id][3].append("female name")
                    else:
                        madlibs_queue[author_id][3].append("[anything! there seems to be something wrong with the code.]")
            print(madlibs_queue.keys())
            for madlibs_queue[author_id][5] in range(10000000):
                # print(madlibs_queue[author_id][5])
                await asyncio.sleep(0.01)
                if madlibs_queue[author_id][2] > 0:
                    if not madlibs_queue[author_id][1]:  # if lexi hasn't asked
                        await self.client.say("**{}** more word(s) left. <@{}>, can you give me a(n) {}?".format(madlibs_queue[author_id][2], author_id, madlibs_queue[author_id][3][items - madlibs_queue[author_id][2]]))
                        madlibs_queue[author_id][1] = True
                else:
                    madlibs_queue[author_id][0] = True
                    count = 0
                    pre_output = []
                    for j in text:
                        word = j.split("~")
                        if word[0][0] == "%":
                            if len(word) == 2:  # has punctuation
                                pre_output.append(madlibs_queue[author_id][4][count] + word[1])
                            else:
                                pre_output.append(madlibs_queue[author_id][4][count])
                            count += 1
                        else:
                            pre_output.append(j)
                    post_output = " ".join(pre_output).split(".")
                    await self.client.say("<@{}> Congratulations for finishing your madlibs!".format(author_id))
                    comment_chance = random.randint(1, 5)
                    if comment_chance == 1:
                        comment = "Can't wait for you to read this!"
                    elif comment_chance == 2:
                        comment = "This had me laughing so hard."
                    elif comment_chance == 3:
                        comment = "Here is the result! Enjoy reading!"
                    elif comment_chance == 4:
                        comment = "I can't keep my mouth shut after reading this!"
                    elif comment_chance == 5:
                        comment = "This actually is pretty nice!"
                    else:
                        comment = "LMAO. MUST READ"
                    await self.client.say(comment)
                    await self.client.say("__**{}** (Madlibs)__".format(title))
                    await self.client.say(".\n".join(post_output))
                if madlibs_queue[author_id][0]:
                    break
                if madlibs_queue[author_id][5] == 9999999:
                    await self.client.say("Can't make up your mind, <@{}>?".format(author_id))
                    await self.client.say("Stopping and cancelling the madlibs game.")

            madlibs_queue.pop(author_id, None)
            print(madlibs_queue)
        else:
            await self.client.say("<@{}>, you're already playing!".format(author_id))

    # TODO: add a countries game!
    @commands.command(pass_context=True)
    async def ispy(self, ctx):
        channel = ctx.message.channel
        content = ctx.message.content
        server = ctx.message.server
        if (server, channel) in ispy_ref.keys():
            if str(content) == "_ispy new":
                ispy_ref.pop((server, channel), None)
            elif str(content) == "_ispy show":
                embed = discord.Embed(
                    title="Here it is again!",
                    color=discord.Color.dark_teal()
                )
                ispy_hint = ispy_ref[(server, channel)][1][0]
                ispy_image = ispy_ref[(server, channel)][0]
                print(ispy_hint, ispy_image)
                embed.add_field(name="Topic:", value="I spy with my digital eye something " + ispy_hint)
                embed.set_image(url=ispy_image)
                await self.client.say(embed=embed)
            else:
                await self.client.say("There already is an ispy game in this channel!")
        if (server, channel) not in ispy_ref.keys():
            ispy_topic = random.choice(ispy_topics)  # TODO: incorporate answer in the mass array
            ispy_image = ispy_topic[0]
            ispy_choice = random.choice(ispy_topic[1])
            ispy_hint = ispy_choice[0]
            ispy_answer = ispy_choice[1]
            embed = discord.Embed(
                title="Good luck!",
                color=discord.Color.dark_teal()
            )
            embed.add_field(name="Topic:", value="I spy with my digital eye something " + ispy_hint[0])
            embed.set_image(url=ispy_image)
            await self.client.say(embed=embed)
            ispy_ref[(server, channel)] = [ispy_image, ispy_hint, ispy_answer]  # URL, embed
            print(ispy_choice)
            print(ispy_ref)

    async def on_message(self, message):
        author = message.author
        author_id = message.author.id
        content = str(message.content).strip()
        channel = message.channel
        try:
            if author_id in mystery_box_queue.keys() and content != "_mysterybox":
                if int(content) == mystery_box_queue[author_id][1]:
                    mystery_box_queue[author_id][0] = True
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

        if author_id in madlibs_queue.keys() and content != "_madlibs":
            if content[0] == "_":
                if content == "_noun" or content == "_adj" or content == "_adv" or content == "_verb":
                    pass
                elif content[0:7] == "_ignore":
                    pass
                else:
                    madlibs_queue[author_id][0] = True
                    await self.client.send_message(channel, "I see you tried using a command.")
                    await self.client.send_message(channel, "<@{}> : Madlibs cancelled.".format(author_id))
            elif content == "lexi stop" or content == "Lexi stop":
                madlibs_queue[author_id][0] = True
                await self.client.send_message(channel, "Stopping and cancelling the madlibs game.")
                await self.client.send_message(channel, "Try it again later, <@{}>!".format(author_id))
            elif madlibs_queue[author_id][1]:
                madlibs_queue[author_id][4].append("__" + content + "__")
                madlibs_queue[author_id][2] -= 1
                madlibs_queue[author_id][1] = False


def setup(client):
    client.add_cog(Games(client))
