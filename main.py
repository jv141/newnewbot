import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
client = discord.Client()
from discord.ext import commands
from discord.ext.commands import Bot
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
from discord.ext.commands import cooldown, BucketType





client = commands.Bot(command_prefix="<", case_insensitive=True)
bot = commands.Bot(command_prefix="<", case_insensitive=True)



@client.command(aliases = ["bal"])
async def balance(self, ctx, user: discord.Member = None):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  beurs_amt = users[str(user.id)]["beurs"]
  bank_amt = users[str(user.id)]["bank"]
  
  em = discord.Embed(title = f"{ctx.author.name}'s balans")
  em.add_field(name = "beurs balans",value = beurs_amt)
  em.add_field(name = "Bank balans",value = bank_amt)
  await ctx.send(embed = em)

@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def beg(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author
  
  earnings = random.randrange(50)

  await ctx.send(f"iemand gaf jou {earnings} munten!!")


  users[str(user.id)]["beurs"] += earnings

  with open("mainbank.json","w") as f:
      json.dump(users,f)

@beg.error
async def command_name_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"doe eens rustig",description=f"je kan nog eens bedelen over {error.retry_after:.2f} seconden")
            await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 7200, commands.BucketType.user)
async def work(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author
  
  earnings = random.randrange(250)

  await ctx.send(f"je hebt gewerkt en {earnings} munten verdient. netjes")


  users[str(user.id)]["beurs"] += earnings

  with open("mainbank.json","w") as f:
      json.dump(users,f)

@work.error
async def werk_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"doe eens rustig",description=f"je kan nog eens werken over {error.retry_after:.2f} seconden")
            await ctx.send(embed=em)



@client.command()
async def withdraw(ctx,amount = None):
  await open_account(ctx.author)

  if amount == None:
      await ctx.send("Vul de hoeveelheid in")
      return

  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[1]:
    await ctx.send("Zoveel geld heb je niet!")
    return
  if amount<0:
    await ctx.send("De hoeveelheid moet boven de 0 zijn!")
    return

  await update_bank(ctx.author,amount)
  await update_bank(ctx.author,-1*amount,"bank")

  await ctx.send(f"je hebt {amount} munten opgenomen!")


@client.command()
async def deposit(ctx,amount = None):
  await open_account(ctx.author)

  if amount == None:
      await ctx.send("Vul de hoeveelheid in")
      return

  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("Zoveel geld heb je niet!")
    return
  if amount<0:
    await ctx.send("De hoeveelheid moet boven de 0 zijn!")
    return

  await update_bank(ctx.author,-1*amount)
  await update_bank(ctx.author,amount,"bank")

  await ctx.send(f"je hebt {amount} munten gestort!")


@client.command()
async def send(ctx,member:discord.Member,amount = None):
  await open_account(ctx.author)
  await open_account(member)

  if amount == None:
      await ctx.send("Vul de hoeveelheid in")
      return

  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[1]:
    await ctx.send("Zoveel geld heb je niet!")
    return
  if amount<0:
    await ctx.send("De hoeveelheid moet boven de 0 zijn!")
    return

  await update_bank(ctx.author,-1*amount,"bank")
  await update_bank(member,amount,"bank")

  await ctx.send(f"jij hebt {amount} munten gegeven!")

@client.command()
async def rob(ctx,member:discord.Member):
  await open_account(ctx.author)
  await open_account(member)

  bal = await update_bank(member)

  if bal[0]<100:
    await ctx.send("Die gebruiker is te arm om van te stelen!")
    return

  earnings = random.randrange(0, bal[0])

  await update_bank(ctx.author,earnings)
  await update_bank(member,-1*earnings)

  await ctx.send(f"je hebt {earnings} munten gestolen!")


@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)
async def slots(ctx,amount = None):
  await open_account(ctx.author)

  if amount == None:
      await ctx.send("vul de hoeveelheid in")
      return

  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("Zoveel geld heb je niet!")
    return
  if amount<0:
    await ctx.send("De hoeveelheid moet boven de 0 zijn!")
    return

  final = []
  for i in range(4):
      a = random.choice(["🍎","🍋","🍊","🍉"])

      final.append(a)

  await ctx.send(str(final))

  if final[0] == final[1]  == final[2] or final[0] == final[1]  == final[3] or final[0] == final[2]  == final[3] or final[1] == final[2]  == final[3]:
    await update_bank(ctx.author,2*amount)
    await ctx.send("Je hebt gecheat en gewonnen")
  else:
    await update_bank(ctx.author,-1*amount)
    await ctx.send("You hebt verloren LOSER!!")

@slots.error
async def slots_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"doe eens rustig",description=f"je kan nog eens gokken over {error.retry_after:.2f} seconden")
            await ctx.send(embed=em)


mainshop = [{"name":"Horloge","price":100,"description":"Tijd"},
            {"name":"Appel","price":50,"description":"Eten"},
            {"name":"PC","price":10000,"description":"Gaming"}]


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"€{price} | {desc} ")

    await ctx.send(embed = em)



@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("Dat object bestaat niet hier!")
            return
        if res[1]==2:
            await ctx.send(f"maat je bent te skeer om {amount} {item} te kopen")
            return


    await ctx.send(f"Jij hebt zojuist {amount} {item} gekocht")
##
@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["beurs"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)
##
@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        rugzak = users[str(user.id)]["rugzak"]
    except:
        rugzak = []


    em = discord.Embed(title = "rugzak")
    for item in rugzak:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)    



async def open_account(user):

  users = await get_bank_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["beurs"] = 0
    users[str(user.id)]["bank"] = 0

    with open("mainbank.json","w") as f:
      json.dump(users,f)
    return True


async def get_bank_data():
  with open("mainbank.json","r") as f:
    users = json.load(f) 

  return users

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["rugzak"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["rugzak"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["rugzak"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["rugzak"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"beurs")

    return [True,"Worked"]

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your rugzak.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your rugzak.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["rugzak"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["rugzak"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"beurs")

    return [True,"Worked"]

async def update_bank(user,change = 0,mode = "beurs"):
  users = await get_bank_data()

  users[str(user.id)][mode] += change

  with open("mainbank.json","w") as f:
      json.dump(users,f)

  bal = [users[str(user.id)]["beurs"],users[str(user.id)]["bank"]]
  return bal
  
###

@client.command()
@has_permissions(kick_members=True)
async def giveaway(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly

    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = ['Which channel will I host the giveaway in?', 'What is the prize?', 'How long should the giveaway run for (in seconds)?',]
    giveaway_answers = []

    # Checking to be sure the author is the one who answered and in which channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    # Askes the questions from the giveaway_questions list 1 by 1
    # Times out if the host doesn't answer within 30 seconds
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for('message', timeout= 30.0, check= check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time. Please try again and be sure to send your answer within 30 seconds of the question.')
            return
        else:
            giveaway_answers.append(message.content)

    # Grabbing the channel id from the giveaway_questions list and formatting is properly
    # Displays an exception message if the host fails to mention the channel correctly
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(f'You failed to mention the channel correctly. Please do it like this: {ctx.channel.mention}')
        return
    
    # Storing the variables needed to run the rest of the commands
    channel = client.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.send(f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds.')

    # Giveaway embed message
    give = discord.Embed(color = 0x2ecc71)
    give.set_author(name = f'GIVEAWAY TIME!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
    give.add_field(name= f'{ctx.author.name} is giving away: {prize}!', value = f'React with 🎉 to enter!\n Ends in {round(time/60, 2)} minutes!', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
    give.set_footer(text = f'Giveaway ends at {end.strftime("%m/%d/%Y, %H:%M")} UTC!')
    my_message = await channel.send(embed = give)
    
    # Reacts to the message
    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the winner
    winning_announcement = discord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'THE GIVEAWAY HAS ENDED!', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 Prize: {prize}', value = f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Thanks for entering!')
    await channel.send(embed = winning_announcement)


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
async def poll_error(ctx, error):
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
async def aank_error(ctx, error):
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
async def say_error(ctx, error):
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
async def warn_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")


###MEME


@client.command(pass_context=True, name='meme', help='Stuurt een meme')
async def meme(ctx):
    embed = discord.Embed(title="een slechte meme", description="")
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

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
        'Ik ben moe. *gaat slapen*', 'zelfs ik weet het antwoord niet', 'Je wilt het antwoord niet weten', 'Waarom  gebruik je je hersencellen niet en verzin je zelf een antwoord?','Stop eens met vragen stellen'
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
async def purge_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(
            "u heeft geen toestemming om dit te gebruiken")

####Joke

@client.command(name='joke',
                description="Random slechte grap",
                brief="Random slechte grap",
                aliases=['grap', 'dadjoke'],
                pass_context=True)
async def joke(ctx):
   async with aiohttp.ClientSession() as session:
      # This time we'll get the joke request as well!
      request = await session.get('https://some-random-api.ml/joke')
      jokejson = await request.json()
      async with ctx.typing():
          await asyncio.sleep(1)
   
   embed = discord.Embed(title="Another bad joke", color=discord.Color.purple())
   embed.set_footer(text=jokejson['joke'])
   await ctx.send(embed=embed)
      
###NEW

#### status
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name="Naamloos..."))
    print("Bot is ready!")

###


  
##
keep_alive()
client.run(os.getenv('TOKEN'))


