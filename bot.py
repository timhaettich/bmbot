"""
Blackmagic Design Discord Community bot
Version 1.0.1
Written by TimothyLH
With additions by Dave Caruso

ChangeLog:
v1.0.0
Introduces a basic set of functions
"""
VERSIONNR = "1.0.1"
#Import Libraries and Env-Variables
import os
import random
import psutil
import discord
import urllib
import re
from dotenv import load_dotenv

#Import Custom Code
from bmd_crawler.interface import allVisibleResolveVersionNames,getResolveVersionData,getResolveLatestData,allResolveVersionNames,allVisibleFusionVersionNames,getFusionVersionData,getFusionLatestData,allFusionVersionNames
from functions import HelpFunctions
from const import *

print('Trying to start')

#Load Bot Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))
RULES = int(os.getenv('CHANNEL_RULES'))
TERMINAL = int(os.getenv('CHANNEL_TERMINAL'))
ROLES = int(os.getenv('CHANNEL_ROLES'))

print(GUILD)


#Create bot
from discord.ext import commands

bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX') + " ")

#Get Help functions
f = HelpFunctions(bot,GUILD)

#--- START UP CODE ---------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! Discord.py Version: {discord.__version__}')
    print('Currently running at CPU: {0} RAM: {1}'.format(psutil.cpu_percent(), psutil.virtual_memory()[2]))

    await bot.change_presence(activity=discord.Game(name='DaVinci Resolve'))


#--- Welcome Message -------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    await bot.get_channel(RULES).send(
        '{0} {1.mention}, welcome to the Blackmagic Community! Please read the rules and assign yourself {2}. Type _!bmd help_ and _!bmd channels_ to get a quick introduction'
        .format(f.emoji('bmd'),
        member,
        bot.get_channel(ROLES).mention),
        delete_after = float("30")
    )
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Blackmagic Community! Please note that we use diffrent channels for diffrent things, you can see an overview below:'
    )
    await member.dm_channel.send(embed=f.channel_help())

#--- PING PONG -------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="ping", description="Use this command to see if the bot is online")
async def on_command(ctx):
    replays = [
        "Pong!", "No! I'm better than just writting 'Pong'", "Pong... ee. Hah you didn't expect this one. No seriously get yourself a warm blanket, it's cold outside!", "Stop pinging me! I want to sleep", "Dude stop pinging me! I'm presenting the new Blackmagic Not Anymore Pocket Cinema Camera 8k",
        f"Better ping gooogle than me. My current ping to Google is: {random.randint(1,10)}", "You expected me to say Pong! And so I did...", f"Pingreeeeee {f.emoji('PeepoPing')}",
        "Ping? Ping! I will tell you who I ping next!", "Ping, Pong, Ping, Pong, Ping, Pong, Ping, Pong... That's the last Ping Pong Championship summarized", "Ping!", "async def ping(ctx):\n    await ctx.channel.send('Pong')"
    ]
    await ctx.channel.send(random.choice(replays))

#--- Swiss Text ------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="swiss", hidden="true")
async def on_command(ctx):
    swissgerman = [
        "Huere Michi Grind", "Schafsäcku", "Degenerierts Layer-8-Phänomen", "Spezifikations-GAU", "Grachteschnäpfe", "Gopfverdammi", "Shit!", "Scheisse", "Dummi Chueh", "Gopferdecku", "Schofseckel", "Gwaggli", "Gumslä", "Sürel", "Habasch", "Halbschue", "Täschbäsä", "Chotzbrocke", "Totsch", "Tschumpel", "Säuniggel"
    ]
    await ctx.channel.send(random.choice(swissgerman))

#--- Rules -----------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='rule', help='Displays the selected rule. Do not give a number to get a general warning. Give a username to warn a specific user.')
async def on_command(ctx, id: int):
    if id == 1:
        msg = '1️⃣ Respect other users and their opinions. No impersonation. No racism, sexism, transphobia, homophobia, etc. Your race does not give you a pass to say slurs freely. Rules apply to everyone!'
    elif id == 2:
        msg = '2️⃣ We are a filmmaking discord, not a debate club. Please keep controversy about politics, religion, etc. out of here.'
    elif id == 3:
        msg = '3️⃣ English is the universal standard language.  Any sort of conversation in a foreign language is strictly prohibited. Most of our staff speak English so its not easy to tell if you\'re breaking the rules in another language. Violation of this could end on a mute or warning.'
    elif id == 4:
        msg = '4️⃣ No spamming of any kind. Please be polite to other users and do not be disruptive. Includes but is not limited to nicknames, text, emoji, links, images, EXCESSIVE CAPS, censor dodging (eg. use of spoilers), and spam mentioning @ role/user. Do not pointlessly ping Official Blackmagic Design Staff members for questions others can answer.'
    elif id == 5:
        msg = '5️⃣ Content sharing is allowed.\nPost your work in {0} \nPost your gear in {1} \nKeep memes in {2} strictly.'.format(bot.get_channel(YOURWORK).mention, bot.get_channel(YOURGEAR).mention, bot.get_channel(OFFTOPIC).mention)
    elif id == 6:
        msg = '6️⃣ No loopholes. A loophole is when you try to find technicalities in the rules so you don\'t get punished for what you did.  If you ever find any loopholes then report them to a staff member to be fixed.  Loopholes will not be tolerated and are strictly prohibited.'
    elif id == 7:
        msg = '7️⃣ Keep all your drama out of this server. If you have any sort of an issue with another member then you can simply block them and move on or make an attempt at making amends in private messages (DMs).  Anywhere but this server is the place for you to do this. Violation of this rule will most likely lead to a mute or ban.'
    else:
        msg = '⚠️ Please follow the rules. You can find them in {0}'.format(bot.get_channel(RULES).mention)
    await ctx.channel.send(msg)

#--- Channel help ----------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='channels', help='Displays you a summary of all channels and what they do')
async def on_command(ctx):
    await ctx.send(embed=f.channel_help())

#--- Resolve ---------------------------------------------------------------------------------------------------------------------------------------------------
def resolveEmoji():
    try:
        return discord.utils.get(bot.get_guild(GUILD).emojis, name='resolve');
    except:
        return ':resolve:'

def create_download_markdown(downloads):
    if downloads == None:
        return 'Not Available'
    string = ''
    if 'windows' in downloads:
        string += f"\n[Windows]({downloads['windows']})"
    if 'mac' in downloads:
        string += f"\n[MacOS]({downloads['mac']})"
    if 'linux' in downloads:
        string += f"\n[Linux]({downloads['linux']})"
    if string == '':
        return 'Not Available'
    else:
        return string[1:]


async def send_resolve_version_embed(ctx, release):
    embed = discord.Embed(title="DaVinci Resolve " + release['version'], description=release['shortDescription'], color=0xff8000, url=release['readMoreURL'])
    embed.set_footer(text="The staff does not take any responsibility for the above links.")
    embed.add_field(name="Resolve Free", value=create_download_markdown(release['downloads']['free']))
    embed.add_field(name="Resolve Studio", value=create_download_markdown(release['downloads']['studio']))
    embed.add_field(name=f'Recent Versions:', value='** / **'.join(allVisibleResolveVersionNames()))
    await ctx.send(embed=embed)
async def send_fusion_version_embed(ctx, release):
    embed = discord.Embed(title="Blackmagic Fusion " + release['version'], description=release['shortDescription'], color=0xff8000, url=release['readMoreURL'])
    embed.set_footer(text="The staff does not take any responsibility for the above links.")
    embed.add_field(name="Fusion Free", value=create_download_markdown(release['downloads']['free']))
    embed.add_field(name="Fusion Studio", value=create_download_markdown(release['downloads']['studio']))
    embed.add_field(name=f'Recent Versions:', value='** / **'.join(allVisibleFusionVersionNames()))
    await ctx.send(embed=embed)

@bot.command(name='resolve', help='Gives your the Download Link for the specified DaVinci Resolve Version. Leave empty to get the newest non-beta Release. Enter _!bmd resolve list_ to get a list of all available versions')
async def on_command(ctx, version=None, flag=None):
    if version == None:
        msg = str(resolveEmoji()) + 'No version provided, so here\'s the latest version of resolve.'
        await ctx.channel.send(msg)
        await send_resolve_version_embed(ctx, getResolveLatestData())
        return

    data = getResolveVersionData(version)
    if data != None:
        await send_resolve_version_embed(ctx, data)
    elif version == 'list':
        if flag == '-a':
            msg = str(resolveEmoji()) + 'Listing ***ALL*** available versions of DaVinci Resolve.\n```'
            versionNames = allResolveVersionNames()
        else:
            msg = str(resolveEmoji()) + 'Listing recent versions of DaVinci Resolve.\n```'
            versionNames = allVisibleResolveVersionNames()
        col = -1
        for version in versionNames:
            col += 1
            if col == 5:
                col = 0
                msg += '\n'
            msg += version + '        '[len(version):]
        msg += "\n```"
        await ctx.channel.send(msg)
    else:
        msg = str(resolveEmoji()) + 'Uh oh, that version of DaVinci Resolve doesn\'t exist. Here\'s the latest one.'
        await ctx.channel.send(msg)
        await send_resolve_version_embed(ctx, getResolveLatestData())

#--- Fusion ----------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='fusion', help='Gives your the Download Link for the specified Fusion Version. Leave empty to get the newest non-beta Release. Enter _!bmd fusion list_ to get a list of all available versions')
async def on_command(ctx, version=None, flag=None):
    if version == None:
        msg = str(resolveEmoji()) + 'No version provided, so here\'s the latest version of resolve.'
        await ctx.channel.send(msg)
        await send_fusion_version_embed(ctx, getResolveLatestData())
        return

    data = getFusionVersionData(version)
    if data != None:
        await send_fusion_version_embed(ctx, data)
    elif version == 'list':
        if flag == '-a':
            msg = str(resolveEmoji()) + 'Listing ***ALL*** available versions of Fusion.\n```'
            versionNames = allFusionVersionNames()
        else:
            msg = str(resolveEmoji()) + 'Listing recent versions of Fusion.\n```'
            versionNames = allVisibleFusionVersionNames()
        col = -1
        for version in versionNames:
            col += 1
            if col == 5:
                col = 0
                msg += '\n'
            msg += version + '        '[len(version):]
        msg += "\n```"
        await ctx.channel.send(msg)
    else:
        msg = str(resolveEmoji()) + 'Uh oh, that version of Fusion doesn\'t exist. Here\'s the latest one.'
        await ctx.channel.send(msg)
        await send_fusion_version_embed(ctx, getResolveLatestData())

#--- Compliment ------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='compliment', help='Gives the tagges person a compliment')
async def on_command(ctx, user: discord.Member):
    compliments = [
        "You're doing great!", "You're awesome!", "Great filmmaker!", "Nice to see you!", "Nice camera!","You're that “Nothing” when people ask me what I'm thinking about.", "You look great today.", "You're a smart cookie.", "I bet you make babies smile.", "You have impeccable manners.", "I like your style.", "You have the best laugh.", "I appreciate you.", "You're an awesome friend.", "You're a gift to those around you.", "You're a smart cookie.", "You are awesome!", "You have impeccable manners.", "I like your style.", "You have the best laugh.", "I appreciate you.", "You are the most perfect you there is.", "You are enough.", "You're strong.", "Your perspective is refreshing.", "I'm grateful to know you.", "You light up the room.", "You deserve a hug right now.", "You should be proud of yourself.", "You're more helpful than you realize.", "You have a great sense of humor.", "You've got an awesome sense of humor!", "You are really courageous.", "Your kindness is a balm to all who encounter it.", "You're all that and a super-size bag of chips.", "On a scale from 1 to 10, you're an 11.", "You are strong.", "You're even more beautiful on the inside than you are on the outside.", "You have the courage of your convictions.", "I'm inspired by you.", "You're like a ray of sunshine on a really dreary day.", "You are making a difference.", "Thank you for being there for me.", "You bring out the best in other people.", "Your ability to recall random factoids at just the right time is impressive.", "You're a great listener.", "How is it that you always look great, even in sweatpants?", "Everything would be better if more people were like you!", "I bet you sweat glitter.", "You were cool way before hipsters were cool.", "That color is perfect on you.", "Hanging out with you is always a blast.", "You always know -- and say -- exactly what I need to hear when I need to hear it.", "You help me feel more joy in life.", "You may dance like no one's watching, but everyone's watching because you're an amazing dancer!", "Being around you makes everything better!", "When you say", "I meant to do that"," I totally believe you.", "When you're not afraid to be yourself is when you're most incredible.", "Colors seem brighter when you're around.", "You're more fun than a ball pit filled with candy. (And seriously, what could be more fun than that?)","That thing you don't like about yourself is what makes you so interesting.", "You're wonderful.", "You have cute elbows. For reals!", "Jokes are funnier when you tell them.", "You're better than a triple-scoop ice cream cone. With sprinkles.", "When I'm down you always say something encouraging to help me feel better.", "You are really kind to people around you.", "You're one of a kind!", "You help me be the best version of myself.", "If you were a box of crayons, you'd be the giant name-brand one with the built-in sharpener.", "You should be thanked more often. So thank you!!", "Our community is better because you're in it.", "Someone is getting through something hard right now because you've got their back. ", "You have the best ideas.", "You always find something special in the most ordinary things.", "Everyone gets knocked down sometimes, but you always get back up and keep going.", "You're a candle in the darkness.", "You're a great example to others.", "Being around you is like being on a happy little vacation.", "You always know just what to say.", "You're always learning new things and trying to better yourself, which is awesome.", "If someone based an Internet meme on you, it would have impeccable grammar.", "You could survive a Zombie apocalypse.", "You're more fun than bubble wrap.", "When you make a mistake, you try to fix it.", "Who raised you? They deserve a medal for a job well done.", "You're great at figuring stuff out.", "Your voice is magnificent.", "The people you love are lucky to have you in their lives.", "You're like a breath of fresh air.", "You make my insides jump around in the best way.", "You're so thoughtful.", "Your creative potential seems limitless.", "Your name suits you to a T.", "Your quirks are so you -- and I love that.", "When you say you will do something, I trust you.", "Somehow you make time stop and fly at the same time.", "When you make up your mind about something, nothing stands in your way.", "You seem to really know who you are.", "Any team would be lucky to have you on it.", "In high school I bet you were voted most likely to keep being awesome.", "I bet you do the crossword puzzle in ink.", "Babies and small animals probably love you.", "If you were a scented candle they'd call it Perfectly Imperfect (and it would smell like summer).", "There's ordinary, and then there's you.", "You're someone's reason to smile.", "You're even better than a unicorn, because you're real.", "How do you keep being so funny and making everyone laugh?", "You have a good head on your shoulders.", "Has anyone ever told you that you have great posture?", "The way you treasure your loved ones is incredible.", "You're really something special.", "Thank you for being you."

    ]
    await ctx.send(random.choice(compliments) + " " + user.mention)

#--- Give CPU and RAM Monitoring -------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='stats', help='Gives you the Status of the bot and server')
async def on_command(ctx):
    #if ctx.message.author.guild_permissions.administrator:
    embed = discord.Embed(title="Blackmagic Bot Statistics", color=0xff8000)
    embed.add_field(name='System Usage:', value=f'CPU: {psutil.cpu_percent()} RAM: {psutil.virtual_memory()[2]}')
    embed.add_field(name='Codeshare:', value='https://github.com/timhaettich/bmd')
    embed.add_field(name='Version::', value=f'v{VERSIONNR} This bot is still in Development.')
    embed.add_field(name='Member count:', value='{0}'.format(bot.get_guild(479297254528647188).member_count),inline="false")
    embed.add_field(name='Bot written by:', value='This bot was written by @TimothyLH, additional features were contributed by @dave. This bot is based on discord.py', inline="false")
    await ctx.send(embed=embed)
    #Reload Crawler Data, this is placed here, so it is called once in a while
    reloadData()

#--- Auto Commands --------------------------------------------------------------------------------------------------------------------------------------------
#--- Role asigning --------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 701068310019571824:
        map = {
            '📢':701006546645155870,
            '💰':701006651557412864,
            '🎥':701006754430976011,
            '🖥️':701006696717353091,
            '✍️':701006801981931640,
            '👨':701006871015850006,
        }
        print(payload.emoji.name)
        print(map[payload.emoji.name])
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = bot.get_guild(479297254528647188).get_role(map[payload.emoji.name])

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            print("done")
    if payload.message_id == 701071925656551489:
        map = {
            '🖥️':701007112016363540,
            '🎥':701007219306528810,
            '📡':701007421778296852
        }
        print(payload.emoji.name)
        print(map[payload.emoji.name])
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = bot.get_guild(479297254528647188).get_role(map[payload.emoji.name])

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            print("done")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 701071925656551489:
        map = {
            '🖥️':701007112016363540,
            '🎥':701007219306528810,
            '📡':701007421778296852
        }
        print(payload.emoji.name)
        print(map[payload.emoji.name])
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = bot.get_guild(479297254528647188).get_role(map[payload.emoji.name])

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            print("done")
    if payload.message_id == 701068310019571824:
        map = {
            '📢':701006546645155870,
            '💰':701006651557412864,
            '🎥':701006754430976011,
            '🖥️':701006696717353091,
            '✍️':701006801981931640,
            '👨':701006871015850006,
        }
        print(payload.emoji.name)
        print(map[payload.emoji.name])
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = bot.get_guild(479297254528647188).get_role(map[payload.emoji.name])

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            print("done")

#--- One time stuff --------------------------------------------------------------------------------------------------------------------------------------------
"""@bot.command(name='role-msg')
async def on_command(ctx):
    message1 = "🎬 You can assign yourself a role here 🎬\nThis will help others to quickly identify your interest and knowledge.\n\nYour occupation:\n📢  Director\n💰  Producer\n🎥 Camera Department\n🖥️  Post Production\n✍️  Writer\n👨  Hobbyist\nJust click the corresponding emoji below."
    message2 = ".\n\nYour gear:\n🖥️  Post Production Gear\n🎥  Camera Gear\n📡  Broadcasting\nJust click the corresponding emoji below."
    await ctx.send(message2)"""
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
bot.run(TOKEN)
