import discord
from discord.ext import commands
from discord import app_commands
from Stocks.Exo_stock import exos
from Stocks.Commands_stock import check_basic_command
from time import sleep, asctime

mois = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label= "Exo sur les types de valeurs",
                value= "0"
            ),
            discord.SelectOption(
                label= "Exo sur le transtypage et les instructions conditionelles",
                value= "1"
            )
        ]

        super().__init__(placeholder="Quel exo voulez vous ?", min_values= 1, max_values= 1, options= options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.delete_original_response()
        await interaction.response.send_message(content= "Voici ton exercice.")
            

class Menu_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())


class Tutos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Tout les tutos doivents bien venir de quelque part non ?"

    @app_commands.command(name= "exos", description= "Permet de lancer un exercice grace a son nom.")
    async def exo(self, interaction: discord.Interaction, nom: str):
        await interaction.response.defer(thinking= True, ephemeral= True)
        for exo in exos:
            if exo["nom"] == nom:
                questions = exo["questions"]
                break
        else:
            sleep(2)
            await interaction.edit_original_response(content= "Cet exercice n'existe pas.")

        for view, enonce, bonne_rep in questions:
            await interaction.edit_original_response(embed= discord.Embed(color= interaction.user.color, title= f"Question {questions.index((view, enonce, bonne_rep)) + 1}", description= enonce), view= view)
            
            await view.wait()
            
            for i in range(len(view.children)):
                if view.children[i].rep:
                    datetime = asctime()
                    annee = int(datetime[20:])
                    mois_date = mois.index(datetime[4:7])
                    jour = int(datetime[8:10])
                    heures = int(datetime[11:13])
                    minutes = int(datetime[14:16])
                    secondes = int(datetime[17:19])
                    if secondes + 15 >= 60:
                        minutes += 1
                        secondes = (secondes + 15) - 60

                    timestamp = discord.datetime(year= annee, month= mois_date, day= jour, hour= heures, minute= minutes, second= secondes)
                    if bonne_rep == i:
                        await interaction.edit_original_response(embed= discord.Embed(color= interaction.user.color, title= "Vous avez eu la bonne réponse.", description= f"La réponse était bien {view.children[i].label}.", timestamp= timestamp))
                    else:
                        await interaction.edit_original_response(embed= discord.Embed(color= interaction.user.color, title= "Vous n'avez pas eu la bonne réponse.", description= f"La bonne réponse était {view.children[bonne_rep].label}.", timestamp= timestamp))
            
            sleep(15)

        
async def setup(bot: commands.Bot):    
    await bot.add_cog(Tutos(bot))
