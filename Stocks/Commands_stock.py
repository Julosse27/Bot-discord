from discord.ext import commands

def check_me(*ids):
        
        def predicate(ctx):
            for role in ctx.author.roles:
                if role.id in ids:
                    return True
            else:
                return False
        

        return commands.check(predicate)

