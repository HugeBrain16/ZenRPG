import iniparser2
import discord


async def _about():
    metadata = iniparser2.INI()
    metadata.read_file("metadata.ini")

    embed = discord.Embed(title="About", color=0xFF00FF)
    embed.description = f"{metadata['program']['description']}\nSource: {metadata['program']['source']}\n\nPROGRAM:\n```Name: {metadata['program']['name']}\nVersion: v{metadata['program']['version']}```"
    embed.set_thumbnail(url=_about.client.user.avatar_url)

    await _about.message.channel.send(embed=embed)
