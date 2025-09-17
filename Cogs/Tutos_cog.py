import discord
from discord.ext import commands
from Stocks.Exo_stock import exos
from Stocks.Commands_stock import check_me

class Exo_b(discord.ui.View):
    def __init__(self, nb_exo):
        super().__init__(timeout = None)
        self.nb_exo = int(nb_exo)
    
    @discord.ui.button(label= "Testez moi!", style= discord.ButtonStyle.blurple)
    async def button_callback(self, interaction: discord.Interaction, bouton):
        await interaction.user.send(view = exos[self.nb_exo]())
        await interaction.response.send_message(f"Bouton testé par {interaction.user.name}")


class Menu(discord.ui.Select):  
    def __init__(self):
        options = [
            discord.SelectOption(
                label= "Exo sur les types de valeurs",
                value= "0"
            ),
            discord.SelectOption(
                label= "Exo sur le transtypage et les boucles",
                value= "1"
            )
        ]

        super().__init__(placeholder="Quel exo voulez vous ?", min_values= 1, max_values= 1, options= options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view= Exo_b(self.values[0]))
            

class Menu_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

class TutosCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name = "Exos_select", aliases = ["Exos", "Exo"], description = "Une commande qui permet de s'exercer aux diferents tutos.", brief = "Fait spawn un exo.")
    @check_me(1417199810099937411)
    async def monTuto(self, ctx):
        await ctx.send(view= Menu_view())


async def setup(bot: commands.Bot):    
    await bot.add_cog(TutosCog(bot))