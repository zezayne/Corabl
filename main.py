import discord
import pywhatkit
import requests
from discord.ext import commands

bot_prefix = '-' # Your bot prefix here
bot_intents = discord.Intents.all() # Your bot intents here

client = commands.Bot(command_prefix=bot_prefix, intents=bot_intents)


@client.event
async def on_ready():
    print('Bot is ready.')

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



@client.command()
async def stat(ctx, *, player_name):
    player_name = player_name.replace("#", "%23")
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer API_TOKEN'
    }
    response = requests.get(f'https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{player_name}',
                            headers=headers)

    if response.status_code == 200:
        data = response.json()['data']
        stats = data['segments'][0]['stats']
        unrated_stats = None
        for segment in data['segments']:
            if segment['metadata']['name'] == 'Unrated':
                unrated_stats = segment['stats']
                break

        # Competitive mode stats
        comp_stats = {
            "Games Played": stats["competitive"]["gamesPlayed"],
            "Wins": stats["competitive"]["wins"],
            "Win %": stats["competitive"]["winRatePercentage"],
            "Kills": stats["competitive"]["kills"],
            "Deaths": stats["competitive"]["deaths"],
            "K/D Ratio": stats["competitive"]["kdRatio"],
            "Assists": stats["competitive"]["assists"],
            "Headshots": stats["competitive"]["headshots"],
            "Headshot %": stats["competitive"]["headshotPercentage"],
            "Total Damage": stats["competitive"]["damage"],
            "Average Damage": stats["competitive"]["averageDamage"]
        }

        # Unrated mode stats
        unrated_stats_dict = {}
        if unrated_stats:
            unrated_stats_dict = {
                "Games Played": unrated_stats["gamesPlayed"],
                "Wins": unrated_stats["wins"],
                "Win %": unrated_stats["winRatePercentage"],
                "Kills": unrated_stats["kills"],
                "Deaths": unrated_stats["deaths"],
                "K/D Ratio": unrated_stats["kdRatio"],
                "Assists": unrated_stats["assists"],
                "Headshots": unrated_stats["headshots"],
                "Headshot %": unrated_stats["headshotPercentage"],
                "Total Damage": unrated_stats["damage"],
                "Average Damage": unrated_stats["averageDamage"]
            }

        # Send the response to Discord channel
        embed = discord.Embed(title=f"Stats for {data['platformInfo']['platformUserHandle']}", color=discord.Color.green())
        embed.set_thumbnail(url=data['platformInfo']['avatarUrl'])
        embed.add_field(name="**Competitive Mode**", value="\n".join([f"**{k}:** {v}" for k, v in comp_stats.items()]), inline=False)
        if unrated_stats:
            embed.add_field(name="**Unrated Mode**", value="\n".join([f"**{k}:** {v}" for k, v in unrated_stats_dict.items()]), inline=False)
        await ctx.send(embed=embed)

    elif response.status_code == 404:
        await ctx.send(f"Player '{player_name}' not found. Please check the spelling and try again.")
    else:
        await ctx.send("Something went wrong. Please try again later.")


client.run('DISCORD_TOKEN')
