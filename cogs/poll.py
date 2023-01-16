import nextcord
from nextcord.ext import commands


class QuickPoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = nextcord.Embed(title=question, description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)
        await ctx.author.send("```To end the poll you just made use this command\nsl_tally [Poll id]```")

    #@poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            em = nextcord.Embed(title="Error!", description="You can't do that! You dont have the permission required to perform this command (Manage messages)\nHaving trouble? Try `sl_help purge`", color= 0xFF0000, timestap=ctx.message.created_at)
            await ctx.send(embed=em)
        elif isinstance(error, commands.BadArgument):
            em = nextcord.Embed(title="Error!", description="Please provide valid fields\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            await ctx.send(embed=em)
        elif isinstance(error, commands.MissingRequiredArgument):
            em = nextcord.Embed(title="Error!", description="Please provide all the required arguments\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            await ctx.send(embed=em)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def tally(self, ctx, id=None):
        poll_message = await ctx.channel.fetch_message(id)
        embed = poll_message.embeds[0]
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        print(f'unformatted{unformatted_options}')
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)
        output = f"Results of the poll for '{embed.title}':\n" + '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(output)


def setup(bot):
    bot.add_cog(QuickPoll(bot))
