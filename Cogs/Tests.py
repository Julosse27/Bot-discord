import discord
from discord.ext import commands
from Stocks.File_stock.Recup_fichiers import recup_path, file_not_exist
from Stocks.Commands_stock import get_defer_time, timer
from discord import app_commands
from time import sleep

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
        await interaction.response.send_message(f'Tu as pris {self.values[0]}')

class Menu_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

class Tests(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Le cog basic ou tout est testé, j'ai commencé à coder ce avec ces commandes."

    @app_commands.command(name= "timer", description= "Démare un timer et fait une truc secret à la fin.")
    async def timer_command(self, interaction: discord.Interaction, secondes: int, minutes: int = 0, heures: int = 0, jours: int = 0, mois: int = 0, annee: int = 0):
        await interaction.response.send_message("Je me prépare")
        fonction = interaction.edit_original_response
        if await timer(secondes, fonction, "Il reste", "avant la surprise.", minutes, heures, jours, mois, annee):
            await fonction(content= "Voila votre surprise: 'Vous m'avez testé'")
        else:
            await fonction(content= "Il y a eu un problème dans le procesus votre récompense à été donc annulée.")


    @app_commands.command(name= "timestamp", description= "Envois un timestamp dans un Embed.")
    async def timestamp(self, interaction: discord.Interaction, secondes: int, minutes: int = 0, heures: int = 0, jours: int = 0, mois: int = 0, années: int = 0):
        if 0 == minutes == heures == jours == mois == années:
            timestamp = get_defer_time(secondes).timestamp() #type: ignore
        else:
            timestamp = get_defer_time([secondes, minutes, heures, jours, mois, années]).timestamp() #type: ignore
        em = discord.Embed(title= "Test du timestamp", description= f"Le voici:") #type: ignore
        await interaction.response.send_message(embed= em)

    @app_commands.command(name= "test_slash", description= "Envois un message 'test'")
    async def test_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(content= "test")

    @commands.command(name= "sleep", aliases= ["tests"], brief= "Envoie une réponse en décallé.", description= "Envois 'test' 3 secondes après l'envoi de la commande.")
    async def defer(self, ctx: commands.Context):
        message = await ctx.send("Je suis en train d'écrire.")
        sleep(3)
        await message.edit(content= "Ma réponse est 'test")
        
    @commands.command(name= "bouton", aliases= ["testb"], brief= "Fait spawn un bouton.", description= "Fait spawn le bouton de test.")
    async def bouton(self, ctx: commands.Context):
        await ctx.send(view= View())

    @commands.command(name= "menu", aliases= ["testm"], brief= "Fait spawn un menu.", description= "Fait spawn le menu de test.")
    async def mon_menu(self, ctx: commands.Context):
        await ctx.send(view= Menu_view())

    @commands.command(hidden= True)
    async def test(self, ctx: commands.Context, *, message: str):
        await ctx.author.send(content = message)
        await ctx.send(content = 'Message envoyé.')
    
    @commands.command(name = "download", aliases= ["télécharger", "tel"], brief= "Télécharge le fichier de test.", description= "Il téléchargera un fichier de texte simple créé pour le test spécialement")
    async def download(self, ctx: commands.Context, fichier: str):
        file = recup_path(fichier)
        if file == file_not_exist:
            await ctx.send(content= f"Désolé le fichier {fichier} n'existe pas dans ma mémoire")
        else:
            await ctx.send(content= f"Voici le fichier {fichier} que vous demandez.",file= discord.File(file, fichier))

    @app_commands.command(name = "download", description= "Il téléchargera un fichier de texte simple créé pour le test spécialement")
    async def tel(self, ctx: discord.Interaction, fichier: str):
        file = recup_path(fichier)
        if file == file_not_exist:
            await ctx.response.send_message(content= f"Désolé le fichier {fichier} n'existe pas dans ma mémoire", ephemeral= True)
        else:
            await ctx.response.send_message(content= f"Voici le fichier {fichier} que vous demandez.",file= discord.File(file, fichier), ephemeral= True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Tests(bot))
