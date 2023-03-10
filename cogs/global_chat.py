import json
import nextcord
import datetime
from random import randint
from nextcord.ext import commands


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['gcstart'])
    @commands.has_permissions(administrator=True)
    async def globalchatstart(self, ctx, channel):
        guild_id = ctx.message.guild.id
        channel_id = int(channel.strip('<#>'))

        with open('databases/global_chat.json', 'r') as file:
            global_chat_data = json.load(file)
            new_global_chat = str(guild_id)

            # Existing global chat
            if new_global_chat in global_chat_data:
                await ctx.send(':no_entry: **Channel has already added to global chat!**')

            # Add new global chat
            else:
                global_chat_data[new_global_chat] = channel_id
                with open('databases/global_chat.json', 'w') as new_global_chat:
                    json.dump(global_chat_data, new_global_chat, indent=4)

                await ctx.send(':white_check_mark: **Channel has been added to global chat!**')

    @commands.command(aliases=['gcstop'])
    @commands.has_permissions(administrator=True)
    async def globalchatstop(self, ctx):
        guild_id = ctx.message.guild.id

        with open('databases/global_chat.json', 'r') as file:
            global_chat_data = json.load(file)

        global_chat_data.pop(str(guild_id))

        # Update global chat
        with open('databases/global_chat.json', 'w') as update_global_chat_file:
            json.dump(global_chat_data, update_global_chat_file, indent=4)

        await ctx.send(':white_check_mark: **Channel has been removed from global chat!**')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.content.startswith('!'):
                with open('databases/global_chat.json', 'r') as file:
                    global_chat_data = json.load(file)

                channel_id = list(global_chat_data.values())

                # Message sender
                if message.channel.id in channel_id:

                    # Unsupported message content
                    if not message.content:
                        return

                    # Message receiver
                    for ids in channel_id:
                        if message.channel.id != ids:
                            message_embed = nextcord.Embed(colour=randint(0, 0xffffff))
                            if message.author.avatar.url == None:
                                icon_url="https://cdn.discordapp.com/avatars/1054719146304225285/e5ab0ff9744fc47e40b20a65aad406a8.png?size=1024"
                            icon_url = message.author.avatar.url
                            message_embed.timestamp = datetime.datetime.now()
                            message_embed.set_author(icon_url=message.author.avatar.url, name=f'{message.author}')
                            message_embed.description = f'**`Said: {message.content}`**'
                            message_embed.set_footer(text=message.guild.name)
                            try:
                            	channel=await self.bot.fetch_channel(ids)
                            	await channel.send(embed=message_embed)
                            except Exception as e:
                                print(e)


def setup(bot):
    bot.add_cog(GlobalChat(bot))
