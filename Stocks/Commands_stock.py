from discord.ext import commands

def check_me(*ids):
        
        def predicate(ctx):
            for role in ctx.author.roles:
                if role.id in ids:
                    return True
            else:
                ctx.send(content = "Vous n'avez pas les permisions requises")
                return False
        

        return commands.check(predicate)
