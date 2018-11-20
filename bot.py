#!python3
import discord
from discord.ext import commands
import random
import functions_en
import asyncio
import sys

with open("misc/thing.txt") as inFile:
    TOKEN = inFile.readline().strip()

client = commands.Bot(command_prefix='_')

extensions = ['custom_texts', 'grammar', 'games']
client.remove_command('help')


@client.event
async def on_ready():
    print("Lexi initialized")
    await client.change_presence(game=discord.Game(name='your _help', type=2))

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} extension failed to load. [{}]'.format(extension, error))
        else:
            print("{} has successfully loaded.".format(extension))


@client.event
async def on_message(message):
    """
    Event whenever a message is sent
    :param message:
    :return:
    """
    bads = ["kcuf", "tihs", "ssa", "eid", "yag", "aggin"]
    author = message.author
    content = str(message.content).lower().strip().split()
    channel = message.channel
    if len(content) > 0 and str(author) != "Lexi#2892":
        if content[0] == "lexi":
            if len(content) == 1:
                await client.send_message(channel, "Hi, <@{}>!".format(author.id))
            elif content[1] == "should" or content[1] == "am" or content[1] == "will" or content[1] == "is":
                chance = random.randint(1, 2)
                if chance == 1:
                    await client.send_message(channel, "I think so.")
                else:
                    await client.send_message(channel, "I don't think so.")
            else:  # sentence length more than 1
                for word in bads:
                    if word[::-1] in content:
                        adj = functions_en.random_from_txt("texts/negative_adjectives.txt").lower()
                        await client.send_message(channel, "Hey, <@{}>, that sounds pretty {}.".format(author.id, adj))
        elif content[0] == "yes":
            await client.send_message(channel, "indeed.")
        elif content[0] == "maybe":
            chance = random.randint(1, 6)
            if chance == 1:
                await client.send_message(channel, "What if you do?")
            elif chance == 2:
                await client.send_message(channel, "You shouldn't..")
            elif chance == 3:
                await client.send_message(channel, "Ask Siri, my dude.")
            elif chance == 4:
                await client.send_message(channel, "Try it!")
            elif chance == 5:
                await client.send_message(channel, "Alexa, answer <@{}>'s doubts.".format(author.id))
            elif chance == 6:
                await client.send_message(channel, "You probably shouldn't..")
        elif content[0] == "welp" or (content[0] == "oh" and content[1] == "well"):
            await client.send_message(channel, "¯\_(ツ)_/¯")

    await client.process_commands(message)


@client.event
async def on_message_delete(message):
    """
    Event whenever a message is deleted
    :param message:
    :return:
    """
    author_id = message.author.id
    content = message.content
    channel = message.channel
    await client.send_message(channel, "Woah, <@{}> deleted a message o.o".format(author_id))


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    author_id = author.id
    channel = ctx.message.channel

    embed = discord.Embed(
        color=discord.Color.dark_magenta(),
        title="Replace the parentheses with your command arguments.",
        description="ex: _shuffle This message will be shuffled."
    )

    embed.set_author(name="Here's what I know:\n")

    embed.add_field(name="======================| General |======================", value="Some basic, generic commands", inline=False)
    embed.add_field(name="[:grey_question:] _help", value="displays this message", inline=True)
    embed.add_field(name="[:ping_pong:] _ping", value="Pong!", inline=True)
    embed.add_field(name="[:speech_balloon:] _echo (message)", value="echoes the message back", inline=False)

    embed.add_field(name="====================| Custom Texts |====================", value="Use these commands to generate custom messages!", inline=False)
    embed.add_field(name="[:arrow_backward:] _reverse (message)", value="reverses the word order in a sentence", inline=True)
    embed.add_field(name="[:arrow_left:] _reverseall (message)", value="reverses every letter in a sentence", inline=True)
    embed.add_field(name="[:game_die:] _shuffle (message)", value="randomizes the word order \n in a sentence", inline=True)
    embed.add_field(name="[:twisted_rightwards_arrows:] _shuffleall (message)", value="randomizes the letters of each word \n in a sentence", inline=True)
    embed.add_field(name="[:fire:] _shufflechaos (message)", value="randomizes the letters of each word and sentence order", inline=True)
    embed.add_field(name="[:lips:] _rant ([topic?], [lines?], [tts?])", value="apparently self-generated poems become off topic extremely quickly. \n"
                    "set the topic to '?' or empty for a randomly generated topic. \n "
                    "set the tts variable to 'tts' if you want text to speech. otherwise, leave it empty.",
                    inline=True)

    embed.add_field(name="======================| Grammar |======================",
                    value="Here are some commands pertaining to English grammar.", inline=False)
    embed.add_field(name="[:small_blue_diamond:] _adj ([syllables?])", value="here's a random adjective!", inline=True)
    embed.add_field(name="[:small_blue_diamond:] _adv ([syllables?])", value="here's a random adverb!", inline=True)
    embed.add_field(name="[:small_blue_diamond:] _noun ([syllables?])", value="here's a random noun!", inline=True)
    embed.add_field(name="[:small_blue_diamond:] _verb ([syllables?])", value="here's a random verb!", inline=True)
    embed.add_field(name="[:closed_book:] _isword (word)", value="check to see if the word is an English word.", inline=True)

    embed.add_field(name="=======================| Fun! |=======================", value="It looks like my game packages have shipped with me too!", inline=False)
    embed.add_field(name="[:raising_hand:] _opinion (word)", value="what do you think about something? \n what do you think lexi thinks about something?", inline=True)
    embed.add_field(name="[:point_right:] _yomamma @(user)", value="can't think of a good insult? I gotcha.", inline=True)
    embed.add_field(name="[:package:] _mysterybox", value="feeling lucky? good guesser?", inline=True)

    embed.set_footer(text="Note: [asdf?]: this indicates an optional* value for a command")

    print("Help sent to {}".format(author))
    await client.send_message(channel, "<@{}>, here's some literature!".format(author_id))
    await client.send_message(author, "Glad you asked!")
    await client.send_message(author, embed=embed)
    await client.send_message(author, "Feel free to test these commands in this conversation!")


@client.command()
async def ping():
    await client.say("Pong!")


@client.command()
async def echo(*args):
    s = []
    for i in args:
        s.append(i)
    if len(s) == 0:
        await client.say("Doesn't seem like I have anything to echo.")
    else:
        output = " ".join(s)
        await client.say(output)

client.run(TOKEN)
