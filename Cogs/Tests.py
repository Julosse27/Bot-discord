import discord
from discord.ext import commands

class View(discord.ui.View):
    def __init__(self, *, timeout: float | None = None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label= "Testez moi!", style= discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, bouton):
        await interaction.user.send(f"Tu m'as testé !")
        await interaction.response.send_message(f"Bouton testé par {interaction.user.name}")

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

class TestsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= "bouton", aliases= ["testb"], brief= "Fait spawn un bouton.", description= "Fait spawn le bouton de test.")
    async def bouton(self, ctx):
        await ctx.send(view= View())

    @commands.command(name= "menu", aliases= ["testm"], brief= "Fait spawn un menu.", description= "Fait spawn le menu de test.")
    async def mon_menu(self, ctx):
        await ctx.send(view= Menu_view())

    @commands.command(hidden= True)
    async def test(self, ctx, *, message: str):
        await ctx.author.send(content = message)
        await ctx.send(content = 'Message envoyé.')

async def setup(bot: commands.Bot):

    await bot.add_cog(TestsCog(bot))
