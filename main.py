import discord
import pywhatkit
import requests
from discord.ext import commands

bot_prefix = '-' # Your bot prefix here
bot_intents = discord.Intents.all() # Your bot intents here

client = commands.Bot(command_prefix=bot_prefix, intents=bot_intents)


prohibited_words = ['fuck', 'shit', 'asshole', 'bitch', 'cunt', 'dick', 'pussy', 'bastard', 'motherfucker', 'cock', 'twat', 'douche', 'wanker', 'prick', 'slut', 'whore', 'arse', 'bollocks', 'bugger', 'crap', 'damn', 'git', 'hell', 'jerk', 'idiot', 'moron', 'nitwit', 'nutter', 'sod', 'tosser', 'wank']

async def google_search(message, query):
    try:
        results = pywhatkit.search(query)
        if not results:
            await message.channel.send("No results found.")
            return
        
        result = results[0]
        
        if result.startswith("https://"):
            await message.channel.send(result)
        else:
            await message.channel.send("No results found.")
    except Exception as e:
        await message.channel.send("An error occurred during the search. Please try again later.")
        print(str(e))

@client.command()
async def google(ctx, *, query):
    await google_search(ctx.message, query)


@client.event
async def on_message(message):
    for word in message.content.split():
        if word.lower() in prohibited_words:
            response = "Your message contains a prohibited word. Please refrain from using this kind of language."
            await message.author.send(response)
            break
    await client.process_commands(message)

@client.command()
async def valorant(ctx):
    message = "@everyone Valorant anyone?"
    await ctx.send(message)


client.run('DISCORD TOKEN')
