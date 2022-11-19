import discord
import os
import requests
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import logging
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from random import randint
from random import choice as randchoice
import datetime
import time
import aiohttp
import praw
from discord import Embed
from requests import get
import sys
from secret import token


client = commands.Bot(command_prefix="<", case_insensitive=True, intents=discord.Intents.all())



##### POLL
@client.command(pass_context=False ,hidden=True)
@commands.has_permissions(administrator=True)
async def poll(ctx, *, content: str):
    print("Creating yes/no poll...")
    #create the embed file
    embed = discord.Embed(
        title=f"{content}",
        description="Reageer op dit bericht met ✅ voor ja, of ❌ voor nee.",
        color=0x00ff00)
    #set the author and icon
    embed.set_author(name="NAAMLOOS POLL: ")
    print("Embed created")
    #send the embed
    message = await ctx.message.delete()
    message = await ctx.channel.send(embed=embed)
    #add the reactions
    await message.add_reaction("✅")
    await message.add_reaction("❌")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")



##### ANNOUNCE?
@client.command(pass_context=False ,hidden=True)
@commands.has_permissions(administrator=True)
async def aank(ctx, *, content: str):
    print("Creating announcement")
    #create the embed file
    embed = discord.Embed(
        title=f"{content}",
        description="",
        color=0x0000FF)
    #set the author and icon
    embed.set_author(name="NAAMLOOS SMP AANKONDIGING: ")
    print("Embed created")
    #send the embed
    message = await ctx.message.delete()
    message = await ctx.channel.send(embed=embed)
    #add the reactions
    await message.add_reaction("👍")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")


#####onderhoud?
@client.command(pass_context=False ,hidden=True)
@commands.is_owner()
async def main(ctx, *, content: str):
    print("Creating announcement")
    #create the embed file
    embed = discord.Embed(
        title=f"{content}",
        description="",
        color=0x0000FF)
    #set the author and icon
    embed.set_author(name="BOT ONDERHOUD AANKONDIGING: ")
    print("Embed created")
    #send the embed
    message = await ctx.message.delete()
    message = await ctx.channel.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")
  

####WEEKNUMMER

@client.command(pass_context=True, name='week', help='Stuurt het nummer van de week')
async def week(ctx):
     my_date = datetime.date.today() # if date is 01/01/2018
     year, week_num, day_of_week = my_date.isocalendar()
        
     await ctx.channel.send("Het is week #" + str(week_num) + " Van het jaar " + str(year))

      
####REBOOT
def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@client.command(pass_context=False ,hidden=True)
@commands.has_permissions(administrator=True)
async def restart(ctx):
  await ctx.send("De bot start opnieuw op...")
  restart_bot()  


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")
  
  
############ REPEAT
@client.command(pass_context=False ,hidden=True)
@commands.has_permissions(administrator=True)
async def say(ctx, *, text=''):
    if text == '':
        await ctx.send("U moet iets zeggen")
    else:
        await ctx.send(text)
        await ctx.message.delete()
      
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")





###Warn
@client.command(pass_context=False ,hidden=True)
@commands.has_permissions(administrator=True)
async def warn(ctx, *, text=''):
    if text == '':
        await ctx.send("Tag iemand")
    else:
        await ctx.message.delete()
        await ctx.send(text)
        message = await ctx.channel.send("JE BENT GEWAARSCHUWD")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")


###MEME


@client.command(pass_context=True, name='meme', help='Stuurt een meme')
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content, )
    meme = discord.Embed(
        title=f"{data['title']}",
        Color=discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.channel.send(embed=meme)

###IP


@client.command(pass_context=True, name='ip', help='Stuurt het ip van de server')
async def ip(ctx):
  async with ctx.typing():
    await asyncio.sleep(2)
    await ctx.channel.send("het ip van de server is: play.publicnaamloos.nl")



###8ball
@client.command(name='8ball',
                description="Antwoord op een ja of nee vraag",
                brief="Antwoord op een ja of nee vraag",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'Zoals ik het zie. Ja', 'Ja',
        'Ik ben overtuigd van wel', 'Grote kans van wel', 'Nee',
        'Ik ben er niet van overtuigd', 'Misschien', 'Ik weet het niet zeker', 'Waarschijnlijk',
        'Ik kan nu geen antwoord geven', 'Ik ben nu te lui om antwoord te geven',
        'Ik ben moe. *gaat slapen*', 'zelfs ik weet het antwoord niet', 'Je wilt het antwoord niet weten', 'Waarom  gebruik je je hersencellen niet en verzin je zelf een antwoord?'
    ]
    await context.channel.send(
        random.choice(possible_responses) + ", " +
        context.message.author.mention)


#### PURGE
@client.command(pass_context=False ,hidden=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")


###NEW

#### status
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name="Naamloos..."))
    print("Bot is ready!")


##
client.run(token)
