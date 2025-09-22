import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = "!",  description = "Bot du tuto", intents= discord.Intents.all())

class View(discord.ui.View):

    @discord.ui.button(label= "Testez moi!", style= discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, bouton):
        await interaction.user.send(f"Tu m'as testé !")
        await interaction.response.send_message(f"Bouton testé par {interaction.user.name}")
    
@bot.command(name= "bouton", description= "Fait spawn un bouton.")
async def bouton(ctx):
    await ctx.send(view= View())

class Menu(discord.ui.Select):  
    def __init__(self):
        options = [
            discord.SelectOption(
                label= "Test 1",
                description= "C'est le premier test"
            ),
            discord.SelectOption(
                label= "Test 2",
                description= "Le 2eme test"
            )
        ]

        super().__init__(placeholder="Quel test voulez vous ?", min_values= 1, max_values= 1, options= options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Tu as pris {self.values}')

class Menu_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

@bot.command(name= "menu", description= "Fait spawn un menu.")
@commands.has_role(1417199810099937411)
async def mon_menu(ctx):
    await ctx.send(view= Menu_view())

@bot.command()
async def test(ctx, *, message: str):
    await ctx.author.send(content = message)
    await ctx.send(content = 'Message envoyé.')

@bot.command()
async def message(ctx, member: discord.Member, *, contenu: str):
    await member.send(content= contenu)
    await ctx.send(content = 'Message envoyé !')

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    synced = await bot.tree.sync()
    print(f'{len(synced)} commande(s) syncronisée(s)')

token = "MTQxNjg2ODA3NjEwNzk5MzIyOQ.GjbM9g.aq3Rq9gMh2L7OgtW6b8Xqs5cqzeBaiC7Jr3dEU"

bot.run(token)