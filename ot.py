TOKEN = ""
import discord
import os
import asyncio
import pytube
from discord.ext import commands
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
voice_client = None
paused = False


@bot.event
async def on_ready():
    print("Bot está conectado.")


@bot.event
async def on_message(message):
    global voice_client
    global paused
    if message.author == bot.user:
        return
    if "pause" in message.content.lower():
        if voice_client and not paused:
            voice_client.pause()
            paused = True
            await message.channel.send(
                "Música pausada. Para continuar, digite !continue."
            )
        else:
            await message.channel.send("Não estou tocando nada no momento.")
    elif "continue" in message.content.lower():
        if voice_client and paused:
            voice_client.resume()
            paused = False
            await message.channel.send("Música retomada.")
        else:
            await message.channel.send("Não há música pausada no momento.")
    elif "play" in message.content.lower():
        if message.author.voice and message.author.voice.channel:
            channel = message.author.voice.channel
            if voice_client is None:
                voice_client = await channel.connect()
            else:
                await voice_client.move_to(channel)
            query_parts = message.content.split("!play ")
            if len(query_parts) < 2:
                await message.channel.send(
                    "Você precisa fornecer um link para reproduzir música."
                )
                return
            query = query_parts[1]
            print("URL enviada:", query)
            url = None
            try:
                yt = pytube.YouTube(query)
                print(yt)
                url = yt.streams.filter(only_audio=True)[0].url
                print(url)
            except:
                await message.channel.send(
                    "Não foi possível encontrar a música solicitada."
                )
                return
            source = FFmpegPCMAudio(url)
            voice_client.play(source)
            while voice_client.is_playing() or paused:
                await asyncio.sleep(1)
            if not paused:
                await voice_client.disconnect()


bot.run(TOKEN)
