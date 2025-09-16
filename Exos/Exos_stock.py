import discord

class Tuto_1(discord.ui.View):
    def __init__(self, *,  timeout: float | None = None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label= "Commencer l'exercice !!", style= discord.ButtonStyle.blurple)
    async def button_callback(self, interaction: discord.Interaction, bouton):
        await interaction.user.send(f"Tu m'as testé !")
        await interaction.response.send_message(f"{interaction.user.name} à fait cet Exo")
