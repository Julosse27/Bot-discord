from discord.ext import commands

async def check_me(*ids):
        
        async def predicate(ctx: commands.Context):
            for id in ids:
                if ctx.author.get_role(id) != None:
                    return True
            else:
                await ctx.send(content= "Vous n'avez pas les permisions requises !!!")
                return False

        return commands.check(predicate)


