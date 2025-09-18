import discord
from time import sleep

class Tuto_1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label= "Commencer l'exercice !!", style= discord.ButtonStyle.blurple)
    async def button_callback(self, interaction: discord.Interaction, bouton):
        await interaction.response.defer()
        sleep(5)
        await interaction.user.send(f"Tu m'a testé")
        await interaction.response.send_message(f"Regarde tes messages privés {interaction.user.name}!", ephemeral= True)

exos = [Tuto_1]
